"""
Página "Base teórica e normativa" — a fundamentação do agente, visível.

Cada item está amarrado ao conceito que ele ancora e ao ponto onde esse
conceito opera na análise. Bibliografia não é enfeite: referência sem onde
amarrar não entra.
"""

import streamlit as st

from agente.styles import STYLES

st.markdown(STYLES, unsafe_allow_html=True)

st.title("Base teórica e normativa")
st.caption(
    "Tudo que a análise do agente pisa, visível. Cada item está amarrado ao "
    "conceito que ele ancora e ao ponto onde esse conceito opera. "
    "Bibliografia não é enfeite."
)

NORMATIVA = [
    (
        "Lei nº 13.709/2018 — LGPD",
        "Finalidade, adequação, necessidade, não discriminação, prestação de "
        "contas. Base do tratamento de dados pessoais e sensíveis em toda a "
        "análise, e do direito à revisão de decisões automatizadas (art. 20).",
    ),
    (
        "Lei nº 12.527/2011 — LAI",
        "Transparência ativa e passiva, dever de motivação dos atos. Base do "
        "princípio de que decisão de impacto público precisa ser explicável e "
        "contestável.",
    ),
    (
        "Portaria MGI nº 3.485/2026",
        "Política de Governança de IA no MGI: o arcabouço que o agente executa. "
        "Uso de IA generativa restrito a informação pública como regra, "
        "supervisão humana proporcional ao risco, identificação de conteúdo "
        "apoiado por IA, notificação de incidentes ao SCIA.",
    ),
    (
        "Framework AIE (Autoavaliação de Impacto Ético) — MGI",
        "Define o conceito de Risco Excessivo: usos vedados por contrariarem "
        "direitos fundamentais. Base das Red Lines do agente.",
    ),
    (
        "Plano Brasileiro de Inteligência Artificial (PBIA)",
        "Diretrizes éticas e meta de adoção de IA com critérios éticos nos "
        "órgãos do SISP.",
    ),
    (
        "Constituição Federal",
        "Legalidade, impessoalidade, moralidade, publicidade e eficiência "
        "(art. 37); devido processo (art. 5º, LIV); não discriminação "
        "(art. 3º, IV). Chão de todos os motores.",
    ),
    (
        "Lei nº 12.288/2010 — Estatuto da Igualdade Racial",
        "Base para exigir meta de diversidade declarada em contextos de "
        "seleção, ranqueamento e alocação.",
    ),
    (
        "Lei nº 13.146/2015 — Lei Brasileira de Inclusão",
        "Acessibilidade e não discriminação como direitos transversais. "
        "Sustenta o eixo representativo da composição da supervisão.",
    ),
    (
        "Lei nº 14.133/2021 — Lei de Licitações",
        "Promoção do desenvolvimento sustentável e da igualdade nos contratos "
        "públicos. Relevante na contratação de soluções de IA de mercado.",
    ),
    (
        "UNESCO — Recomendação sobre a Ética da IA (2021)",
        "Linhagem internacional do framework brasileiro. Supervisão humana, "
        "transparência, proporcionalidade e abordagem baseada em direitos "
        "humanos são influência upstream da Portaria e do AIE.",
    ),
    (
        "União Europeia — Ethics Guidelines for Trustworthy AI (2019) e AI Act",
        "A abordagem de risco em camadas que inspira a escala de classificação "
        'do agente; "Risco Excessivo" ecoa a categoria de "unacceptable risk", '
        "e as Red Lines lembram as práticas proibidas.",
    ),
]

TEORICA = [
    (
        "Tarcízio Silva — Racismo Algorítmico (2022)",
        "Ancora o tratamento de viés herdado dos dados de treinamento, a "
        "armadilha da otimização-para-fit e a alocação distributiva que "
        "reproduz segregação de perfis por setor. Algoritmo treinado no status "
        "quo reproduz desigualdade estrutural.",
    ),
    (
        "Virginia Eubanks — Automating Inequality (2018)",
        "Ancora o alerta de não automatizar a burocracia: eficiência para o "
        "órgão não é entrega para a pessoa, e a automação no setor público "
        "pode racionar acesso, vigiar e punir, vestida de modernização.",
    ),
    (
        "Sasha Costanza-Chock — Design Justice (2020)",
        "Ancora a composição da supervisão (representativa e epistêmica), o "
        '"demandante ≠ executor" e a própria tese de que diversidade é '
        "arquitetura. Quem o sistema afeta precisa estar na sala onde ele é "
        "desenhado.",
    ),
    (
        "Ruha Benjamin — Race After Technology (2019)",
        'Ancora a ideia de que a neutralidade aparente do modelo é o próprio '
        'mecanismo do viés, e o "desconfie do polido". Tecnologia '
        "discriminatória vestida de neutra ou progressista.",
    ),
    (
        "Safiya Noble — Algorithms of Oppression (2018)",
        "Reforça, junto com Benjamin, o mito da neutralidade algorítmica em "
        "sistemas de busca e ranqueamento.",
    ),
    (
        "Catherine D'Ignazio e Lauren Klein — Data Feminism (2020)",
        "Ancora a passagem de \"ética de dados\" para \"justiça de dados\": "
        "falhas algorítmicas não são acidentes esporádicos, são evidência de "
        "como um sistema desigual opera normalmente. Sustenta a pergunta "
        "deslocada de \"os dados têm viés?\" para \"a base reflete opressões "
        "históricas?\".",
    ),
]

st.subheader("Base normativa e marcos")
for titulo, nota in NORMATIVA:
    with st.expander(titulo):
        st.markdown(nota)

st.subheader("Base teórica")
for titulo, nota in TEORICA:
    with st.expander(titulo):
        st.markdown(nota)
