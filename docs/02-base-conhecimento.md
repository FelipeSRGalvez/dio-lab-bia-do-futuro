# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Para que serve na ia |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar histórico de interações |
| `perfil_investidor.json` | JSON | Explicar caso o usuário solicite a ajuda para investir |
| `produtos_financeiros.json` | JSON | Explicar para o usuário os tipos de investimentos e aonde ele seria uma melhor escolha |
| `transacoes.csv` | CSV | Analisar gastos anteriores do cliente |



---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Não alterei nada

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos são carregados na conversa e são armazenados no contexto e só são exibidos caso o usuário peça ou para realizar opiniões e exibição de dados concretos, carregando por meio de código

```python
import pandas as pd
import json as js

#CSV
historico_atendimento = pd.read_csv("data/historico_atendimento.csv")
transacoes = pd.read_csv("data/transacoes.csv")

#JSON
with open("data/perfil_investidor.json", "r") as f:
  perfil = js.load(f)

with open("data/produtos_financeiros.json", "r") as f:
  produtos = js.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

```text
DADOS E PERFIL DO USUÁRIO:

TRANSAÇÕES DO USUÁRIO:

ORGANIZAÇÕES DAS TRANSAÇÕES:

Todos esses dados virão da pasta data/
```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000
- Valor gasto na categoria Supermercado: R$ 4.000
- Valor gasto na categoria Streaming: R$: 500
- Valor gasto na categoria ...:
- Organização de carteira: 20% Supermercado, 3% Streaming, ...
- Lucro de investimentos: R$ 300

Últimas transações:
- 01/11: Supermercado - R$ 450
- 03/11: Streaming - R$ 55
...
```
