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
        self.colors = {
            "Red": '\033[31m',
            "Green": '\033[32m',
            "Blue": '\033[34m',
            "Cyan": '\033[36m',
            "Pink": '\033[35m',
            "Yellow": '\033[33m',
            "Black": '\033[30m',
            "White": '\033[37m',
            "Reset": '\033[0;0m',
            "LightGreen": '\033[1;32m'
        }

    def start(self):
        print(f"{self.colors['Blue']}{self.name}: {self.colors['Yellow']}Olá! Como posso ajudar? (digite 'ajuda' para ver os comandos disponíveis){self.colors['Reset']}")

        while True:
            try:
                user_input = input(f"{self.colors['LightGreen']}Você: {self.colors['Reset']}").strip()

                if user_input.lower() in ['sair', 'exit', 'quit']:
                    print(f"{self.colors['Blue']}{self.name}: {self.colors['Yellow']}Até logo!{self.colors['Reset']}")
                    break

                response = self.command_handler.process_command(user_input)
                print(f"{self.colors['Blue']}{self.name}: {self.colors['Yellow']}{response}{self.colors['Reset']}")

                self.database.save_interaction(user_input, response)

            except KeyboardInterrupt:
                print(f"\n{self.colors['Cyan']}Encerrando o assistente...{self.colors['Reset']}")
                break
            except Exception as e:
                print(f"{self.colors['Red']}Erro: {str(e)}{self.colors['Reset']}")
