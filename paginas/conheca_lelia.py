"""
Página "Conheça Lélia" — a história de quem inspirou o nome da agente.

A agente desta ferramenta se chama Lélia, em homenagem a Lélia Gonzalez.
O conteúdo biográfico desta página deve ser verificado e completado pela
equipe antes de uso público — homenagem a uma intelectual real não roda
em memória aproximada.
"""

from pathlib import Path

import streamlit as st

from agente.styles import STYLES

st.markdown(STYLES, unsafe_allow_html=True)

LELIA_GONZALEZ_IMG = Path(__file__).parent.parent / "assets" / "lelia_gonzalez.png"

st.title("Conheça Lélia")
st.caption(
    "A agente desta ferramenta se chama Lélia. O nome é uma homenagem — "
    "e a homenagem é um compromisso."
)

if LELIA_GONZALEZ_IMG.exists():
    col_img, col_txt = st.columns([1, 2])
    with col_img:
        st.image(str(LELIA_GONZALEZ_IMG), use_container_width=True)
    contexto = col_txt
else:
    contexto = st.container()

with contexto:
    st.subheader("Quem foi Lélia Gonzalez")
    st.markdown(
        "Lélia Gonzalez (1935–1994) foi uma intelectual, professora e ativista "
        "brasileira, nascida em Belo Horizonte. É uma das fundadoras do "
        "pensamento do feminismo negro no Brasil: pensou raça, gênero e classe "
        "de forma articulada, nunca como camadas separadas.\n\n"
        "Foi uma das fundadoras do Movimento Negro Unificado, em 1978. Cunhou o "
        "conceito de **amefricanidade**, que repensa as Américas a partir da "
        "diáspora africana, e trabalhou a noção de **pretuguês** — a marca das "
        "línguas africanas no português falado no Brasil. Sua obra criticou de "
        "frente o mito da \"democracia racial\" brasileira.\n\n"
        "Marginalizada em vida, sua produção é hoje central no pensamento "
        "social brasileiro."
    )

st.subheader("Por que ela inspira esta agente")
st.markdown(
    "O nome não é decoração. As ideias de Lélia Gonzalez são a fundação "
    "conceitual do que esta ferramenta faz:\n\n"
    "- **Raça, gênero e classe como estrutura, não acessório** — a tese de que "
    "*diversidade é arquitetura* é, antes de tudo, a forma como ela pensava o "
    "social: essas dimensões não se somam ao final da análise, elas a "
    "constituem.\n"
    "- **O mito da democracia racial** — a crítica dela ao Brasil que se diz "
    "neutro em raça é a mesma desconfiança que a agente aplica ao algoritmo "
    "que se diz neutro. Neutralidade aparente costuma ser o mecanismo do viés.\n"
    "- **Amefricanidade** — centrar perspectivas que foram empurradas para a "
    "margem é o que sustenta a exigência de que a revisão de uma decisão de IA "
    "seja composta por quem aquela decisão afeta.\n"
    "- **Pretuguês e a recusa da \"caixa preta\"** — Lélia usou a linguagem "
    "para democratizar o pensamento e enfrentar o jargão acadêmico excludente. "
    "Para a agente, isso significa que a explicabilidade é inegociável: a "
    "justificativa de um algoritmo que afeta o cidadão deve ser traduzível, "
    "compreensível e contestável por qualquer pessoa, e não um privilégio de "
    "engenheiros.\n"
    "- **Anticolonialismo e soberania digital** — a crítica de Lélia à "
    "submissão intelectual a modelos externos fundamenta a defesa do Estado "
    "brasileiro contra o colonialismo de dados. A agente atua para garantir "
    "que os dados públicos não sejam meramente extraídos para treinar modelos "
    "privados sem contrapartida, protegendo a soberania institucional do "
    "país.\n\n"
    "**A práxis e a ação.** Lélia não era apenas uma teórica: foi uma das "
    "fundadoras do Movimento Negro Unificado e uma ativista focada na "
    "transformação prática da realidade. Herdando esse espírito, esta agente "
    "não atua como um órgão censor que paralisa a inovação pelo medo. Ela é "
    "uma viabilizadora: traduz o risco em ação possível, apontando os caminhos "
    "e as mitigações para que o Estado inove com segurança.\n\n"
    "Esta é uma ponte interpretativa: Lélia Gonzalez não escreveu sobre "
    "inteligência artificial. Mas pensar IA no setor público com seriedade "
    "sobre desigualdade é, inevitavelmente, herdar o trabalho dela."
)

st.divider()
st.caption(
    "Esta página é uma homenagem em construção. O conteúdo biográfico será "
    "revisado e ampliado com fontes pela equipe."
)
