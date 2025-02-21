import platform
import psutil
import os
from colorama import init, AnsiToWin32
init(wrap=False)

class SystemTools:
    def __init__(self):
        self.system = platform.system()

    def get_system_info(self):
        return f"""
Informações do Sistema:
Sistema Operacional: {platform.system()}
OS Version: {platform.version()}
Processador: {platform.processor()}
CPU Uso: {psutil.cpu_percent()}%
Memória Total: {round(psutil.virtual_memory().total / (1024.0 ** 3), 2)} GB
Memória Uso: {psutil.virtual_memory().percent}%
"""

    def get_memory_info(self):
        memory = psutil.virtual_memory()
        total = round(memory.total / (1024.0 ** 3), 2)
        used = round(memory.used / (1024.0 ** 3), 2)
        available = round(memory.available / (1024.0 ** 3), 2)
        return f"""
Uso de Memória: {used} GB
Total: {total} GB   
Disponível: {available} GB
Uso: {memory.percent}%
"""

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        return "Tela limpa!"
