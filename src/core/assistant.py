class Assistant:
    def __init__(self):
        self.name = "Eros"
        self.running = True  # controla o loop

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
        print(f"{self.name}: Você disse: '{user_input}'")

    # Encerra o Eros
    def shutdown(self):
        print(f"{self.name}: Até mais!")
        self.running = False
