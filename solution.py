import requests
from datetime import datetime, timedelta

def cotar():
    cotacoes_compra = []
    data_atual = datetime.now()
    data_inicial_busca = data_atual - timedelta(days=500)
    str_inicial = data_inicial_busca.strftime("%m-%d-%Y")
    str_final = data_atual.strftime("%m-%d-%Y")

    url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial='{str_inicial}',dataFinalCotacao='{str_final}')"
    params = {"$format": "json"}

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        dados_api = response.json().get("value", [])

        mapa_cotacoes = {}
        for item in dados_api:
            data_valor = item["dataHoraCotacao"].split(" ")[0]
            mapa_cotacoes[data_valor] = item["cotacaoCompra"]

        ultimo_valor_conhecido = None
        temp_lista = []

        for i in range(364, -1, -1):
            data_alvo = data_atual - timedelta(days=i)
            chave_data = data_alvo.strftime("%Y-%m-%d")

            valor = mapa_cotacoes.get(chave_data)
            if valor is not None:
                ultimo_valor_conhecido = valor

            temp_lista.append(ultimo_valor_conhecido)

        cotacoes_compra = temp_lista[::-1]

    except Exception:
        return [None] * 365

    return cotacoes_compra

if __name__ == "__main__":
    resultado = cotar()
    print(resultado)
    print(f"\nTotal de valores: {len(resultado)}")
