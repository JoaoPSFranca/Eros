import Funcionalidades.SinteseFala as Fala
import webbrowser

def pesquisar_na_internet(comando):
    if 'pesquisar' in comando.lower():
        termo = comando.lower().replace('pesquisar', '').strip().replace(' ', '+')
        url = f"https://www.google.com/search?q={termo}"
        webbrowser.open(url)
        Fala.falar(f"Pesquisando por {termo}.")