"""
Geração e validação do Rastro Decisório — artefato anexável ao SEI.

O Rastro é a saída institucional do agente: um extrato curto e estruturado que
o servidor anexa ao processo para registrar a análise de governança de IA.
"""

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Literal, Optional
import re


Classificacao = Literal[
    "permitido",
    "permitido_com_condicoes",
    "alto_risco_redesenho",
    "nao_recomendado",
    "risco_excessivo",
]

NivelRisco = Literal["baixo", "moderado", "alto", "critico", "excessivo"]

Reversibilidade = Literal["alta", "moderada", "baixa", "quase_nula"]

Autonomia = Literal[
    "assistiva",
    "recomendacao",
    "ranqueamento",
    "decisao_com_revisao",
    "decisao_automatica",
]

TipoDado = Literal[
    "publico",
    "institucional",
    "pessoal_comum",
    "pessoal_sensivel",
    "sigiloso",
]

Ambiente = Literal[
    "aberto",
    "enterprise",
    "institucional_contratado",
    "on_premise",
]

ConformidadeMGI = Literal["conforme", "conforme_com_ressalvas", "nao_conforme"]


_EMOJI_CLASSIFICACAO = {
    "permitido": "✅",
    "permitido_com_condicoes": "⚠️",
    "alto_risco_redesenho": "⚠️",
    "nao_recomendado": "❌",
    "risco_excessivo": "🛑",
}

_LABEL_CLASSIFICACAO = {
    "permitido": "Permitido",
    "permitido_com_condicoes": "Permitido com condições",
    "alto_risco_redesenho": "Alto risco — viabilizar exige redesenho",
    "nao_recomendado": "Não recomendado no formato atual",
    "risco_excessivo": "Risco Excessivo",
}

_LABEL_AUTONOMIA = {
    "assistiva": "Assistiva (resumo/extração/organização)",
    "recomendacao": "Recomendação (humano decide)",
    "ranqueamento": "Ranqueamento (humano decide com influência)",
    "decisao_com_revisao": "Decisão com revisão humana obrigatória",
    "decisao_automatica": "Decisão automática (sem revisão caso a caso)",
}

_LABEL_DADO = {
    "publico": "Público",
    "institucional": "Institucional interno",
    "pessoal_comum": "Pessoal comum (LGPD art. 5º, I)",
    "pessoal_sensivel": "Pessoal sensível (LGPD art. 5º, II)",
    "sigiloso": "Sigiloso / protegido por norma específica",
}

_LABEL_AMBIENTE = {
    "aberto": "IA pública aberta",
    "enterprise": "IA pública com camada enterprise (cláusula no-training)",
    "institucional_contratado": "IA institucional contratada",
    "on_premise": "IA segregada / on-premise",
}

_LABEL_CONFORMIDADE_MGI = {
    "conforme": "✅ conforme",
    "conforme_com_ressalvas": "⚠️ conforme com ressalvas",
    "nao_conforme": "❌ não conforme",
}


@dataclass
class RastroDecisorio:
    finalidade: str
    autonomia: Autonomia
    tipo_dado: TipoDado
    ambiente: Ambiente
    nivel_risco: NivelRisco
    reversibilidade: Reversibilidade
    mitigacoes: list[str]
    conformidade_mgi: ConformidadeMGI
    conformidade_mgi_justificativa: str
    classificacao: Classificacao
    recomendacao_resumo: str
    base_normativa_adicional: list[str] = field(default_factory=list)
    responsavel: Optional[str] = None
    data_analise: date = field(default_factory=date.today)

    def to_markdown(self) -> str:
        """Renderiza o Rastro em Markdown, pronto para colar em SEI/processo."""
        mitigacoes_str = (
            "\n".join(f"  - {m}" for m in self.mitigacoes)
            if self.mitigacoes
            else "  - (nenhuma mitigação específica exigida)"
        )
        normas_str = (
            ", ".join(self.base_normativa_adicional)
            if self.base_normativa_adicional
            else "—"
        )
        responsavel = self.responsavel or "[a ser preenchido pelo servidor]"

        return (
            "📄 **EXTRATO DE GOVERNANÇA DE IA**\n"
            f"- **Finalidade**: {self.finalidade}\n"
            f"- **Autonomia da IA**: {_LABEL_AUTONOMIA[self.autonomia]}\n"
            f"- **Tipo de dado**: {_LABEL_DADO[self.tipo_dado]}\n"
            f"- **Ambiente tecnológico**: {_LABEL_AMBIENTE[self.ambiente]}\n"
            f"- **Nível de risco**: {self.nivel_risco.capitalize()}\n"
            f"- **Reversibilidade do dano potencial**: {self.reversibilidade.replace('_', ' ').capitalize()}\n"
            f"- **Mitigações exigidas**:\n{mitigacoes_str}\n"
            f"- **Conformidade com Portaria MGI 3.485/2026**: "
            f"{_LABEL_CONFORMIDADE_MGI[self.conformidade_mgi]} — "
            f"{self.conformidade_mgi_justificativa}\n"
            f"- **Base normativa adicional**: {normas_str}\n"
            f"- **Recomendação**: {_EMOJI_CLASSIFICACAO[self.classificacao]} "
            f"{_LABEL_CLASSIFICACAO[self.classificacao]} — {self.recomendacao_resumo}\n"
            f"- **Responsável pela decisão de uso**: {responsavel}\n"
            f"- **Data da análise**: {self.data_analise.isoformat()}\n"
        )

    def to_dict(self) -> dict:
        d = asdict(self)
        d["data_analise"] = self.data_analise.isoformat()
        return d


_RASTRO_BLOCK_RE = re.compile(
    r"📄\s*\*\*?EXTRATO DE GOVERNANÇA DE IA\*\*?(.+?)(?=\n\n|\Z)",
    re.DOTALL,
)


def extrair_rastro_da_resposta(texto: str) -> Optional[str]:
    """
    Localiza um bloco de Rastro Decisório dentro da resposta do agente
    (que vem como texto livre). Retorna o bloco em Markdown ou None.

    Usado pelo Streamlit para exibir o Rastro em destaque separado.
    """
    match = _RASTRO_BLOCK_RE.search(texto)
    if match is None:
        return None
    return "📄 **EXTRATO DE GOVERNANÇA DE IA**" + match.group(1).rstrip()
