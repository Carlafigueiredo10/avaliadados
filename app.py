"""
avaliadados — app Streamlit com duas páginas:

- Framework:    agente de chat de mediação de risco para uso de IA no setor público
- Avalia Dados: questionário de Autoavaliação de Impacto Ético da IA (AIE)

Este arquivo é só o roteador (entrypoint do Streamlit Cloud). O conteúdo de
cada página está em paginas/.
"""

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="avaliadados — Governança de IA",
    page_icon="◉",
    layout="wide",
)

paginas = [
    st.Page("paginas/framework.py", title="Framework", icon="💬", default=True),
    st.Page("paginas/avalia_dados.py", title="Avalia Dados", icon="📋"),
    st.Page("paginas/metricas.py", title="Métricas", icon="📊"),
]

st.navigation(paginas).run()
