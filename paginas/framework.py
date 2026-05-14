"""
Página "Framework" — agente de chat de mediação de risco para uso de IA no
setor público.

Tema "Daylight Control Room" (agente/styles.py). Backend: system prompt em
prompt_sistema.md + 3 motores + 5 camadas + prompt caching + adaptive thinking.
"""

from pathlib import Path
import os

import anthropic
import streamlit as st

from agente.exemplos import EXEMPLOS
from agente.rastro_decisorio import extrair_rastro_da_resposta
from agente.styles import STYLES, SEVERITY_LABELS, SEVERITY_CLASS
from analytics import registrar_visita


MODEL = "claude-opus-4-7"
MAX_TOKENS = 16000

VERSION = "v8"
VERSION_NOTE = "A agente se chama Lélia + página Conheça Lélia"

PROMPT_SISTEMA_PATH = Path(__file__).parent.parent / "agente" / "prompt_sistema.md"
LELIA_AVATAR = str(Path(__file__).parent.parent / "assets" / "lelia.png")

AMBIENTE_NAO_INFORMADO = "Não informado"
AMBIENTES = [AMBIENTE_NAO_INFORMADO, "Aberta", "Por API", "Contratada", "Própria"]
AMBIENTE_HELP = (
    "**Aberta:** IA pública usada direto no navegador, conta comum "
    "(ChatGPT, Gemini, Claude.ai), sem contrato corporativo. Risco máximo: "
    "o provedor pode reter e treinar com seus dados.\n\n"
    "**Por API:** um sistema do órgão acessa a IA pelo canal de programação "
    "de um provedor (OpenAI, Anthropic, Google). Há relação contratual e "
    "geralmente opção de não-treinamento, mas os dados ainda transitam para "
    "o provedor.\n\n"
    "**Contratada:** solução de IA de mercado contratada pelo órgão, com "
    "cláusulas específicas (no-training, no-retention, isolamento). O "
    "contrato define as garantias.\n\n"
    "**Própria:** o modelo roda em infraestrutura do próprio órgão "
    "(on-premise ou nuvem privada segregada). Maior controle, menor "
    "exposição externa."
)


@st.cache_resource
def get_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        st.error(
            "ANTHROPIC_API_KEY não encontrada. Crie um arquivo .env "
            "com a chave (veja .env.example)."
        )
        st.stop()
    return anthropic.Anthropic(api_key=api_key)


@st.cache_resource
def get_prompt_sistema() -> str:
    return PROMPT_SISTEMA_PATH.read_text(encoding="utf-8")


def render_sidebar() -> str | None:
    """Painel operacional: ambiente tecnológico + casos de teste."""
    st.sidebar.markdown(
        '<div class="terminal-header">'
        '<div class="th-title">GOVERNANÇA DE IA</div>'
        f'<div class="th-sub">TERMINAL OPERACIONAL · {VERSION.upper()}</div>'
        "</div>",
        unsafe_allow_html=True,
    )

    st.sidebar.selectbox(
        "Ambiente tecnológico",
        AMBIENTES,
        key="ambiente",
        help=AMBIENTE_HELP,
    )

    st.sidebar.markdown(
        '<div class="section-label">Casos de teste</div>'
        '<div class="section-caption">Casos canônicos para experimentar. '
        "Clique para preencher a pergunta.</div>",
        unsafe_allow_html=True,
    )

    pergunta_escolhida = None
    for i, exemplo in enumerate(EXEMPLOS, start=1):
        crit = exemplo.classificacao_esperada
        st.sidebar.markdown(
            '<div class="case-label">'
            f'<span class="case-id">Caso {i:02d}</span>'
            f'<span class="case-crit {SEVERITY_CLASS[crit]}">'
            f'<span class="crit-dot"></span>{SEVERITY_LABELS[crit]}</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        if st.sidebar.button(
            exemplo.titulo, key=f"case_{i}", use_container_width=True
        ):
            pergunta_escolhida = exemplo.pergunta

    st.sidebar.markdown("<hr/>", unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="sidebar-meta">'
        '<div class="meta-row"><span>MODELO</span><span>Claude Opus 4.7</span></div>'
        '<div class="meta-row"><span>PROTOCOLO</span><span>MGI 3.485/2026</span></div>'
        '<div class="meta-row"><span>BASE</span><span>LGPD · LAI · AIE</span></div>'
        "</div>",
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Limpar conversa", key="clear", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    return pergunta_escolhida


def render_metricas_cache(usage) -> None:
    """Mostra métricas de uso e cache na barra inferior (para calibração)."""
    if usage is None:
        return
    cols = st.columns(4)
    cols[0].metric("Tokens entrada (não-cache)", usage.input_tokens)
    cols[1].metric(
        "Tokens lidos do cache",
        getattr(usage, "cache_read_input_tokens", 0) or 0,
    )
    cols[2].metric(
        "Tokens escritos no cache",
        getattr(usage, "cache_creation_input_tokens", 0) or 0,
    )
    cols[3].metric("Tokens saída", usage.output_tokens)


def chamar_agente(
    client: anthropic.Anthropic, messages: list[dict], ambiente: str
) -> tuple[str, object]:
    """
    Chama Claude com:
    - prompt caching no system prompt (cache_control ephemeral)
    - bloco dinâmico com o ambiente tecnológico, quando informado na seleção prévia
    - adaptive thinking
    - effort high (intelligence-sensitive)
    - streaming (max_tokens alto)
    """
    system_blocks = [
        {
            "type": "text",
            "text": get_prompt_sistema(),
            "cache_control": {"type": "ephemeral"},
        }
    ]
    if ambiente and ambiente != AMBIENTE_NAO_INFORMADO:
        system_blocks.append(
            {
                "type": "text",
                "text": (
                    "CONTEXTO INFORMADO PELO USUÁRIO NA SELEÇÃO PRÉVIA: o "
                    f"ambiente tecnológico deste caso é '{ambiente}'. Já está "
                    "definido — incorpore na análise e não pergunte sobre "
                    "ambiente."
                ),
            }
        )

    final_message = None
    text_chunks: list[str] = []

    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        thinking={"type": "adaptive"},
        output_config={"effort": "high"},
        system=system_blocks,
        messages=messages,
    ) as stream:
        placeholder = st.empty()
        for text in stream.text_stream:
            text_chunks.append(text)
            placeholder.markdown("".join(text_chunks) + "▌")
        final_message = stream.get_final_message()
        placeholder.markdown("".join(text_chunks))

    return "".join(text_chunks), final_message.usage


