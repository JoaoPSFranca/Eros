import speech_recognition as sr

def ouvir_comando():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Diga algo:")
        audio = reconhecedor.listen(fonte)
    return audio
