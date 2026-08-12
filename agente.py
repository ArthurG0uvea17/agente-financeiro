"""
Agente com function calling: o modelo decide sozinho quando chamar
cada ferramenta, com base na pergunta do usuário.
"""

import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from ferramentas import calcular_juros_compostos, converter_moeda, buscar_clima

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

# Descreve para o modelo quais ferramentas existem, o que fazem e quais parâmetros esperam.
# É a partir dessa descrição que o modelo decide, sozinho, qual chamar.
FERRAMENTAS_DISPONIVEIS = [
    {
        "type": "function",
        "function": {
            "name": "calcular_juros_compostos",
            "description": "Calcula o montante final de um investimento com juros compostos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "capital": {"type": "number", "description": "Valor inicial investido"},
                    "taxa_anual": {"type": "number", "description": "Taxa de juros anual em porcentagem, ex: 10 para 10%"},
                    "meses": {"type": "integer", "description": "Número de meses do investimento"}
                },
                "required": ["capital", "taxa_anual", "meses"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "converter_moeda",
            "description": "Converte um valor de uma moeda para outra usando a cotação atual.",
            "parameters": {
                "type": "object",
                "properties": {
                    "valor": {"type": "number", "description": "Valor a ser convertido"},
                    "moeda_origem": {"type": "string", "description": "Código da moeda de origem, ex: BRL, USD, EUR"},
                    "moeda_destino": {"type": "string", "description": "Código da moeda de destino, ex: BRL, USD, EUR"}
                },
                "required": ["valor", "moeda_origem", "moeda_destino"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_clima",
            "description": "Busca a temperatura atual de uma cidade, dado seu nome e coordenadas geográficas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "cidade": {"type": "string", "description": "Nome da cidade"},
                    "latitude": {"type": "number", "description": "Latitude da cidade"},
                    "longitude": {"type": "number", "description": "Longitude da cidade"}
                },
                "required": ["cidade", "latitude", "longitude"]
            }
        }
    }
]

# Mapeia o nome da função (como o modelo vai chamá-la) para a função Python real
FUNCOES_PYTHON = {
    "calcular_juros_compostos": calcular_juros_compostos,
    "converter_moeda": converter_moeda,
    "buscar_clima": buscar_clima
}


def perguntar_ao_agente(pergunta_usuario: str) -> str:
    mensagens = [{"role": "user", "content": pergunta_usuario}]

    resposta = client.chat.completions.create(
        model=MODEL,
        messages=mensagens,
        tools=FERRAMENTAS_DISPONIVEIS
    )

    mensagem = resposta.choices[0].message

    # Se o modelo não pediu nenhuma ferramenta, a resposta já está pronta
    if not mensagem.tool_calls:
        return mensagem.content

    # O modelo decidiu chamar uma ou mais ferramentas: executamos de verdade
    mensagens.append(mensagem)

    for chamada in mensagem.tool_calls:
        nome_funcao = chamada.function.name
        argumentos = json.loads(chamada.function.arguments)

        print(f"  [agente decidiu chamar: {nome_funcao}({argumentos})]")

        resultado = FUNCOES_PYTHON[nome_funcao](**argumentos)

        mensagens.append({
            "role": "tool",
            "tool_call_id": chamada.id,
            "content": json.dumps(resultado)
        })

    # Manda o resultado da ferramenta de volta para o modelo formular a resposta final
    resposta_final = client.chat.completions.create(
        model=MODEL,
        messages=mensagens,
        tools=FERRAMENTAS_DISPONIVEIS
    )

    return resposta_final.choices[0].message.content


if __name__ == "__main__":
    print("=== Agente Financeiro (function calling) ===")
    print("Pergunte sobre câmbio, juros compostos ou clima. Digite 'sair' para encerrar.\n")

    while True:
        pergunta = input("Você: ")
        if pergunta.lower() == "sair":
            break

        resposta = perguntar_ao_agente(pergunta)
        print(f"Agente: {resposta}\n")
