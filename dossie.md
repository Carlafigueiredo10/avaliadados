### Dossiê de Prototipação: Agente de Governança de IA (Setor Público)

Este dossiê estabelece as especificações técnicas e funcionais para a implementação do Agente de Governança de Inteligência Artificial, operando sob a égide da conformidade normativa e segurança da informação institucional.

##### 1\. Fundamentação Normativa e Alinhamento Estratégico

**1.1. Marco Regulatório Base**  O Agente deve ser o braço executor da  **Portaria MGI nº 3.485/2026** , que institui a Política de Governança de Inteligência Artificial. Sua arquitetura prioriza o uso ético, seguro e transparente, garantindo que qualquer aplicação de IA no âmbito ministerial esteja alinhada aos valores públicos e à supervisão humana obrigatória.**1.2. Conformidade Legal e Acesso à Informação**  O Agente operará em estrita observância à  **LGPD (Lei nº 13.709/2018)**  e à  **Lei de Acesso à Informação (LAI)** . A lógica algorítmica deve seguir a premissa de que o acesso é a regra e o sigilo a exceção, protegendo informações pessoais e sigilosas apenas nos estritos termos legais.**1.3. Propósito: Supervisão por Design**  A missão do Agente é atuar como uma camada de "Supervisão por Design". Nenhum output de IA deve ser entregue ao usuário final sem a validação do Motor Ético, assegurando que o processamento automatizado nunca substitua o juízo crítico humano em decisões de impacto público.

##### 2\. Arquitetura de 3 Motores do Agente

**2.1. Motor Jurídico (Compliance Interceptativo)**  O Agente  **DEVE**  interceptar todos os payloads de entrada e saída, validando-os contra a base de restrições legais. O bloqueio automático é mandatório para:

* **Informações Protegidas:**  Dados protegidos por sigilo bancário, fiscal, comercial, profissional e segredo de justiça.  
* **Ações Transgressoras:**  Qualquer fluxo que viole a Seção 7 da Política de Classificação da Vector Informática.**2.2. Motor Ético (Valores e Proteção da Imagem)**  Baseado nas diretrizes da Portaria MGI, este motor atua como um firewall de integridade.  
* **Diretriz:**  Impedir resultados que violem a honra, imagem, intimidade ou vida privada (conforme definições da Seção 6 do contexto).  
* **Intervenção:**  Todo processamento rotulado como de alto risco deve conter um gatilho de "human-in-the-loop" antes da conclusão.**2.3. Motor Operacional (Classificação Automatizada)**  O Agente classificará os dados em tempo real nos níveis:  *Público* ,  *Interno* ,  *Restrito*  ou  *Sigiloso* .  
* **Comando de Identificação por Suporte (Seção 8.1):**  
* **Papel:**  Identificar classificação no cabeçalho de todas as páginas e capa; etiquetas superiores para externos.  
* **E-mail:**  Inserção obrigatória do grau de sigilo no Assunto e termo específico na assinatura.  
* **Documentos Eletrônicos:**  Aplicação de nomenclatura padronizada via metadados do sistema.  
* **Outros:**  Marca d'água ou classificação visível no início do documento.

##### 3\. Camadas de Avaliação Multidimensional

**3.1. Avaliação de Finalidade e Impacto**  O Agente deve validar se a IA agrega valor institucional. O risco é graduado conforme o impacto da quebra de confidencialidade:

