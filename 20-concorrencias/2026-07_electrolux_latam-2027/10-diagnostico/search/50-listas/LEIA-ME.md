# Lista de keywords — a cauda não-branded

**2.000 keywords**, prontas para rodar. Arquivos:

- `lista-cauda-nao-branded.txt` — só as keywords, uma por linha, para colar na ferramenta
- `lista-cauda-nao-branded.csv` — com prioridade, família, categoria e o racional de cada uma
- `gerar_lista.py` — o gerador, reexecutável e auditável

---

## O que esta lista é

É o **quadrante ausente** do dataset atual. O pacote que temos cobre a cabeça não-branded
(65 keywords, todas de uma a três palavras) e a cauda branded (4.899 keywords com nome de
marca). Falta a **cauda não-branded**, e é ali que vive toda a demanda de serviço, uso, defeito,
peça e como-fazer — porque ninguém digita "assistência técnica" em duas palavras: digita
"assistência técnica máquina de lavar campinas".

Sem ela, a tese do ecossistema é uma frase. Com ela, é um número.

## Como foi construída

Combinatória de **famílias × categorias × modificadores**, no vocabulário real extraído do
corpus de 4.749 prompts e perguntas de IA — não em suposição. Três estruturas vieram do dado e
não teriam sido adivinhadas:

1. **A busca de assistência é geolocalizada.** O padrão observado é
   `assistência técnica <categoria> <cidade>`. A lista cruza 8 categorias com 36 cidades.
2. **A busca de peça é por componente específico**, não por "peça". Daí `borracha da porta
   geladeira`, `correia máquina de lavar`, `filtro de carvão coifa`.
3. **Manual é família própria**, não subitem de uso. `manual <categoria> pdf` é contato de
   pós-compra que hoje a marca entrega a terceiros.

**Acentuação preservada.** A base do SEMrush trata formas acentuadas e não acentuadas como
keywords distintas — no próprio dataset atual, `microondas` (550.000) e `micro ondas` (33.100)
aparecem separadas. A lista usa a forma acentuada como principal e inclui as variantes sem
acento das categorias de maior volume no bloco de sinônimos.

## Estrutura de prioridade

A lista está **ordenada por prioridade**. Se a ferramenta só aceitar um lote menor, corte pelo
fim: os primeiros são os que mais importam.

| P | Família | n | Por que nesta posição |
|---|---|---:|---|
| 1 | Defeito | 232 | Maior intenção de serviço e a família mais invisível no dataset atual (0,13% do volume branded) |
| 2 | Assistência técnica | 525 | Geolocalizada; é onde a marca disputa contra assistência independente e marketplace |
| 3 | Manual e uso | 123 | Contato de pós-compra hoje entregue a terceiro |
| 4 | Peça e consumível | 232 | Cauda de altíssima intenção transacional; a família mais promissora para D2C |
| 5 | Manutenção e cuidado | 71 | Território de conteúdo e relacionamento recorrente |
| 6 | Instalação | 75 | Frente nomeada do cliente (Instala) |
| 7 | Consumo e eficiência | 73 | Única família de serviço com sinal já visível no dataset atual |
| 8 | Garantia | 23 | Produto de serviço vendável (extensão de garantia) |
| 9 | Descarte e sustentabilidade | 16 | Território declarado com **zero** demanda no corpus de IA — precisa ser confirmado em busca |
| 10 | Receita e preparo | 21 | O briefing cita "pesquisar uma receita" como ponto de entrada da marca |
| 11 | **Controle branded** | 40 | Deliberado — ver abaixo |
| 12 | Sinônimos e variantes | 80 | Formas alternativas da mesma categoria |
| 13 | Complemento de cobertura | 489 | Fecha lacunas das famílias sub-representadas |

**1.960 não-branded + 40 de controle branded.**

## Por que 40 termos branded numa lista não-branded

Os 40 termos de controle existem para responder uma pergunta que a lista não-branded sozinha
não responde: **quanto da demanda de serviço já menciona a marca?**

Rodando `assistência técnica geladeira` ao lado de `assistência técnica geladeira electrolux`,
a razão entre os dois volumes dá a fatia da demanda que já chega com a marca na cabeça — e a
fatia que está em disputa aberta. Sem esse par, o número não-branded não tem contra o que ser
lido.

Os 10 termos das **frentes nomeadas** — `electrolux cuida`, `electrolux instala`,
`electrolux projeta`, `electrolux pro`, `electrolux shopclub`, `electrolux outlet`,
`coleta consciente electrolux` e outros — fecham o quadrante "anunciado e vago" com medição
direta, em vez de inferência.

## Como rodar

Ferramenta: **SEMrush Keyword Overview em lote**, ou **Keyword Manager**, base `br`.
Não usar Keyword Magic com estes termos como seed — a lista já são keywords finais, não
sementes; expandi-las multiplicaria o volume de linhas sem acrescentar cobertura.

Campos que precisam vir no export, além dos padrão: **Volume**, **Trend** (série de 12 pontos),
**Intent**, **SERP Features**, **Keyword Difficulty**, **CPC**, **Competitive Density**.

Se houver como marcar, peça também **Competitors / Competitor on TOP 10** — no pacote anterior
essa coluna veio vazia em todos os oito arquivos, e é ela que responde quem captura cada
demanda hoje.

## O que esta lista destrava

Rodando esta lista, saem do estado "não respondível" as perguntas que hoje são o buraco do job:

| # | Pergunta | Hoje |
|---|---|---|
| A1 | Qual o tamanho da demanda de "vida com o produto" frente à de aquisição? | não respondível |
| A2 | Quais famílias de serviço têm demanda relevante e quais não têm? | parcial |
| A3 | As frentes nomeadas existem em busca? | parcial |
| C3 | Como a marca permanece relevante além dos momentos de compra? | não respondível |
| C4 | Quais pontos de entrada existem e qual o peso de cada um? | parcial, cego em pós-compra |

E, principalmente: **H1 volta a ser testável.** A hipótese original — de que existe volume
relevante de demanda de vida com o produto hoje capturada por terceiros, e que esse volume é o
tamanho de mercado do ecossistema — depende exatamente deste recorte. Com ele, o argumento
central da resposta ao case Brasil deixa de ser tese e passa a ser medição.

## O que ela ainda não responde

Volume não é captura. Mesmo com esta lista, sem a coluna de competidores ou sem Organic
Positions dos domínios captores, dá para dizer **quanta demanda existe** e não **quem a pega
hoje**. A leitura de "o território está vago" continua apoiada em posicionamento declarado ×
demanda medida, não em share de captura.
