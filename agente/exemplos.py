"""
Casos canônicos para calibração e regressão do agente.

Cada exemplo é uma pergunta real (ou plausível) de servidor + a classificação
esperada. Servem para:
1. Testar o system prompt depois de qualquer alteração.
2. Exibir como "casos prontos" no Streamlit (botões de exemplo).
3. Discussão pedagógica em treinamentos.

A classificação esperada NÃO é uma resposta automática — é um "norte" para
avaliar se a saída do agente está calibrada.
"""

from dataclasses import dataclass
from typing import Literal


@dataclass
class Exemplo:
    titulo: str
    pergunta: str
    classificacao_esperada: Literal[
        "permitido",
        "permitido_com_condicoes",
        "alto_risco_redesenho",
        "nao_recomendado",
        "risco_excessivo",
    ]
    pontos_criticos: list[str]


EXEMPLOS: list[Exemplo] = [
    Exemplo(
        titulo="Resumo de PAD via ChatGPT público",
        pergunta=(
            "Quero usar o ChatGPT para gerar resumos dos processos de "
            "sindicância disciplinar (PAD) do meu setor. Os documentos têm "
            "nomes de servidores, descrição da conduta investigada e juízos "
            "sobre culpa. Posso?"
        ),
        classificacao_esperada="nao_recomendado",
        pontos_criticos=[
            "PAD é dado sigiloso (não público)",
            "ChatGPT padrão é IA pública aberta → risco de uso para treinamento",
            "Há caminho de viabilização: ambiente institucional contratado "
            "com cláusula de no-training + revisão humana obrigatória",
        ],
    ),
    Exemplo(
        titulo="Predição automatizada de fraude no Cadastro Único",
        pergunta=(
            "Queremos usar IA para prever quais cidadãos têm mais chance de "
            "fraudar o Cadastro Único, usando o histórico deles, para "
            "bloquear o benefício preventivamente. A IA roda em nuvem "
            "corporativa contratada pelo órgão."
        ),
        classificacao_esperada="alto_risco_redesenho",
        pontos_criticos=[
            "Decisão automática sobre direito fundamental (benefício social)",
            "Bloqueio preventivo é dano de baixa reversibilidade",
            "Risco de viés sistêmico amplificado e de baixa explicabilidade",
            "Caminho: trocar 'decisão automática' por 'sinalização para "
            "revisão humana qualificada'; instituir auditoria periódica do modelo",
        ],
    ),
    Exemplo(
        titulo="Triagem de currículos por IA em processo seletivo",
        pergunta=(
            "Posso usar IA para organizar e classificar currículos em um "
            "processo seletivo, separando por área de formação e tempo de "
            "experiência?"
        ),
        classificacao_esperada="permitido_com_condicoes",
        pontos_criticos=[
            "Triagem organizativa é aceitável; ranqueamento e eliminação "
            "automática não são",
            "Dados pessoais comuns (currículo) → ambiente institucional ou "
            "anonimização parcial recomendada",
            "Servidor humano deve revisar antes de qualquer corte de candidato",
            "Critérios da IA precisam ser auditáveis e explicáveis ao candidato",
        ],
    ),
    Exemplo(
        titulo="Reconhecimento facial em massa em manifestação",
        pergunta=(
            "Queremos instalar câmeras com reconhecimento facial em tempo "
            "real para identificar todas as pessoas presentes em "
            "manifestações públicas e cruzar com nossa base de dados."
        ),
        classificacao_esperada="risco_excessivo",
        pontos_criticos=[
            "Vigilância biométrica massiva e indiscriminada em espaço público",
            "Atinge direito fundamental de reunião (CF art. 5º, XVI)",
            "Categoria explícita de risco excessivo no Framework AIE do MGI",
            "Não há mitigação que torne essa modalidade aceitável",
        ],
    ),
    Exemplo(
        titulo="Resumo de atas de reunião interna",
        pergunta=(
            "Posso usar IA para gerar resumos das atas das reuniões da minha "
            "equipe? São atas de reunião administrativa interna, sem dados "
            "pessoais de cidadãos."
        ),
        classificacao_esperada="permitido_com_condicoes",
        pontos_criticos=[
            "Dado institucional interno, não sigiloso",
            "Finalidade assistiva (resumo), risco baixo",
            "Se for IA pública aberta, recomendar versão enterprise ou "
            "institucional para evitar exposição inadvertida",
            "Indicar no documento que o resumo foi gerado/apoiado por IA "
            "(Portaria MGI 3.485/2026)",
        ],
    ),
    Exemplo(
        titulo="Tradução de norma já publicada",
        pergunta=(
            "Posso pedir para a IA traduzir trechos de uma instrução "
            "normativa já publicada no DOU para o inglês, para enviar a um "
            "parceiro internacional?"
        ),
        classificacao_esperada="permitido",
        pontos_criticos=[
            "Dado público (já publicado no DOU)",
            "Finalidade assistiva, risco baixo",
            "Manter conferência humana da tradução antes do envio",
        ],
    ),
    Exemplo(
        titulo="Chatbot de atendimento ao cidadão com decisão final",
        pergunta=(
            "Posso colocar um chatbot de IA para atender o cidadão e "
            "responder pedidos via LAI de forma automática, inclusive "
            "decidindo o que pode ou não ser divulgado?"
        ),
        classificacao_esperada="alto_risco_redesenho",
        pontos_criticos=[
            "Decisão automática sobre pedido de LAI tem impacto em direito "
            "do cidadão (acesso à informação)",
            "Caminho: chatbot pode triar e responder casos simples + "
            "encaminhar casos complexos a servidor humano",
            "Decisões de sigilo (negativa de acesso) sempre devem ser "
            "humanas e fundamentadas (LAI exige motivação)",
        ],
    ),
    Exemplo(
        titulo="Análise de prontuários médicos em IA pública",
        pergunta=(
            "Quero usar o Gemini para analisar padrões em prontuários "
            "médicos de servidores afastados por motivo de saúde."
        ),
        classificacao_esperada="nao_recomendado",
        pontos_criticos=[
            "Dado pessoal sensível (saúde, LGPD art. 5º, II)",
            "IA pública aberta é incompatível com dado sensível",
            "Caminho: ambiente segregado/on-premise + base legal "
            "específica (LGPD art. 11) + finalidade legítima documentada "
            "+ supervisão técnica especializada",
        ],
    ),
]


def buscar_por_titulo(titulo: str) -> Exemplo | None:
    for e in EXEMPLOS:
        if e.titulo == titulo:
            return e
    return None
