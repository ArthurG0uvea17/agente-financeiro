"""Ferramentas reais que o agente pode decidir chamar."""

import requests


def calcular_juros_compostos(capital: float, taxa_anual: float, meses: int) -> dict:
    """Calcula o montante final de um investimento com juros compostos."""
    taxa_mensal = (1 + taxa_anual / 100) ** (1 / 12) - 1
    montante = capital * (1 + taxa_mensal) ** meses
    juros_ganhos = montante - capital

    return {
        "capital_inicial": round(capital, 2),
        "montante_final": round(montante, 2),
        "juros_ganhos": round(juros_ganhos, 2),
        "meses": meses,
        "taxa_anual_pct": taxa_anual
    }


def converter_moeda(valor: float, moeda_origem: str, moeda_destino: str) -> dict:
    """Converte um valor entre moedas usando cotação atual (API Frankfurter, sem necessidade de chave)."""
    url = f"https://api.frankfurter.dev/v1/latest?base={moeda_origem.upper()}&symbols={moeda_destino.upper()}"
    resposta = requests.get(url, timeout=10)
    dados = resposta.json()

    taxa = dados["rates"][moeda_destino.upper()]
    valor_convertido = valor * taxa

    return {
        "valor_original": valor,
        "moeda_origem": moeda_origem.upper(),
        "moeda_destino": moeda_destino.upper(),
        "taxa_cambio": taxa,
        "valor_convertido": round(valor_convertido, 2)
    }


def buscar_clima(cidade: str, latitude: float, longitude: float) -> dict:
    """Busca a temperatura atual de uma cidade usando coordenadas (API Open-Meteo, sem necessidade de chave)."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
    resposta = requests.get(url, timeout=10)
    dados = resposta.json()

    return {
        "cidade": cidade,
        "temperatura_celsius": dados["current"]["temperature_2m"]
    }
