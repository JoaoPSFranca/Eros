import Funcionalidades.OuvirComando as Ouvir
import Funcionalidades.SinteseFala as Falar
import Funcionalidades.AbrirApps as Apps
import Funcionalidades.WebSeacrh as Pesquisa
import Funcionalidades.Wit_ai as Wit
import Funcionalidades.Cohere as Cohere

if __name__ == "__main__":
    # comando = Ouvir.ouvir_comando()
    # Falar.falar(f"Você disse: {comando}")
    # Apps.abrir_aplicativo(comando)
    # Pesquisa.pesquisar_na_internet(comando)
    # resposta = Hug.consultar_huggingchat("Qual o tamanho da lua?")
    # Falar.falar(resposta)
    # print(resposta)
    audio = Ouvir.ouvir_comando()
    texto_reconhecido = Wit.reconhecer_voz_wit(audio)
    print("Texto reconhecido:", texto_reconhecido)
    if texto_reconhecido.strip():
        resposta = Cohere.gerar_resposta_cohere(texto_reconhecido)
        Falar.falar(resposta)
    else:
        print("Nenhuma entrada válida reconhecida.")
