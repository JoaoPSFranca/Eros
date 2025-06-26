import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

class IntentClassifier:
    def __init__(self, path_to_intents: str):
        self.intents = self.load_intents(path_to_intents)
        self.vectorizer = TfidfVectorizer()
        self.model = SVC(probability=True)
        self.tags = []
        self.train()

    def load_intents(self, path: str) -> list:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['intents']

    def train(self):
        patterns = []
        tagList = []

        for intent in self.intents:
            for pattern in intent['patterns']:
                patterns.append(pattern)
                tagList.append(intent['tag'])

        self.vectorizer.fit(patterns)
        X_vectors = self.vectorizer.transform(patterns)

        self.model.fit(X_vectors, tagList)
        self.tags = list(set(tagList))  # salva para referência

    def predict_intent(self, sentence: str) -> tuple[str, float]:
        vec = self.vectorizer.transform([sentence])
        pred = self.model.predict(vec)[0]
        probs = self.model.predict_proba(vec)[0]
        conf = max(probs)

        return pred, conf

    def get_response(self, tag: str) -> str:
        for intent in self.intents:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
        return "Desculpe, não entendi."
