from src.command_handler import CommandHandler
from src.database import Database
from src.system_tools import SystemTools
from src.web_tools import WebTools

class Assistant:
    def __init__(self):
        self.name = "Eros"
        self.database = Database("data/memory.db")
        self.web_tools = WebTools()
        self.system_tools = SystemTools()
        self.command_handler = CommandHandler(self.system_tools, self.web_tools, self.database)

    def start(self):
        print(f"{self.name}: Olá! Como posso ajudar? (digite 'ajuda' para ver os comandos disponíveis)")

        while True:
            try:
                user_input = input("Você: ").strip()

                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print(f"{self.name}: Até logo!")
                    break

                response = self.command_handler.process_command(user_input)
                print(f"{self.name}: {response}")

                self.database.save_interaction(user_input, response)

            except KeyboardInterrupt:
                print("\nEncerrando o assistente...")
                break
            except Exception as e:
                print(f"Erro: {str(e)}")
