import speech_recognition as sr

def ouvir_comando():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Diga algo:")
        audio = reconhecedor.listen(fonte)
    try:
        comando = reconhecedor.recognize_google(audio, language="pt-BR")
        print("Você disse: " + comando)
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError:
        print("Erro ao conectar-se ao serviço de reconhecimento de voz.")
    return comando