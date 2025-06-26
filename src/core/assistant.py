from nlp.intent_classifier import IntentClassifier

class Assistant:
    def __init__(self):
        self.name = "Eros"
        self.running = True  # controla o loop
        self.classifier = IntentClassifier("data/intents.json")

    def start(self):
        # Print de Inicio
        print(f"{self.name}: Olá! Estou pronto para conversar. (Digite 'sair' para encerrar)")

        while self.running:
            user_input = input("Você: ").strip().lower()

            if user_input in ['sair', 'exit', 'quit']:
                self.shutdown()
            else:
                self.handle_input(user_input)

    # Processa o que a pessoa escreveu
    def handle_input(self, user_input):
        tag, conf = self.classifier.predict_intent(user_input)
        resposta = self.classifier.get_response(tag)
        if conf <= 0.6:
            print(f"{self.name}: Desculpe, não entendi bem. ({conf:.2f})")
        else:
            print(f"{self.name}: {resposta} ({conf:.2f})")

    # Encerra o Eros
    def shutdown(self):
        print(f"{self.name}: Até mais!")
        self.running = False
