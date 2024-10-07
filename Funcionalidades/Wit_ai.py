import requests

def reconhecer_voz_wit(audio):
    url = "https://api.wit.ai/speech"
    headers = {
        "Authorization": "Bearer RAB3ABA3DC45TLC64DRW4D76NV4WABOU",
        "Content-Type": "audio/wav"
    }

    # Converta o áudio para bytes
    audio_data = audio.get_wav_data()

    response = requests.post(url, headers=headers, data=audio_data)

    # Verifique se a resposta foi bem-sucedida
    if response.status_code == 200:
        print("Resposta da API:", response.text)  # Verifique a resposta
        try:
            # Obtenha o texto da resposta
            texto = response.json().get("text", "")
            return texto if texto else "Nenhuma entrada válida reconhecida."
        except requests.exceptions.JSONDecodeError:
            print("Erro de decodificação JSON.")
            return "Erro de decodificação JSON."
    else:
        print(f"Erro na API: {response.status_code} - {response.text}")
        return "Erro na API."
