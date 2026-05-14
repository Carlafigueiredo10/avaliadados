"""
Página "Métricas" — painel de visitas das páginas do app, protegido por senha.

A senha vem de METRICAS_SENHA (st.secrets no Streamlit Cloud, ou .env local).
A leitura dos agregados usa a função SECURITY DEFINER `metricas_visitas` no
Supabase — a tabela de visitas continua bloqueada por RLS.
"""

import hmac

import pandas as pd
import requests
import streamlit as st

from analytics import ler_config


ROTULOS_PAGINA = {"framework": "Framework", "avalia_dados": "Avalia Dados"}


def exigir_senha() -> None:
    """Bloqueia a página até que a senha correta seja informada."""
    senha_correta = ler_config("METRICAS_SENHA")
    if not senha_correta:
        st.error(
            "METRICAS_SENHA não configurada. Defina nos Secrets do Streamlit "
            "Cloud (ou no .env local) para acessar esta página."
        )
        st.stop()

    if st.session_state.get("_metricas_ok"):
        return

    senha = st.text_input("Senha", type="password")
    if not senha:
        st.stop()
    if not hmac.compare_digest(senha, senha_correta):
        st.error("Senha incorreta.")
        st.stop()
    st.session_state["_metricas_ok"] = True
    st.rerun()


def carregar_metricas() -> dict | None:
    url = ler_config("SUPABASE_URL")
    key = ler_config("SUPABASE_KEY")
    if not url or not key:
        st.error("SUPABASE_URL / SUPABASE_KEY não configurados.")
        return None
    try:
        resp = requests.post(
            f"{url}/rest/v1/rpc/metricas_visitas",
            headers={
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            timeout=8,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Não foi possível ler as métricas: {e}")
        return None


st.title("Métricas de visitas")

exigir_senha()

dados = carregar_metricas()
if dados is None:
    st.stop()

total_geral = dados.get("total", 0)
if total_geral == 0:
    st.info("Nenhuma visita registrada ainda.")
    st.stop()

por_pagina = {
    r["pagina"]: r["total"] for r in dados.get("por_pagina", [])
}

cols = st.columns(len(ROTULOS_PAGINA) + 1)
cols[0].metric("Total", total_geral)
for i, (chave, rotulo) in enumerate(ROTULOS_PAGINA.items(), start=1):
    cols[i].metric(rotulo, por_pagina.get(chave, 0))

st.subheader("Visitas por dia")
por_dia = dados.get("por_dia", [])
if por_dia:
    df = pd.DataFrame(por_dia)
    df["pagina"] = df["pagina"].map(lambda p: ROTULOS_PAGINA.get(p, p))
    pivot = df.pivot_table(
        index="dia", columns="pagina", values="total", fill_value=0
    )
    st.bar_chart(pivot)
else:
    st.caption("Sem dados diários ainda.")

if st.button("Atualizar"):
    st.rerun()
