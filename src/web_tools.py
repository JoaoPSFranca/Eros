import webbrowser
import requests
from bs4 import BeautifulSoup

class WebTools:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def web_search(self, search_term):
        try:
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            return f"Pesquisando por '{search_term}' no navegador."
        except Exception as e:
            return f"Erro ao realizar pesquisa: {e}"

    def get_page_content(self, url):
        try:
            response = self.session.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.get_text()
        except Exception as e:
            return f"Erro ao acessar a página: {e}"
