import os
import json
from datetime import datetime
import re

class StudyTools:
    def __init__(self):
        self.notes_dir = "data/notes"
        self.reminders_file = "data/reminders.json"
        self.setup_storage()

    def setup_storage(self):
        try:
            os.makedirs(self.notes_dir, exist_ok=True)
            if not os.path.exists(self.reminders_file):
                with open(self.reminders_file, 'w', encoding='utf-8') as f:
                    json.dump([], f)
        except Exception as e:
            print(f"Erro ao configurar armazenamento: {e}")

    def create_note(self, title, content, tags=None):
        try:
            timestamp = datetime.now().strftime("%d%m%Y_%H%M%S")
            filename = f"{timestamp}_{title.replace(' ', '_')}.md"
            filepath = os.path.join(self.notes_dir, filename)

            note_content = f"""# {title}
Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Tags: {', '.join(tags) if tags else 'Sem tags'}

{content}
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(note_content)

            return f"Nota '{title}' criada com sucesso!"
        except Exception as e:
            return f"Erro ao criar nota: {e}"

    def list_notes(self, tag=None):
        try:
            notes = []
            for filename in os.listdir(self.notes_dir):
                if filename.endswith('.md'):
                    with open(os.path.join(self.notes_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if tag:
                            if f"Tags: {tag}" in content:
                                notes.append(filename.split('_', 1)[1].replace('_', ' ')[:-3])
                        else:
                            notes.append(filename.split('_', 1)[1].replace('_', ' ')[:-3])

            if not notes:
                return "Nenhuma nota encontrada."

            return "\n" + "\n".join([f"📝 {note}" for note in sorted(notes)])
        except Exception as e:
            return f"Erro ao listar notas: {e}"

    def search_notes(self, query):
        try:
            results = []
            for filename in os.listdir(self.notes_dir):
                if filename.endswith('.md'):
                    with open(os.path.join(self.notes_dir, filename), 'r', encoding='utf-8') as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            title = filename.split('_', 1)[1].replace('_', ' ')[:-3]
                            results.append(f"📝 {title}")

            if not results:
                return "Nenhuma nota encontrada com esse termo."

            return "\n".join(results)
        except Exception as e:
            return f"Erro ao pesquisar notas: {e}"

    def create_reminder(self, message, date_time):
        try:
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                reminders = json.load(f)

            reminders.append({
                "message": message,
                "datetime": date_time,
                "created": datetime.now().isoformat(),
                "completed": False
            })

            with open(self.reminders_file, 'w', encoding='utf-8') as f:
                json.dump(reminders, f, indent=4)

            return f"Lembrete criado para {date_time}"
        except Exception as e:
            return f"Erro ao criar lembrete: {e}"

    def list_reminders(self, show_completed=False):
        try:
            with open(self.reminders_file, 'r', encoding='utf-8') as f:
                reminders = json.load(f)

            active_reminders = [r for r in reminders if not r['completed'] or show_completed]

            if not active_reminders:
                return "Nenhum lembrete encontrado."

            return "\n".join([
                f"{'✓' if r['completed'] else '⏰'} {r['message']} ({r['datetime']})"
                for r in active_reminders
            ])
        except Exception as e:
            return f"Erro ao listar lembretes: {e}"

    def create_summary(self, text):
        try:
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]

            if len(sentences) <= 3:
                summary = sentences
            else:
                summary = [sentences[0]]  # Primeira sentença
                summary.append(sentences[len(sentences) // 2])  # Sentença do meio
                summary.append(sentences[-1])  # Última sentença

            return "\n".join(summary)
        except Exception as e:
            return f"Erro ao criar resumo: {e}"