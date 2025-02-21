from datetime import datetime

class CommandHandler:
    def __init__(self, system_tools, web_tools, database):
        self.system_tools = system_tools
        self.web_tools = web_tools
        self.database = database

        self.commands = {
            "ajuda": self.show_help,
            "sistema": self.system_tools.get_system_info,
            "hora": self.get_time,
            "pesquisar": self.web_search,
            "limpar": self.system_tools.clear_screen,
            "memoria": self.system_tools.get_memory_info,
            "historico": self.show_history
        }

    def show_help(self, *args):
        return """
Comandos disponíveis:
- ajuda: Mostra esta mensagem
- hora: Mostra a hora atual
- sistema: Mostra informações do sistema
- pesquisar [termo]: Pesquisa na web
- limpar: Limpa a tela (necessita de alterações)
- memoria: Mostra uso de memória
- historico: Mostra histórico de comandos
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

    def process_command(self, command):
        if not command:
            return "Como posso ajudar?"

        parts = command.lower().split()
        main_command = parts[0]
        args = parts[1:]

        if main_command in self.commands:
            return self.commands[main_command](*args)
        elif "olá" in command or "oi" in command:
            return f"Olá! Como posso ajudar? (digite 'ajuda' para ver os comandos disponíveis)"
        else:
            return "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."
