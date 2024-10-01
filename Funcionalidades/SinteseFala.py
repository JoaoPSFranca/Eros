import pyttsx3

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()
