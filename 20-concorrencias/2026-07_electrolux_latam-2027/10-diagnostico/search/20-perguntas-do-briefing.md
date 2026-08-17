# Etapa 2 — O briefing traduzido em perguntas

Critério de aceitação do job. Cada pergunta nasce de um ponto explícito do briefing ou dos
cases, e carrega a prática que a responde, o cluster de entregável do RFP que ela serve, a
fonte que a responde e o **status com o pacote de dados atual**.

No fim do job, cada linha desta tabela sai marcada como respondida, respondida em parte ou
declarada não respondível. Nenhuma some.

**Status agregado: 34 perguntas — 15 respondíveis, 12 parciais, 7 não respondíveis hoje.**

Legenda de status: **OK** respondível com o pacote atual · **PARC** respondível em parte, com
lacuna declarada · **NÃO** exige dado do `pedido-de-dados.md`.

---

## Contexto que o briefing acrescenta e que reposiciona duas perguntas

**1. O vão da marca no Brasil.** O BHT Kantar Q1/2026 mostra awareness alto e consideração
(T2B) bem abaixo, em MDA e em SDA. O desafio declarado pelo cliente é literalmente "moving
beyond awareness, converting brand recognition into purchase intent at the moment of decision".
Busca é uma das poucas fontes que enxerga esse momento de decisão em escala.

**2. A ameaça asiática entra pelo serviço.** O briefing dedica um slide à Haier chegando ao
Brasil, e o eixo declarado dela é **confiança de pós-venda**: mais de 1.000 pontos técnicos,
mais de 200 posições de atendimento, expertise em casa conectada, público A/B, expectativa de
R$ 500 milhões no primeiro ano. Isso muda o enquadramento de H1: o ecossistema não é só a
oportunidade de crescimento da Electrolux — é o terreno onde o novo entrante decidiu atacar.
Uma tese de ecossistema deixa de ser ambição de posicionamento e passa a ser **defesa de
território**.

---

## A · Ecossistema — o pedido central do case Brasil

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| A1 | Qual o tamanho da demanda de "vida com o produto" frente à demanda de aquisição? | P4 | Brand Strategy | keywords de serviço não-branded | **NÃO** |
| A2 | Quais famílias de serviço têm demanda relevante e quais não têm? | P4 | Ecosystem | keywords | **PARC** — só enxerga o que menciona a marca |
| A3 | As frentes nomeadas (Instala, Projeta, Cuida, Pro, Shopclub, Outlets, Afiliados) existem em busca? | P4 | Ecosystem | keywords | **PARC** — 7 keywords, 0,03% do volume |
| A4 | Quem captura hoje a demanda de serviço? | P4 + P2 | Ecosystem | Organic Positions dos captores | **NÃO** |
| A5 | Em perguntas de uso, manutenção e serviço feitas à IA, a Electrolux é citada? | P4 | Ecosystem | AI answers + 4.000 prompts | **OK** |
| A6 | Quais fontes os modelos citam nessas respostas, e quanto disso é propriedade da marca? | P4 | Content & Influence | `sources_count` sem a lista de fontes | **PARC** |
| A7 | Existe demanda que já conecta categorias entre si — a "narrativa única" pedida? | P4 | Brand Strategy | co-ocorrência em keywords e prompts | **OK** |

## B · Marca, posicionamento e o vão awareness → consideração

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| B1 | Qual a proporção entre busca branded e non-branded, e o que isso diz sobre o vão do BHT? | P4 + P1 | Brand Strategy | keywords, campo Intent | **OK** |
| B2 | Quando a categoria é buscada sem marca, quem aparece no top 10? | P4 + P2 | Brand Media | `Competitor on TOP 10` | **OK** |
| B3 | A Electrolux é buscada como marca (navegacional) ou como solução de um problema? | P4 | Brand Strategy | Intent + estrutura das queries | **OK** |
| B4 | Qual o sentimento da marca nas respostas de IA, contra os concorrentes? | P4 + P1 | Brand Strategy | AI answers, `sentiment score` | **OK** |
| B5 | Preço aparece como atributo dominante na demanda da marca — coerente com o "justified premium" do briefing? | P4 + P1 | Brand Strategy | keywords de preço e comparação | **OK** |

