import cohere as co

def gerar_resposta_cohere(pergunta):
    coh = co.Client('9QrgEmt9B8K4nXCKlHe5MDhni3LsiTpwo8ofBYpl')
    resposta = coh.generate(
        model='command-xlarge-nightly',
        prompt=pergunta,
        max_tokens=100
    )
    return resposta.generations[0].text.strip()
