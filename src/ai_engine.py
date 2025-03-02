import os
import numpy as np
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from src.nlp_tools import NLPTools

try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('wordnet')
    nltk.download('punkt')


class AIEngine:
    def __init__(self):
        self.intents_file = "data/ai/intents.json"
        self.model_file = "data/ai/model.pkl"
        self.vectorizer_file = "data/ai/vectorizer.pkl"
        self.lemmatizer = WordNetLemmatizer()
        self.intents = {}
        self.model = None
        self.vectorizer = None
        self.nlp = NLPTools()
        self.conversation_context = []
        self.context_length = 5
        self.setup_ai()

    def setup_ai(self):
        try:
            os.makedirs('data/ai', exist_ok=True)

            if not os.path.exists(self.intents_file):
                basic_intents = {
                    "intents": [
                        {
                            "tag": "saudacao",
                            "patterns": [
                                "oi", "olá", "e aí", "bom dia", "boa tarde", "boa noite"
                            ],
                            "responses": [
                                "Olá! Como posso ajudar?",
                                "Oi! Em que posso ser útil hoje?",
                                "Olá! O que você precisa?"
                            ]
                        },
                        {
                            "tag": "despedida",
                            "patterns": [
                                "tchau", "até mais", "até logo", "adeus"
                            ],
                            "responses": [
                                "Até logo!",
                                "Foi um prazer ajudar!",
                                "Volte sempre que precisar!"
                            ]
                        },
                        {
                            "tag": "agradecimento",
                            "patterns": [
                                "obrigado", "obrigada", "valeu", "agradeço"
                            ],
                            "responses": [
                                "Por nada!",
                                "Disponha!",
                                "É um prazer ajudar!"
                            ]
                        },
                        {
                            "tag": "ajuda",
                            "patterns": [
                                "me ajude", "preciso de ajuda", "pode me ajudar"
                            ],
                            "responses": [
                                "Claro, como posso ajudar?",
                                "Estou aqui para ajudar. O que você precisa?",
                                "Digite 'ajuda' para ver todos os comandos disponíveis."
                            ]
                        }
                    ]
                }
                with open(self.intents_file, 'w', encoding='utf-8') as f:
                    json.dump(basic_intents, f, indent=4, ensure_ascii=False)

            self.load_intents()

            if os.path.exists(self.model_file) and os.path.exists(self.vectorizer_file):
                self.load_model()
            else:
                self.train_model()


        except Exception as e:
            print(f"Erro ao configurar IA: {e}")

    def load_intents(self):
        try:
            with open(self.intents_file, 'r', encoding='utf-8') as f:
                self.intents = json.load(f)
        except Exception as e:
            print(f"Erro ao carregar intents: {e}")
            self.intents = {"intents": []}

    def preprocess_text(self, text):
        tokens = word_tokenize(text.lower())
        return [self.lemmatizer.lemmatize(word) for word in tokens]

    def train_model(self):
        try:
            X = []  # frases de entrada
            y = []  # tags correspondentes

            for intent in self.intents["intents"]:
                for pattern in intent["patterns"]:
                    X.append(pattern)
                    y.append(intent["tag"])

            if not X:
                print("Sem dados de treinamento!")
                return False

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            self.vectorizer = TfidfVectorizer(tokenizer=self.preprocess_text)
            X_train_tfidf = self.vectorizer.fit_transform(X_train)

            clf = SVC(kernel='linear', probability=True)
            clf.fit(X_train_tfidf, y_train)

            self.model = clf

            X_test_tfidf = self.vectorizer.transform(X_test)
            accuracy = self.model.score(X_test_tfidf, y_test)
            print(f"Acurácia do modelo: {accuracy:.2f}")

            with open(self.model_file, 'wb') as f:
                pickle.dump(self.model, f)

            with open(self.vectorizer_file, 'wb') as f:
                pickle.dump(self.vectorizer, f)

            return True
        except Exception as e:
            print(f"Erro ao treinar modelo: {e}")
            return False

    def load_model(self):
        try:
            with open(self.model_file, 'rb') as f:
                self.model = pickle.load(f)

            with open(self.vectorizer_file, 'rb') as f:
                self.vectorizer = pickle.load(f)

            return True
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            self.model = None
            self.vectorizer = None
            return False

    def update_context(self, text):
        self.conversation_context.append(text)
        if len(self.conversation_context) > self.context_length:
            self.conversation_context.pop(0)
        self.nlp.update_context(text)

    def get_context_enhanced_input(self, text):
        if not self.conversation_context:
            return text

        entities = self.nlp.extract_entities(text)
        entity_text = ""

        for entity_type, values in entities.items():
            if entity_type in ['PERSON', 'ORG', 'GPE', 'LOC', 'PRODUCT']:
                entity_text += " " + " ".join(values)

        return text + " " + entity_text

    def predict_intent(self, text):
        if not self.model or not self.vectorizer:
            return None, 0.0

        try:
            enhanced_text = self.get_context_enhanced_input(text)

            text_tfidf = self.vectorizer.transform([enhanced_text])

            intent_probs = self.model.predict_proba(text_tfidf)[0]
            max_prob = max(intent_probs)
            max_idx = np.argmax(intent_probs)
            predicted_tag = self.model.classes_[max_idx]

            self.update_context(text)

            return predicted_tag, max_prob
        except Exception as e:
            print(f"Erro ao predizer intent: {e}")
            return None, 0.0

    def get_response(self, text):
        tag, confidence = self.predict_intent(text)

        sentiment = self.nlp.analyze_sentiment(text)

        if confidence < 0.4 or not tag:
            for intent in self.intents["intents"]:
                for pattern in intent["patterns"]:
                    similarity = self.nlp.text_similarity(text, pattern)
                    if similarity > 0.7:
                        tag = intent["tag"]
                        confidence = similarity
                        break

        if confidence < 0.3 or not tag:
            return None

        for intent in self.intents["intents"]:
            if intent["tag"] == tag:
                responses = intent["responses"]

                if sentiment == "positivo" and len(responses) > 1:
                    positive_responses = [r for r in responses if
                                          any(word in r.lower() for word in ["!", "ótimo", "excelente"])]
                    if positive_responses:
                        return random.choice(positive_responses)

                elif sentiment == "negativo" and len(responses) > 1:
                    empathic_responses = [r for r in responses if
                                          any(word in r.lower() for word in ["ajudar", "claro", "posso"])]
                    if empathic_responses:
                        return random.choice(empathic_responses)

                return random.choice(responses)

        return None

    def add_training_data(self, tag, patterns, responses):
        try:
            tag_exists = False
            for intent in self.intents["intents"]:
                if intent["tag"] == tag:
                    intent["patterns"].extend([p for p in patterns if p not in intent["patterns"]])
                    intent["responses"].extend([r for r in responses if r not in intent["responses"]])
                    tag_exists = True
                    break

            if not tag_exists:
                self.intents["intents"].append({
                    "tag": tag,
                    "patterns": patterns,
                    "responses": responses
                })

            with open(self.intents_file, 'w', encoding='utf-8') as f:
                json.dump(self.intents, f, indent=4, ensure_ascii=False)

            return self.train_model()
        except Exception as e:
            print(f"Erro ao adicionar dados de treinamento: {e}")
            return False

    def get_model_stats(self):
        if not self.model or not self.vectorizer:
            return "Modelo não carregado."

        try:
            num_intents = len(self.intents["intents"])
            total_patterns = sum(len(intent["patterns"]) for intent in self.intents["intents"])
            total_responses = sum(len(intent["responses"]) for intent in self.intents["intents"])

            most_patterns = max(self.intents["intents"], key=lambda x: len(x["patterns"]))

            if hasattr(self.model, 'support_'):
                support_vectors = len(self.model.support_)
            else:
                support_vectors = "N/A"

            stats = f"Estatísticas do modelo:\n"
            stats += f"- Número de intents: {num_intents}\n"
            stats += f"- Total de padrões: {total_patterns}\n"
            stats += f"- Total de respostas: {total_responses}\n"
            stats += f"- Intent com mais padrões: {most_patterns['tag']} ({len(most_patterns['patterns'])} padrões)\n"
            stats += f"- Vetores de suporte: {support_vectors}\n"
            stats += f"- Tamanho do vocabulário: {len(self.vectorizer.get_feature_names_out())}\n"

            return stats
        except Exception as e:
            return f"Erro ao obter estatísticas: {e}"