"""
Contador de visitas via Supabase.

Tabela `avaliadados_visitas` no projeto Supabase `alavanca`, acessada por uma
função SECURITY DEFINER (`registrar_visita`) — a chave publishable não toca a
tabela diretamente. Falha sempre em silêncio: o contador nunca quebra a página.
"""

from __future__ import annotations

import os
import uuid

import requests
import streamlit as st


def ler_config(nome: str) -> str | None:
    """Lê de st.secrets (Streamlit Cloud) ou das variáveis de ambiente (.env local)."""
    try:
        valor = st.secrets.get(nome)
    except Exception:
        valor = None
    return valor or os.environ.get(nome)


def registrar_visita(pagina: str) -> int | None:
    """
    Registra uma visita à `pagina` — uma única vez por sessão — e devolve o
    total acumulado daquela página. Retorna None se o Supabase não estiver
    configurado ou indisponível.
    """
    ja_registrada = f"_visita_registrada_{pagina}"
    total_cache = f"_visita_total_{pagina}"

    if st.session_state.get(ja_registrada):
        return st.session_state.get(total_cache)

    url = ler_config("SUPABASE_URL")
    key = ler_config("SUPABASE_KEY")
    if not url or not key:
        return None

    if "_sessao_id" not in st.session_state:
        st.session_state["_sessao_id"] = uuid.uuid4().hex

    try:
        user_agent = st.context.headers.get("User-Agent")
    except Exception:
        user_agent = None

    total = None
    try:
        resp = requests.post(
            f"{url}/rest/v1/rpc/registrar_visita",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "p_pagina": pagina,
                "p_sessao": st.session_state["_sessao_id"],
                "p_user_agent": user_agent,
            },
            timeout=4,
        )
        resp.raise_for_status()
        total = resp.json()
    except Exception:
        total = None

    st.session_state[ja_registrada] = True
    st.session_state[total_cache] = total
    return total
