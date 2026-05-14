"""
Agente de Governança de IA — protótipo Streamlit.

Frontend simples. Backend sofisticado (system prompt em prompt_sistema.md +
3 motores + 5 camadas + prompt caching da Anthropic + adaptive thinking).
"""

from pathlib import Path
import os

import anthropic
import streamlit as st
from dotenv import load_dotenv

from agente.exemplos import EXEMPLOS
from agente.rastro_decisorio import extrair_rastro_da_resposta


load_dotenv()

MODEL = "claude-opus-4-7"
MAX_TOKENS = 16000

PROMPT_SISTEMA_PATH = Path(__file__).parent / "agente" / "prompt_sistema.md"


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
    """Sidebar com casos de teste prontos. Retorna a pergunta escolhida, se houver."""
    st.sidebar.title("Casos de teste")
    st.sidebar.caption(
        "Casos canônicos para experimentar. Clique para preencher a pergunta."
    )

    pergunta_escolhida = None
    for exemplo in EXEMPLOS:
        if st.sidebar.button(exemplo.titulo, use_container_width=True):
            pergunta_escolhida = exemplo.pergunta

    st.sidebar.divider()
    st.sidebar.markdown(
        "**Sobre**\n\n"
        "Agente de mediação de risco para uso de IA no setor público. "
        "Backend baseado em Portaria MGI 3.485/2026, LGPD, LAI e Framework AIE."
    )

    if st.sidebar.button("🗑️ Limpar conversa", use_container_width=True):
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


def chamar_agente(client: anthropic.Anthropic, messages: list[dict]) -> tuple[str, object]:
    """
    Chama Claude com:
    - prompt caching no system prompt (cache_control ephemeral)
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
    st.set_page_config(
        page_title="Agente de Governança de IA",
        page_icon="📄",
        layout="wide",
    )

    st.title("Agente de Governança de IA")
    st.caption(
        "Mediação de risco para uso responsável de IA no setor público — "
        "Portaria MGI 3.485/2026, LGPD, LAI, Framework AIE."
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "ultima_usage" not in st.session_state:
        st.session_state.ultima_usage = None

    pergunta_da_sidebar = render_sidebar()

    # Renderiza histórico
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                rastro = extrair_rastro_da_resposta(msg["content"])
                if rastro:
                    with st.expander("📄 Rastro Decisório (anexável ao processo)"):
                        st.markdown(rastro)
                        st.download_button(
                            "Baixar como Markdown",
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

        with st.chat_message("assistant"):
            client = get_client()
            resposta, usage = chamar_agente(client, st.session_state.messages)
            st.session_state.ultima_usage = usage

            rastro = extrair_rastro_da_resposta(resposta)
            if rastro:
                with st.expander("📄 Rastro Decisório (anexável ao processo)"):
                    st.markdown(rastro)
                    st.download_button(
                        "Baixar como Markdown",
                        data=rastro,
                        file_name="rastro_decisorio.md",
                        mime="text/markdown",
                        key="download_atual",
                    )

        st.session_state.messages.append({"role": "assistant", "content": resposta})

    if st.session_state.ultima_usage is not None:
        with st.expander("🔍 Métricas (uso e cache)"):
            render_metricas_cache(st.session_state.ultima_usage)


if __name__ == "__main__":
    main()
