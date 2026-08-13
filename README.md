# Workspace — Direção Executiva de Mídia e Dados | Youdare (Grupo Dreamers)

Ambiente de trabalho da cadeira. O `CLAUDE.md` da raiz é o prompt-mestre: ele carrega
identidade, tese, a matriz de mandatos × práticas, a doutrina de decisão e as regras
inegociáveis em toda sessão do Claude Code aberta neste repositório.

## Como navegar

| Pasta | O que vive aqui |
|---|---|
| `00-cadeira/` | Método, práticas, padrões, stack e benchmarks. O que torna o trabalho reproduzível entre clientes. |
| `10-clientes/` | Uma pasta por cliente, com `CLAUDE.md` próprio e estágios de contexto, dado, planejamento, operação, report e aprendizado. |
| `20-concorrencias/` | Pipeline de pitch em estágios numerados, para cliente novo e para projeto novo em cliente existente. |
| `30-inteligencia/` | Radar de território e cultura, transversal aos clientes. |
| `40-produtos/` | Produtos proprietários em desenvolvimento. |
| `50-engenharia/` | Conectores, pipelines, agentes, scripts, notebooks, modelos de dado e logs de execução. |

## Como começar uma sessão

1. Diga em qual cliente ou concorrência você está trabalhando.
2. O agente lê o `CLAUDE.md` daquela pasta e a pasta da prática envolvida antes de produzir.
3. Toda entrega substantiva abre com a célula da matriz (mandato × prática) e fecha com
   "o que eu faria a seguir".

## Como entregar arquivos ao agente

Material novo de uma concorrência vai para o `_inbox/` daquela pasta. Rode `/ancorar` e o
agente classifica cada arquivo no estágio correto do pipeline, perguntando quando o estágio
não for óbvio (R7).

## Governança de dado

Dados de cliente **são** versionados neste repositório. Credenciais **não**: tokens, chaves de
API, senhas e strings de conexão vão para variável de ambiente ou arquivo local ignorado pelo
git (R6). O `.gitignore` já cobre os padrões mais comuns.