## C · Território — as perguntas que o cliente fez com estas palavras

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| C1 | Quais territórios podem criar diferenciação mais forte? | M1 × P4 | Brand Strategy | taxonomia de pontos de entrada + AI answers | **PARC** |
| C2 | Como produtos, serviços e experiências podem se reforçar mutuamente? | P4 | Ecosystem | co-ocorrência produto × serviço | **PARC** |
| C3 | Como a marca permanece relevante além dos momentos de compra? | P4 | Ecosystem | demanda pós-compra | **NÃO** |
| C4 | Quais pontos de entrada de categoria existem, e qual o peso de cada um? | M1 × P4 | Brand Strategy | keywords + prompts | **PARC** — completo em aquisição, cego em pós-compra |

## D · Competição

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| D1 | Qual a posição relativa da Electrolux por ponto de entrada, contra o conjunto declarado? | P2 + P4 | Brand Media | keywords | **PARC** — amostra assimétrica entre marcas |
| D2 | As marcas asiáticas já aparecem na demanda, e em quais pontos de entrada? | P2 | Brand Strategy | Hisense e Midea nos arquivos | **PARC** — **Haier não está no pacote** |
| D3 | A Haier já disputa a demanda de serviço e pós-venda, que é o eixo declarado dela? | P2 + P4 | Ecosystem | — | **NÃO** — falta Haier e faltam seeds de serviço |
| D4 | Quem são os captores que não são fabricantes — marketplace, conteúdo, assistência independente? | P2 | Commerce | `Competitor on TOP 10` | **PARC** |
| D5 | Como a marca se posiciona contra os concorrentes dentro das respostas de IA? | P4 | Brand Strategy | AI answers, posição e sentimento | **OK** |

## E · Por cluster de entregável do RFP

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| E1 | Quais atributos aparecem espontaneamente associados à marca nas respostas de IA? | P4 | Brand Strategy | texto integral das 150 respostas | **OK** |
| E2 | Quais pontos de entrada têm volume alto e presença de `AI Overview` no SERP? | P5 + P4 | Brand Media | `SERP Features` | **OK** |
| E3 | Quais keywords têm intenção transacional com alta densidade competitiva? | P6 | Performance Media | Intent + Competitive Density + CPC | **OK** |
| E4 | Que perguntas as pessoas fazem que a marca poderia responder com conteúdo próprio? | P9 + P4 | Social & Content | 4.000 prompts com resposta | **OK** |
| E5 | A demanda migra para marketplace antes de chegar na marca? | P7 | Retail Media | `Competitor on TOP 10` | **PARC** |
| E6 | A loja própria aparece na busca da categoria, ou só na busca da marca? | P8 | Commerce | keywords + AI referrals | **PARC** |

## F · AI search

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| F1 | Em quais perguntas e com que posição a marca aparece, por plataforma? | P4 | Brand Media | AI answers, 5 provedores | **OK** |
| F2 | O comportamento difere entre ChatGPT, Gemini, Google AI Mode e Perplexity? | P4 | Brand Media | AI answers + os dois PDFs | **OK** |
| F3 | O tráfego real vindo de LLM está crescendo, e como se compara ao dos concorrentes? | P4 + P8 | Performance | AI referrals, 12 meses | **OK** |
| F4 | O que a IA responde quando perguntam pela Electrolux pelo nome? | P4 | Brand Strategy | — | **NÃO** — só veio non-branded |
| F5 | Quais domínios os modelos usam como autoridade na categoria? | P4 | Content & Influence | — | **PARC** |

## G · Negócio

| # | Pergunta | Prática | Cluster RFP | Fonte | Status |
|---|---|---|---|---|---|
| G1 | Qual o valor da demanda não capturada, em receita potencial? | P1 + P6 | Performance | — | **NÃO** — exige CPC real e taxa de conversão |
| G2 | Qual o ROAS e a contribuição de busca para a receita da loja? | P1 + P6 | Performance | — | **NÃO** — exige GA4 e dado de venda |

---

## Como esta lista governa o resto do job

- Nenhuma análise entra no entregável sem estar amarrada a pelo menos uma destas perguntas.
- O que a análise descobrir **fora** desta lista vai para *achados não solicitados*, no passe
  aberto, e depois é amarrado ao ponto do briefing que ele acabar respondendo.
- As sete perguntas marcadas **NÃO** não são desculpa: elas viram, no entregável final, uma
  seção de "o que este dado não responde e o que resolveria" — o que é postura de método na
  banca, e não fraqueza.
- Duas delas — **A1** e **C3** — são o núcleo de H1. Enquanto estiverem sem dado, H1 permanece
  hipótese declarada e não sai como achado.
