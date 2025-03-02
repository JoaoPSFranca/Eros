from datetime import datetime
import re

import requests

from src.automation_tools import AutomationTools
from src.study_tools import StudyTools
from src.ai_engine import AIEngine
from src.learning_tools import LearningTools
from src.nlp_tools import NLPTools

class CommandHandler:
    def __init__(self, system_tools, web_tools, database):
        self.system_tools = system_tools
        self.web_tools = web_tools
        self.database = database
        self.automation = AutomationTools()
        self.study_tools = StudyTools()
        self.ai_engine = AIEngine()
        self.nlp_tools = NLPTools()
        self.learning_tools = LearningTools(self.ai_engine)

        self.commands = {
            "abrir": self.open_program_or_result,
            "ajuda": self.show_help,
            "atalho": self.add_shortcut,
            "baixar": self.download_content,
            "buscar_nota": self.search_notes,
            "clear": self.system_tools.clear_screen,
            "clima": self.get_weather,
            "historico": self.show_history,
            "hora": self.get_time,
            "lembrete": self.create_reminder,
            "lembretes": self.list_reminders,
            "ls": self.list_files,
            "memoria": self.system_tools.get_memory_info,
            "mkdir": self.create_folder,
            "mv": self.move_file,
            "nota": self.create_note,
            "notas": self.list_notes,
            "noticia": self.get_news,
            "organizar": self.organize_files,
            "pesquisar": self.web_search,
            "resumir": self.create_summary,
            "resumir_url": self.summarize_url,
            "sistema": self.system_tools.get_system_info,
            # Comandos de NLP e IA
            "sentimento": self.analyze_sentiment,
            "entidades": self.extract_entities,
            "treinar": self.train_ai,
            "feedback": self.save_feedback,
            "similaridade": self.check_similarity,
            "stats": self.model_stats,
            "aprender": self.apply_learning,
            "analise": self.analyze_learning
        }

    def show_help(self, *args):
        return """
Comandos disponíveis:
- abrir [programa]: Abre um programa
- ajuda: Mostra esta mensagem
- atalho [nome] [caminho]: Cria um atalho para um arquivo ou programa
- buscar_nota [nome]: Busca uma nota existente
- clear: Limpa a tela 
- historico: Mostra histórico de comandos
- hora: Mostra a hora atual
- lembrete [data_hora] [mensagem]: Cria um lembrete
- lembretes <todos>: Mostra os lembretes ativos (ou todos) 
- ls <caminho>: Lista os arquivos de um local
- memoria: Mostra uso de memória
- mkdir [nome]: Cria uma pasta no local
- mv [origem] [destino]: Move um arquivo ou pasta de local
- nota [titulo] [conteudo] <#tag>: Cria uma nota com uma tag
- notas <tag>: Mostra todas as notas ou filtra elas por tag 
- organizar <caminho>: Organiza os arquivos de um local
- pesquisar [termo]: Pesquisa na web
- resumir [texto]: Resume um texto
- sistema: Mostra informações do sistema

Comandos de NLP e IA:
- sentimento [texto]: Analisa o sentimento de um texto
- entidades [texto]: Extrai entidades de um texto
- treinar [tag] [padrões] [respostas]: Adiciona dados de treinamento à IA
- feedback [pontuação] [resposta_melhor]: Fornece feedback sobre a última resposta
- similaridade [texto1] [texto2]: Calcula a similaridade entre dois textos
- stats: Exibe estatísticas do modelo de IA
- aprender [max]: Aplica sugestões de aprendizado (opcional: número máximo)
- analise: Analisa dados de aprendizado

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

    def open_program_or_result(self, *args):
        if not args:
            return "Por favor, especifique o programa para abrir ou o número do resultado."

        if args[0].isdigit():
            return self.web_tools.open_result(args[0])

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

    def create_note(self, *args):
        if len(args) < 2:
            return "Use: nota [título] [conteúdo] #tag1 #tag2"

        content = " ".join(args[1:])
        tags = re.findall(r'#(\w+)', content)
        content = re.sub(r'#\w+', '', content).strip()

        return self.study_tools.create_note(args[0], content, tags)

    def list_notes(self, *args):
        tag = args[0] if args else None
        return self.study_tools.list_notes(tag)

    def search_notes(self, *args):
        if not args:
            return "Por favor, especifique o termo de busca."
        query = " ".join(args)
        return self.study_tools.search_notes(query)

    def create_reminder(self, *args):
        if len(args) < 2:
            return "Use: lembrete [data_hora] [mensagem]"
        date_time = args[0]
        message = " ".join(args[1:])
        return self.study_tools.create_reminder(message, date_time)

    def list_reminders(self, *args):
        show_completed = "todos" in args
        return self.study_tools.list_reminders(show_completed)

    def create_summary(self, *args):
        if not args:
            return "Por favor, forneça o texto para resumir."
        text = " ".join(args)
        return self.study_tools.create_summary(text)

    def analyze_sentiment(self, *args):
        if not args:
            return "Por favor, forneça um texto para análise de sentimento."
        text = " ".join(args)
        sentiment = self.nlp_tools.analyze_sentiment(text)

        emojis = {
            "positivo": "😊",
            "negativo": "😞",
            "neutro": "😐"
        }

        return f"Sentimento: {sentiment} {emojis.get(sentiment, '')}"

    def extract_entities(self, *args):
        if not args:
            return "Por favor, forneça um texto para extração de entidades."
        text = " ".join(args)
        entities = self.nlp_tools.extract_entities(text)

        if not entities:
            return "Nenhuma entidade encontrada no texto."

        result = "Entidades encontradas:\n"
        for entity_type, values in entities.items():
            result += f"- {entity_type}: {', '.join(values)}\n"

        return result

    def check_similarity(self, *args):
        if len(args) < 2:
            return "Use: similaridade [texto1] [texto2]"

        mid_point = len(args) // 2
        text1 = " ".join(args[:mid_point])
        text2 = " ".join(args[mid_point:])

        similarity = self.nlp_tools.text_similarity(text1, text2)
        percentage = similarity * 100

        return f"Similaridade: {percentage:.2f}% entre os textos"

    def train_ai(self, *args):
        if len(args) < 3:
            return "Use: treinar [tag] [padrões separados por vírgula] [respostas separadas por vírgula]"

        tag = args[0]

        full_args = " ".join(args[1:])
        patterns_end = full_args.rfind(']')

        if patterns_end == -1:
            return "Formato inválido. Use: treinar [tag] [padrão1, padrão2] [resposta1, resposta2]"

        patterns_str = full_args[:patterns_end + 1]
        responses_str = full_args[patterns_end + 1:]

        try:
            patterns = [p.strip() for p in patterns_str.strip('[]').split(',')]
            responses = [r.strip() for r in responses_str.strip('[]').split(',')]

            if not patterns or not responses:
                return "Padrões e respostas não podem estar vazios."

            if self.ai_engine.add_training_data(tag, patterns, responses):
                return f"IA treinada com sucesso! Adicionados {len(patterns)} padrões e {len(responses)} respostas para a tag '{tag}'."
            else:
                return "Erro ao treinar IA. Verifique o formato dos dados."
        except Exception as e:
            return f"Erro ao processar dados de treinamento: {e}"

    def save_feedback(self, *args):
        if not args:
            return "Use: feedback [pontuação 1-5] [resposta_melhor]"

        history = self.database.get_history()
        if not history:
            return "Nenhum histórico de conversa encontrado para dar feedback."

        last_input = history[-1][1] if history else ""
        last_output = "Resposta não registrada"

        try:
            score = int(args[0])
            if score < 1 or score > 5:
                return "A pontuação deve ser entre 1 e 5."

            better_response = " ".join(args[1:]) if len(args) > 1 else None

            self.learning_tools.save_feedback(last_input, last_output, score, better_response)

            if score >= 4:
                return "Obrigado pelo feedback positivo! 😊"
            elif better_response:
                return "Obrigado pelo feedback. Sua sugestão de resposta foi registrada e será considerada para melhorias futuras."
            else:
                return "Obrigado pelo feedback. Tentaremos melhorar nossas respostas."

        except ValueError:
            return "A pontuação deve ser um número entre 1 e 5."

    def model_stats(self, *args):
        return self.ai_engine.get_model_stats()

    def apply_learning(self, *args):
        max_suggestions = int(args[0]) if args and args[0].isdigit() else 5
        return self.learning_tools.apply_suggested_intents(max_suggestions)

    def analyze_learning(self, *args):
        return self.learning_tools.analyze_learning_data()

    def summarize_url(self, *args):
        if not args:
            return "Por favor, forneça a URL para resumir."
        url = args[0]
        return self.web_tools.summarize_url(url)

    def download_content(self, *args):
        if len(args) < 2:
            return "Uso: baixar [url] [nome_arquivo]"

        url = args[0]
        filename = args[1]

        try:
            import requests
            response = requests.get(url, stream=True)
            with open(filename, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return f"Arquivo baixado com sucesso: {filename}"
        except Exception as e:
            return f"Erro ao baixar arquivo: {e}"

    def get_weather(self, *args):
        if not args:
            return "Por favor, especifique uma cidade para consulta de clima."

        city = " ".join(args)
        try:
            api_key = "bbaad92c57b38b67517996eb56182b15"
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br"

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind = data['wind']['speed']

                return f"Clima em {city}:\n- Temperatura: {temp}°C\n- Condição: {desc}\n- Umidade: {humidity}%\n- Vento: {wind} m/s"
            else:
                return f"Erro ao obter clima: {data.get('message', 'Cidade não encontrada')}"
        except Exception as e:
            return f"Erro ao consultar clima: {e}"

    def get_news(self, *args):
        query = " ".join(args) if args else "brasil"

        try:
            api_key = "0e7eeb9c820f4910bac6ac25118e9dbe"

            url = f"https://newsapi.org/v2/top-headlines?country=br&apiKey={api_key}"

            response = requests.get(url)
            data = response.json()

            if response.status_code == 200 and data.get('articles'):
                news_list = data['articles'][:5]

                result = f"Notícias sobre '{query}':\n\n"
                for i, news in enumerate(news_list, 1):
                    result += f"{i}. {news['title']}\n"
                    result += f"   Fonte: {news['source']['name']}\n"
                    result += f"   Link: {news['url']}\n\n"

                return result
            else:
                return f"Erro ao obter notícias: {data.get('message', 'Nenhuma notícia encontrada')}"
        except Exception as e:
            return f"Erro ao consultar notícias: {e}"

    def process_command(self, command):
        if not command:
            return "Como posso ajudar?"

        self.database.save_interaction(command, None)

        self.nlp_tools.update_context(command)

        parts = command.split()
        main_command = parts[0].lower()
        args = parts[1:]

        if main_command in self.commands:
            response = self.commands[main_command](*args)

            if response:
                self.learning_tools.save_conversation(command, response)
                self.database.save_interaction(command, response)

            return response

        ai_response = self.ai_engine.get_response(command)
        if ai_response:
            self.learning_tools.save_conversation(command, ai_response)
            return ai_response

        for cmd_name in self.commands:
            similarity = self.nlp_tools.text_similarity(command, cmd_name)
            if similarity > 0.7:
                suggested_cmd = f"Você quis dizer o comando '{cmd_name}'? Tente: '{cmd_name} {' '.join(args)}'"
                return suggested_cmd

        default_response = "Comando não reconhecido. Digite 'ajuda' para ver os comandos disponíveis."
        self.learning_tools.save_conversation(command, default_response)
        return default_response
