from src.core import Assistant

def main():
    print('\033[36m' + "Iniciando Assistente Virtual..." + '\033[0;0m')
    assistant = Assistant()
    assistant.start()

if __name__ == "__main__":
    main()
