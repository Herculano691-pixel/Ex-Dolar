import requests
from datetime import datetime

def cotar(data):
    data = datetime.strptime(data, "%m%d%Y").strftime("%m-%d-%Y")
    url = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    params = {
        "@dataInicial": f"'{data}'",
        "@dataFinalCotacao": f"'{data}'",
        "$format": "json",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    cotacoes = response.json()["value"]
    return cotacoes[0]["cotacaoCompra"] if cotacoes else None

print(cotar("08282024"))