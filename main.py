import Funcionalidades.OuvirComando as Ouvir
import Funcionalidades.SinteseFala as Falar
import Funcionalidades.AbrirApps as Apps
import Funcionalidades.WebSeacrh as Pesquisa

if __name__ == "__main__":
    comando = Ouvir.ouvir_comando()
    Falar.falar(f"Você disse: {comando}")
    Apps.abrir_aplicativo(comando)
    Pesquisa.pesquisar_na_internet(comando)
