"""
Página "Avalia Dados" — questionário de Autoavaliação de Impacto Ético da IA
no Setor Público (AIE).

O questionário é um HTML autocontido (assets/aie.html), embutido sem nenhuma
alteração num iframe isolado.
"""

from pathlib import Path

import streamlit as st

from analytics import registrar_visita


AIE_HTML = Path(__file__).parent.parent / "assets" / "aie.html"

registrar_visita("avalia_dados")

st.title("Autoavaliação de Impacto Ético da IA (AIE)")
st.caption(
    "Jornada de reflexão para construir IAs mais justas, transparentes e "
    "responsáveis no setor público. Versão BETA."
)

st.iframe(AIE_HTML, height=1500)
