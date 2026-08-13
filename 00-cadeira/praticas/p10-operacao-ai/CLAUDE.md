# P10 · Operação orquestrada por AI

**Pergunta central:** o que nesta operação ainda depende de esforço humano que não exige julgamento humano.

**Componentes:** governança · templates canônicos · planos e cronogramas · backlogs priorizados por impacto · pipelines com contrato de qualidade (frescor, completude, schema) · agentes de operação, incluindo otimização de compra via API das plataformas.

**Escada de autonomia e guardrails:** `../../metodo/autonomia-de-agentes.md`. Toda automação declara seu degrau N0–N4 antes de ir ao ar e preenche a ficha de registro. Automação sem dono humano nomeado não sobe.

**Observabilidade:** todo agente registra em `50-engenharia/logs/` o que fez, por que fez, o estado anterior e o efeito estimado.

**Fronteira com M4:** P10 constrói para dentro, M4 empacota para fora. Rotina estável, valiosa e reproduzível aqui é candidata natural a produto — apontar essa transição faz parte do trabalho.

**Regra de higiene:** pipeline que quebra em silêncio é pior que pipeline que não existe, porque produz report confiante e errado.
