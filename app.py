"""
avaliadados — app Streamlit multipágina:

- Consulta de uso de IA:                            agente de chat de mediação de risco
- Autoavaliação de Impacto Ético da IA (AIE) do MGI: questionário estruturado
- Base teórica e normativa:                         fundamentação anotada do agente
- Métricas:                                         telemetria de uso

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
    st.Page("paginas/framework.py", title="Consulta de uso de IA", icon="💬", default=True),
    st.Page(
        "paginas/avalia_dados.py",
        title="Autoavaliação de Impacto Ético da IA (AIE) do MGI",
        icon="📋",
    ),
    st.Page(
        "paginas/base_teorica.py",
        title="Base teórica e normativa",
        icon="📚",
    ),
    st.Page("paginas/metricas.py", title="Métricas", icon="📊"),
]

st.navigation(paginas).run()
