import webbrowser
import requests
from bs4 import BeautifulSoup

class WebTools:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.search_cache = {}
        self.last_results = []

    def web_search(self, search_term):
        try:
            results = self.search_online(search_term)
            if results:
                self.last_results = results
                summary = "\n".join([f"{i + 1}. {r['title']} - {r['url'][:60]}..." for i, r in enumerate(results[:5])])
                return f"Resultados para '{search_term}':\n{summary}\n\nDigite 'abrir 1' para abrir o primeiro resultado."
            else:
                url = f"https://www.google.com/search?q={search_term}"
                webbrowser.open(url)
                return f"Pesquisando por '{search_term}' no navegador."
        except Exception as e:
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            return f"Erro na pesquisa direta: {e}\nAbrindo navegador para pesquisa."

    def search_online(self, search_term):
        if search_term in self.search_cache:
            return self.search_cache[search_term]

        try:
            url = f"https://lite.duckduckgo.com/lite/?q={search_term}"
            response = self.session.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')

            results = []
            links = soup.find_all('a', attrs={'rel': 'nofollow'})

            for link in links:
                if not link.text or link.text.isspace():
                    continue

                url = link.get('href')
                if not url or not url.startswith(('http://', 'https://')):
                    continue

                results.append({
                    "title": link.text.strip(),
                    "url": url,
                    "snippet": link.find_next('td').text.strip() if link.find_next('td') else ""
                })

                if len(results) >= 10:
                    break

            self.search_cache[search_term] = results
            return results
        except Exception as e:
            print(f"Erro na pesquisa online: {e}")
            return []

    def get_page_content(self, url):
        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            for script in soup(["script", "style", "meta", "noscript"]):
                script.extract()

            text = soup.get_text(separator=' ', strip=True)

            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return text[:5000] + "..." if len(text) > 5000 else text
        except Exception as e:
            return f"Erro ao acessar a página: {e}"

    def summarize_url(self, url):
        try:
            content = self.get_page_content(url)
            paragraphs = content.split('\n')
            meaningful_paragraphs = [p for p in paragraphs if len(p.split()) > 15]

            if not meaningful_paragraphs:
                return f"Não foi possível extrair conteúdo significativo de {url}"

            summary = "\n\n".join(meaningful_paragraphs[:3])
            return f"Resumo de {url}:\n\n{summary}"
        except Exception as e:
            return f"Erro ao resumir URL: {e}"

    def open_result(self, index):
        try:
            index = int(index) - 1  # Converte para índice base-0
            if 0 <= index < len(self.last_results):
                url = self.last_results[index]["url"]
                webbrowser.open(url)
                return f"Abrindo: {self.last_results[index]['title']}"
            else:
                return "Índice de resultado inválido."
        except Exception as e:
            return f"Erro ao abrir resultado: {e}"