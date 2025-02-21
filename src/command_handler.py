from datetime import datetime

from src.automation_tools import AutomationTools


class CommandHandler:
    def __init__(self, system_tools, web_tools, database):
        self.system_tools = system_tools
        self.web_tools = web_tools
        self.database = database
        self.automation = AutomationTools()
        self.commands = {
            "abrir": self.open_program,
            "ajuda": self.show_help,
            "ls": self.list_files,
            "atalho": self.add_shortcut,
            "historico": self.show_history,
            "hora": self.get_time,
            "clear": self.system_tools.clear_screen,
            "memoria": self.system_tools.get_memory_info,
            "mv": self.move_file,
            "organizar": self.organize_files,
            "mkdir": self.create_folder,
            "pesquisar": self.web_search,
            "sistema": self.system_tools.get_system_info
        }


    def show_help(self, *args):
        return """
Comandos disponíveis:
- abrir [programa]: Abre um programa
- ajuda: Mostra esta mensagem
- ls <caminho>: Lista os arquivos de um local
- atalho [nome] [caminho]: Cria um atalho para um arquivo ou programa
- historico: Mostra histórico de comandos
- hora: Mostra a hora atual
- clear: Limpa a tela 
- memoria: Mostra uso de memória
- mv [origem] [destino]: Move um arquivo ou pasta de local
- organizar <caminho>: Organiza os arquivos de um local
- mkdir [nome]: Cria uma pasta no local
- pesquisar [termo]: Pesquisa na web
- sistema: Mostra informações do sistema
- sair: Encerra o assistente
"""

    def get_time(self, *args):
        return f"Agora são {datetime.now().strftime('%H:%M:%S')} de {datetime.now().strftime('%d/%m/%Y')}"

    def web_search(self, *args):
        if not args:
            return "Por favor, forneça um termo para pesquisa."
        search_term = " ".join(args)
        return self.web_tools.web_search(search_term)

    def show_history(self, *args):
        history = self.database.get_history()
        if not history:
            return "Nenhum histórico encontrado."

        result = "Últimos 5 comandos:\n"
        for timestamp, input_text in history:
            dt = datetime.fromisoformat(timestamp)
            result += f"{dt.strftime('%H:%M:%S')}: {input_text}\n"
        return result

    def open_program(self, *args):
        if not args:
            return "Por favor, especifique o programa para abrir."
        program_name = " ".join(args)
        return self.automation.open_program(program_name)

    def add_shortcut(self, *args):
        if len(args) < 2:
            return "Use: atalho [nome] [caminho]"
        name = args[0]
        path = " ".join(args[1:])
        return self.automation.add_shortcut(name, path)

    def list_files(self, *args):
        path = " ".join(args) if args else "."
        return self.automation.list_files(path)

    def create_folder(self, *args):
        if not args:
            return "Por favor, especifique o nome da pasta."
        folder_name = " ".join(args)
        return self.automation.create_folder(folder_name)

    def move_file(self, *args):
        if len(args) < 2:
            return "Use: mover [origem] [destino]"
        source = args[0]
        destination = " ".join(args[1:])
        return self.automation.move_file(source, destination)

    def organize_files(self, *args):
        path = " ".join(args) if args else "."
        return self.automation.organize_files(path)

    def process_command(self, command):
        if not command:
            return "Como posso ajudar?"

        parts = command.split()
        main_command = parts[0].lower()
        args = parts[1:]

        if main_command in self.commands:
            return self.commands[main_command](*args)
        elif "olá" in command or "oi" in command:
            return f"Olá! Como posso ajudar? (digite 'ajuda' para ver os comandos disponíveis)"
        else:
            return "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."
