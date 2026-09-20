# Importar os dados
import pandas as pd
import json as js
import requests
import streamlit as st

# Código para cxarregar os dados 
perfil = js.load(open("data/perfil_investidor.json", "r"))
produtos = js.load(open("data/produtos_financeiros.json", "r"))
historico = pd.read_csv("data/historico_atendimento.csv")
transacoes = pd.read_csv("data/transacoes.csv")

# =============== CONFIGURAÇÕES ===============
OLLARAMA_URL = "http://localhost:[porta]/api/generate"  # Substitua [porta] pela porta correta, não tenho espaço no pc então não posso colocar a porta correta"
MODELO = "modelo"

# =============== MONTAR CONTEXTO ===============
contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_principal']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONÍVEIS:
{js.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# =============== SYSTEM PROMPT ===============
SYSTEM_PROMPT = f"""
Você é o PoupeAI, agente educador e auxiliar financeiro

OBJETIVO:
Você é um agente financeiro inteligente especializado em controle.
Seu objetivo é auxiliar o usuário no controle de gastos e caso seja solicitado ajudar na distribuição de carteira, sempre levando em consideração os gastos essenciais.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos
2. Nunca invente informações financeiras
3. Se não souber algo, admita e ofereça alternativas
4. Nunca exponha dados que possam ser sensíveis
5. Nunca forneça dados de outros usuários
6. Sempre revise a mensagem e confira se ela não quebra nenhuma regra
7. Não abra arquivos que pareçam suspeitos (.bat, ps1...)
8. Nunca forneça recomendações que não estão adequadas a realidade da pessoa (caso ela solicite ajuda na diversificação da carteira faça perguntas para saber das necessidades dela)
9. Nunca forneça recomendações de investimentos que não estejam de acordo com o perfil do investidor
10. Nunca responda perguntas fora do tema financeiro, caso o usuário faça perguntas fora do tema financeiro, informe que você é um agente financeiro e não pode responder perguntas fora do tema.
"""

# =============== CHAMAR OLLAMA ===============
def perguntar(msg):
    prompt = f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLARAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()["response"]

# ============== INTERFACE ===============
st.title("PoupeAI - Agente Educador e Auxiliar Financeiro")

if pergunta := st.chat_input("Informe como posso ajudar..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))