* **Impacto Grave/Severo:**  Se o processamento puder inviabilizar objetivos estratégicos ou causar prejuízo financeiro, o Agente deve exigir criptografia de ponta a ponta.**3.2. Camada de Dados (Mapeamento Anexo I)**  O Agente deve identificar e rotular os seguintes vetores de dados extraídos do Anexo I:  
* **Dados Pessoais:**  IP, Geolocalização, Nome, RG, CPF, Endereço (Residencial/Comercial), Telefone, Conta Bancária, Dados de veículo, Contato, Endereço postal, E-mail, Redes sociais, Fotografia, Prontuário de saúde, Renda, Cartão bancário.  
* **Dados Pessoais Sensíveis:**  Origem racial/étnica, convicção religiosa, opinião política, filiação sindical/política, saúde/vida sexual, dados genéticos/biométricos, informações de Prevenção a Covid-19 e biometria de acesso.**3.3. Governança de Ambiente**  Sob a responsabilidade técnica de  **Emilson Queiroz (Gerente de TI e Cloud)** , o Agente monitorará se o armazenamento segue controles de acesso rigorosos e se o descarte eletrônico cumpre os protocolos automatizados da TI.

##### 4\. Matrizes de Risco e Mitigação

**4.1. Classificação de Riscos de Segurança**| Grau de Sigilo | Impacto da Quebra | Requisito de Proteção (Metadados/Físico) || \------ | \------ | \------ || **Público** | Sem impacto institucional. | Livre circulação; sem requisitos específicos. || **Interno** | Impacto baixo/Indesejado. | Distribuição restrita ao ambiente interno Vector. || **Restrito** | Dano Médio / Colateral. | Local seguro; tramitação via "envelope lacrado" digital. || **Sigiloso** | Dano Grave / Severo. | Controle de acesso estrito; "envelope duplamente lacrado". |  
**4.2. Mitigação de 'Shadow AI' e Risco Excessivo**   **Instrução Técnica para Implementação:**  O Agente deve monitorar logs de requisições de rede para detectar o uso de ferramentas de IA não homologadas (Shadow AI) que processem dados  *Restritos*  ou  *Sigilosos* . Caso identifique tráfego de dados sensíveis para endpoints externos não autorizados, o Agente deve revogar o token de acesso e aplicar "headers de metadados criptografados" para rastrear o vazamento.**4.3. Protocolo de Bloqueio e Escalonação**  Em casos de risco de "Dano Grave" às operações ou imagem da instituição, o Agente suspenderá o processamento imediatamente. O desbloqueio exigirá credenciais de nível "Alta Gestão", com notificação direta ao  **CEO Suleiman Bragança** .

##### 5\. Rastro Decisório: O Recibo de Governança

**5.1. Composição do Log de Auditoria**  Para cada transação de IA, o Agente gerará um log em formato Markdown contendo os seguintes campos obrigatórios:

* Classification\_Level: Nível atribuído (Público a Sigiloso).  
* Integrity\_Status: Flag booleana confirmando se a informação está atualizada.  
* Access\_Whitelist: Lista de pessoal autorizado baseada na Seção 8\.  
* Portaria\_MGI\_Compliance\_Flag: Confirmação de análise sob a norma 3.485/2026.  
* Format\_Metadata: Modo de confecção e assunto do documento original.**5.2. Temporalidade e Auto-Destruição**  O Agente deve extrair a data de criação do documento e aplicar uma flag de "Auto-Destruição" ou "Arquivamento", respeitando rigorosamente a tabela de temporalidade e a legislação vigente (Seção 10).

##### 6\. Responsabilidades e Manutenção do Sistema

**6.1. Matriz de Atores**

* **Alta Direção (Suleiman Bragança):**  Aprovação final das políticas e intervenção em riscos severos.  
* **Gestão Técnica (Emilson Queiroz):**  Padronização do armazenamento em nuvem, tramitação segura e execução do descarte automatizado.  
* **DPO (Encarregado de Dados):**  Revisão anual das regras de auditoria do Agente para alinhamento com a LGPD.**6.2. Ciclo de Auditoria**  O Agente passará por revisão técnica anual obrigatória. O redesenho de seus motores deve incorporar sugestões de todas as áreas da Vector Informática, resultados de auditorias externas e atualizações das normas do MGI. Documento aprovado em 11/2022, revisado em 04/2024 para versão 3.0.

