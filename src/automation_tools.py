import os
import subprocess
import json
import shutil
import platform


class AutomationTools:
    def __init__(self):
        self.system = platform.system()
        self.config_file = "config/shortcuts.json"
        self.shortcuts = self.load_shortcuts()

    def load_shortcuts(self):
        try:
            os.makedirs('config', exist_ok=True)
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Erro ao carregar atalhos: {e}")
            return {}

    def save_shortcuts(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.shortcuts, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar atalhos: {e}")

    def add_shortcut(self, name, path):
        self.shortcuts[name.lower()] = path
        self.save_shortcuts()
        return f"Atalho '{name}' adicionado com sucesso!"

    def open_program(self, program_name):
        try:
            program_name = program_name.lower()
            if program_name in self.shortcuts:
                path = self.shortcuts[program_name]
            else:
                return f"Atalho não encontrado para '{program_name}'"

            if self.system == "Windows":
                os.startfile(path)
            else:
                subprocess.Popen(['xdg-open', path])
            return f"Abrindo {program_name}..."
        except Exception as e:
            return f"Erro ao abrir programa: {e}"

    def list_files(self, path="."):
        try:
            files = os.listdir(path)
            directories = sorted([f for f in files if os.path.isdir(os.path.join(path, f))])
            regular_files = sorted([f for f in files if os.path.isfile(os.path.join(path, f))])
            sorted_files = directories + regular_files
            return "\n" + "\n".join([
                f"\t📁 {f}" if os.path.isdir(os.path.join(path, f)) else f"\t📄 {f}"
                for f in sorted_files
            ])
        except Exception as e:
            return f"Erro ao listar arquivos: {e}"

    def create_folder(self, folder_name):
        try:
            os.makedirs(folder_name, exist_ok=True)
            return f"Pasta '{folder_name}' criada com sucesso!"
        except Exception as e:
            return f"Erro ao criar pasta: {e}"

    def move_file(self, source, destination):
        try:
            shutil.move(source, destination)
            return f"Arquivo movido de '{source}' para '{destination}'"
        except Exception as e:
            return f"Erro ao mover arquivo: {e}"

    def organize_files(self, path="."):
        try:
            files = os.listdir(path)
            organized = {}

            categories = {
                'imagens': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.wbmp','.svg', '.psd', '.tiff', '.map', '.pdb', '.ico', '.sgi', '.rgb', '.hdr', '.jfif', '.avif', '.dds', '.jbg', '.exr', '.pcx'],
                'compressoes': ['.zip', '.tar.gz', '.tar.xz', '.rar', '.7z', '.jar'],
                'documentos': ['.pdf', '.doc', '.docm', '.docx', '.dotx', '.dot', '.txt', '.xls', '.xlsx', '.rtf', '.odt', '.csv'],
                'apresentacoes': ['.ppt', '.pptx', '.odp', '.ppsx', '.pps', '.pptm', '.potm', '.ppsm', '.potx', '.pot'],
                'musicas': ['.mp3', '.wav', '.flac', '.aac'],
                'videos': ['.mp4', '.mkv', '.avi', '.mov'],
                'codigos': ['.py', '.java', '.js', '.html', '.css', '.c', '.cpp', '.cs', '.ts'],
                'executaveis': ['.rpm', '.exe', '.appimage'],
                'bibliotecas': ['.dll'],
                'sem_extensao': []
            }

            for file in files:
                if os.path.isfile(os.path.join(path, file)):
                    ext = os.path.splitext(file)[1].lower()
                    categorized = False
                    for category, exts in categories.items():
                        if ext in exts:
                            organized.setdefault(category, []).append(file)
                            categorized = True
                            break
                    if not categorized:
                        organized.setdefault('sem_extensao', []).append(file)

            for category, file_list in organized.items():
                folder_path = os.path.join(path, category)
                os.makedirs(folder_path, exist_ok=True)
                for file in file_list:
                    source = os.path.join(path, file)
                    destination = os.path.join(folder_path, file)
                    shutil.move(source, destination)
            return "Arquivos organizados com sucesso!"
        except Exception as e:
            return f"Erro ao organizar arquivos: {e}"
