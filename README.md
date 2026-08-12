# Agente Financeiro (Function Calling)

Agente conversacional que decide autonomamente quando executar ferramentas externas reais (cálculo financeiro, conversão de moeda, consulta de clima) para responder perguntas do usuário em linguagem natural.

## O que é function calling

Diferente de um assistente que apenas gera texto com base em conhecimento genérico, este agente recebe uma lista de ferramentas disponíveis e, a cada pergunta, decide sozinho: (1) se alguma ferramenta é necessária, (2) qual delas, e (3) com quais parâmetros chamá-la — extraídos diretamente da linguagem natural do usuário. O resultado real da execução é devolvido ao modelo, que então formula a resposta final.

## Exemplo de uso

```
Você: Quanto rende R$ 5000 em 12 meses a 10% ao ano?
  [agente decidiu chamar: calcular_juros_compostos({'capital': 5000, 'taxa_anual': 10, 'meses': 12})]
Agente: Um investimento de R$ 5.000,00 em 12 meses a uma taxa de 10% ao ano renderá
um montante final de R$ 5.500,00. Isso significa que os juros ganhos foram de R$ 500,00.

Você: Quanto é 100 dólares em reais?
  [agente decidiu chamar: converter_moeda({'valor': 100, 'moeda_origem': 'USD', 'moeda_destino': 'BRL'})]
Agente: 100 dólares equivalem a 515,57 reais, com a taxa de câmbio atual de 5,1557.

Você: Qual a temperatura em Lisboa? A latitude é 38.7 e longitude -9.1
  [agente decidiu chamar: buscar_clima({'cidade': 'Lisboa', 'latitude': 38.7, 'longitude': -9.1})]
Agente: A temperatura atual em Lisboa é de 24,6 °C.
```

## Ferramentas disponíveis

| Ferramenta | O que faz | Fonte dos dados |
|---|---|---|
| `calcular_juros_compostos` | Calcula o montante final de um investimento | Cálculo local, sem API externa |
| `converter_moeda` | Converte valores entre moedas pela cotação atual | API Frankfurter (gratuita, sem chave) |
| `buscar_clima` | Retorna a temperatura atual de uma cidade | API Open-Meteo (gratuita, sem chave) |

## Arquitetura

```
[Usuário digita uma pergunta]
        |
        v
[agente.py envia a pergunta + lista de ferramentas para a API da OpenAI]
        |
        v
[Modelo decide: responder direto, ou chamar uma ferramenta?]
        |
        +-- Se chamar ferramenta:
        |     [ferramentas.py executa a função real: cálculo, API de câmbio ou clima]
        |     [resultado volta para o modelo]
        |     [modelo formula a resposta final com base no resultado real]
        |
        v
[Resposta em linguagem natural exibida ao usuário]
```

## Tecnologias utilizadas

- **Python** - linguagem principal
- **OpenAI API** - modelo de linguagem e mecanismo de function calling (`gpt-4o-mini`)
- **requests** - chamadas às APIs externas de câmbio e clima

## Decisões técnicas

**Por que APIs sem necessidade de chave (Frankfurter, Open-Meteo)?**
Reduz a fricção para rodar o projeto: além da chave da OpenAI (já necessária), nenhuma outra credencial precisa ser configurada. Ambas são APIs públicas, estáveis e gratuitas, adequadas para um projeto de portfólio.

**Por que não usar um framework de agentes (LangChain, LlamaIndex)?**
Implementar o loop de function calling diretamente com o SDK da OpenAI deixa explícito cada etapa do processo (definição das ferramentas, decisão do modelo, execução real, retorno do resultado), o que é mais didático para demonstrar o entendimento do mecanismo. Frameworks de agentes adicionam abstrações úteis em projetos maiores, mas não são necessários na escala deste projeto.

**Por que terminal em vez de interface web?**
Este projeto foca em demonstrar o mecanismo de function calling em si. O [RAG Document Assistant](https://github.com/ArthurG0uvea17/Rag-document-assistant), outro projeto deste mesmo portfólio, já cobre a camada de interface web, backend em API REST, containerização com Docker e deploy em produção.

## Como rodar localmente

**Pré-requisitos:** Python 3.10+, chave de API da OpenAI.

```bash
git clone https://github.com/ArthurG0uvea17/agente-financeiro.git
cd agente-financeiro

pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como referência):
```
OPENAI_API_KEY=sua_chave_aqui
```

Rode o agente:
```bash
python agente.py
```

Digite perguntas sobre câmbio, juros compostos ou clima. Digite `sair` para encerrar.

## Limitações conhecidas

- Sem interface web; interação apenas via terminal.
- Sem memória entre execuções: cada vez que o programa é reiniciado, o histórico de conversa é perdido.
- As APIs de câmbio e clima têm limites de uso da camada gratuita, adequados para testes mas não para uso em produção em escala.

## Próximos passos

- [ ] Adicionar mais ferramentas (ex: consulta de ações, cálculo de parcelamento)
- [ ] Memória de conversa persistida (reaproveitando a abordagem de SQLite do projeto RAG)
- [ ] Interface web, se o projeto evoluir para além de prova de conceito

## Autor

Arthur Gouvêa - [LinkedIn](https://linkedin.com/in/arthurgouvea/) - [GitHub](https://github.com/ArthurG0uvea17)
