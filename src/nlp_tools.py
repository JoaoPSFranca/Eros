import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class NLPTools:
    def __init__(self):
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except:
            print("Modelo spaCy não encontrado. Instalando...")
            import os
            os.system("python -m spacy download pt_core_news_sm")
            self.nlp = spacy.load("pt_core_news_sm")

        self.context = []  # Manter contexto da conversa

    def analyze_sentiment(self, text):
        doc = self.nlp(text)

        positive_words = {"bom", "ótimo", "excelente", "feliz", "contente", "maravilhoso", "fantástico"}
        negative_words = {"ruim", "péssimo", "terrível", "triste", "chateado", "horrível", "decepcionado"}

        words = [token.lemma_.lower() for token in doc]

        positive_score = sum(1 for word in words if word in positive_words)
        negative_score = sum(1 for word in words if word in negative_words)

        if positive_score > negative_score:
            return "positivo"
        elif negative_score > positive_score:
            return "negativo"
        else:
            return "neutro"

    def extract_entities(self, text):
        doc = self.nlp(text)
        entities = {}

        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)

        return entities

    def update_context(self, text):
        self.context.append(text)
        if len(self.context) > 5:
            self.context.pop(0)

    def get_context(self):
        return " ".join(self.context)

    def text_similarity(self, text1, text2):
        doc1 = self.nlp(text1)
        doc2 = self.nlp(text2)

        if not doc1.has_vector or not doc2.has_vector:
            return 0.0

        return doc1.similarity(doc2)