def main() -> None:
    registrar_visita("framework")

    st.markdown(STYLES, unsafe_allow_html=True)

    st.title("Agente de Governança de IA")
    st.caption(
        "Mediação de risco para uso responsável de IA no setor público. "
        "Portaria MGI 3.485/2026, LGPD, LAI, Framework AIE."
    )
    st.caption(f"**{VERSION}** · {VERSION_NOTE}")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ultima_usage" not in st.session_state:
        st.session_state.ultima_usage = None

    pergunta_da_sidebar = render_sidebar()
    ambiente = st.session_state.get("ambiente", AMBIENTE_NAO_INFORMADO)

    # Renderiza histórico
    for msg in st.session_state.messages:
        avatar = LELIA_AVATAR if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                rastro = extrair_rastro_da_resposta(msg["content"])
                if rastro:
                    with st.expander("Extrato de Governança · Rastro Decisório"):
                        st.markdown(rastro)
                        st.download_button(
                            "Exportar extrato",
                            data=rastro,
                            file_name="rastro_decisorio.md",
                            mime="text/markdown",
                            key=f"download_{id(msg)}",
                        )

    pergunta = pergunta_da_sidebar or st.chat_input(
        "Descreva o uso de IA que você está considerando..."
    )

    if pergunta:
        st.session_state.messages.append({"role": "user", "content": pergunta})
        with st.chat_message("user"):
            st.markdown(pergunta)

        with st.chat_message("assistant", avatar=LELIA_AVATAR):
            client = get_client()
            resposta, usage = chamar_agente(
                client, st.session_state.messages, ambiente
            )
            st.session_state.ultima_usage = usage

            rastro = extrair_rastro_da_resposta(resposta)
            if rastro:
                with st.expander("Extrato de Governança · Rastro Decisório"):
                    st.markdown(rastro)
                    st.download_button(
                        "Exportar extrato",
                        data=rastro,
                        file_name="rastro_decisorio.md",
                        mime="text/markdown",
                        key="download_atual",
                    )

        st.session_state.messages.append({"role": "assistant", "content": resposta})

    if st.session_state.ultima_usage is not None:
        with st.expander("Telemetria · Uso e cache"):
            render_metricas_cache(st.session_state.ultima_usage)

    st.divider()
    st.caption(
        "Em conformidade com o princípio de transparência da Portaria MGI "
        "3.485/2026, que exige identificar o uso de IA: esta ferramenta é "
        "apoiada por IA. Usa a API da Anthropic (modelo Claude); pelos termos "
        "comerciais da API, o conteúdo enviado não é usado para treinar "
        "modelos; os dados transitam para a Anthropic (empresa dos EUA). Na "
        'taxonomia do próprio agente, é um uso "Por API": use com informação '
        "pública ou de baixa sensibilidade, não insira dados pessoais "
        "sensíveis ou sigilosos."
    )


main()
