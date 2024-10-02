import Funcionalidades.SinteseFala as fala
import os

def abrir_aplicativo(comando):
    if 'abrir navegador' in comando.lower():
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")  # Exemplo para Google Chrome
        fala.falar("Abrindo navegador.")
    elif 'abrir bloco de notas' in comando.lower():
        os.startfile("notepad.exe")
        fala.falar("Abrindo Bloco de Notas.")
    elif ('abrir lol' in comando.lower()) or ('abrir league of legends' in comando.lower()):
        os.startfile("C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Riot Games\\League of Legends")
        fala.falar("Abrindo League of Legends.")
