# Pedido de dados — o que falta para o job de search

Complementa o `dicionario-de-dados.md`. Lista, em ordem de criticidade, os exports que faltam,
com a pergunta que cada um destrava e a consequência de não tê-lo. Formato pensado para ser
enviado direto a quem opera as ferramentas.

Base atual: 16 arquivos canônicos, 4.941 keywords únicas, 4.000 prompts, 150 perguntas de IA
× 5 provedores, 12 meses de AI referrals.

---

## Achado que motiva este pedido

Os sete exports de keyword foram puxados com **seed de marca** — `eletrolux`, `brastemp`,
`consul`, `Hisense`, `+midea`, `geladeira samsung` — mais `geladeira` como genérica de
categoria. A consequência é estrutural: o pacote mede muito bem a **marca de produtos** e é
cego para o **ecossistema**, que é justamente o pedido central do case Brasil.

Medida na base atual (4.952 linhas, volume somado 12.876.830):

| Família de "vida com o produto" | Keywords | Volume | % do volume |
|---|---:|---:|---:|
| Peça e consumível | 187 | 168.900 | 1,31% |
| Assistência e reparo | 145 | 118.530 | 0,92% |
| Defeito e erro | 25 | 49.250 | 0,38% |
| Uso e como fazer | 62 | 18.420 | 0,14% |
| Garantia | 11 | 3.780 | 0,03% |
| Frentes nomeadas (Instala, Projeta, Cuida, Pro, Shopclub, Outlets, Afiliados) | 7 | 3.720 | 0,03% |
| Instalação | 1 | 260 | 0,00% |
| Consumo e eficiência | 1 | 590 | 0,00% |
| Receita | 0 | 0 | 0,00% |

Tudo somado: **cerca de 3,5% do volume**. O briefing nomeia "pesquisar uma receita" como ponto
de entrada da marca, e a base tem **zero** keywords de receita.

**Leitura correta:** isso não é evidência de que a demanda de ecossistema não existe. É
evidência de que o dado não foi puxado para encontrá-la. **H1 não é testável com o pacote
atual** — o Tier 1 abaixo é o que a torna testável.

---

## Tier 1 — sem isto, H1 e o pedido central do briefing ficam sem base

| # | Export | Ferramenta | Destrava |
|---|---|---|---|
| 1 | **Keyword universe de serviço e pós-compra, NÃO-branded.** Seeds sugeridas: assistência técnica, conserto, autorizada, peça de reposição, filtro, correia, resistência, instalação, garantia, manutenção, "não gela", "não centrifuga", "não seca", "erro", "como limpar", "como usar", "manual", consumo de energia, kWh, selo Procel, descarte, reciclagem, receita, modo de preparo — cruzadas com as categorias do portfólio | SEMrush Keyword Magic | O tamanho real da demanda de ecossistema. É o teste de H1 |
| 2 | **Keyword universe das frentes nomeadas:** Instala, Projeta, Cuida, Electrolux Pro, Shopclub, Outlets, Afiliados, Coleta Consciente | SEMrush Keyword Magic | Se as frentes que o cliente quer conectar existem em busca, e com que peso |
| 3 | **Organic Positions dos captores que não são fabricantes:** Mercado Livre, Magalu, Amazon, Casas Bahia, Americanas, YouTube e portais de conteúdo doméstico, nas keywords do item 1 | SEMrush Organic Research | Quem captura hoje a demanda do ecossistema. É o conjunto competitivo do ecossistema, distinto do de produto |

## Tier 1B — Haier: a ameaça que o briefing nomeia e o dado não cobre

O briefing dedica um slide à chegada da Haier ao Brasil, com **confiança de pós-venda** como
eixo declarado: mais de 1.000 pontos técnicos, mais de 200 posições de atendimento, expertise
em casa conectada, público A/B, expectativa de R$ 500 milhões no primeiro ano. Em comunicação,
aparecem celebridade (Eliana, para construir familiaridade) e patrocínio esportivo (Liverpool
Football Club). **A Haier não está em nenhum arquivo do pacote.**

Vale rodar, e o teste informa a decisão nos dois resultados possíveis: demanda de serviço e
confiança subindo significa que o entrante já ocupa o território e a urgência é alta; demanda
plana significa território vago e janela para a Electrolux chegar antes.

**Trava de leitura, para constar antes de o dado chegar:** volume absoluto baixo de um
entrante recente **não** é evidência de ausência de ameaça. Marca nova com mídia pesada aparece
primeiro em busca de marca e só depois em busca de categoria. O que decide é a **inclinação**
(campo `Trend`, 12 pontos) e a **composição** da demanda, não o nível.

### Especificação do export

| Corte | Seeds sugeridas | O que testa |
|---|---|---|
| Marca | `haier`, `haier brasil`, `haier eletrodomésticos`, variações e erros de grafia frequentes | Base de familiaridade construída |
| Marca × categoria | `haier` cruzado com as categorias em que a marca opera no Brasil | Se a familiaridade virou demanda de categoria |
| Marca × confiança e serviço | `haier assistência técnica`, `haier garantia`, `haier é boa`, `haier vale a pena`, `haier confiável`, `haier durabilidade` | **O eixo declarado da estratégia deles.** É o corte que testa a tese da Haier |
| Marca × comunicação | `haier eliana`, `haier liverpool` | Se o investimento em familiaridade produz assinatura em busca |

Rodar as **mesmas quatro famílias para a Electrolux**, para haver base pareada. Sem par, a
comparação de vãos não se sustenta.

`[a confirmar: em quais categorias a Haier opera no Brasil, e se a operação usa outras marcas
do grupo. Não presumir — puxar a lista com o time da conta antes de definir os seeds.]`

### O que a comparação pareada revela

O cliente declarou seu próprio desafio como "converter reconhecimento de marca em intenção de
compra no momento da decisão". Medir o mesmo vão na Haier, com o mesmo instrumento, responde
se o entrante resolveu o problema que a Electrolux ainda não resolveu — ou se está pagando
para encher um funil que também não converte. As duas respostas mudam a recomendação.

### Complemento barato, no mesmo pedido

Incluir **Haier** nas marcas rastreadas do relatório de AI answers, hoje limitado a Electrolux,
Consul, Brastemp, Midea e Samsung. Para um entrante recente, a presença em resposta de IA tende
a divergir da presença em busca — os modelos podem estar atrasados por defasagem de dado, ou
adiantados por peso de PR recente. A divergência, se existir, é diagnóstico.

### Observação lateral, fora do pedido da Haier

O conjunto atual tem Samsung mas **não tem LG**, embora a LG apareça nos quadros de
posicionamento e de conjunto competitivo do próprio briefing. A assimetria é estranha e o custo
de corrigir é um export. `[a confirmar: se a ausência de LG foi escolha ou omissão.]`

## Tier 2 — sem isto, "gap" continua sendo inferência e não medida

| # | Export | Ferramenta | Destrava |
|---|---|---|---|
| 4 | **Organic Positions** de `loja.electrolux.com.br` e `electrolux.com.br`, e dos domínios concorrentes | SEMrush Organic Research | Onde a marca de fato ranqueia. Hoje só sabemos quem está no top 10 por keyword, não a posição da Electrolux |
| 5 | **Organic Pages** dos mesmos domínios | SEMrush Organic Research | Quais páginas capturam tráfego, e se as frentes nomeadas têm página que ranqueia |
| 6 | **Domain Overview / Traffic** comparativo dos seis players | SEMrush | Share orgânico sobre base comparável — hoje a amostra é assimétrica (Brastemp 2.000 linhas vs Midea 101) |

## Tier 3 — completa a leitura de AI search

| # | Export | Ferramenta | Destrava |
|---|---|---|---|
| 7 | **AI answers BRANDED** | SEMrush AI | Só veio o não-branded. Falta o que a IA responde quando perguntam pela Electrolux pelo nome |
| 8 | **"Desempenho da marca" nas plataformas faltantes:** Perplexity, Gemini, AI Overview | SEMrush AI | Vieram só ChatGPT e Google AI Mode. Sem as demais, a leitura de presença no filtro fica parcial |
| 9 | **"Desempenho da marca" dos concorrentes** | SEMrush AI | O relatório existe só para `loja.electrolux.com.br`. Sem o dos concorrentes, share em IA depende de uma fonte só |
| 10 | **Fontes citadas em formato tabular** — quais domínios cada modelo cita, por pergunta | SEMrush AI / equivalente | **Responde quem constrói autoridade em cima da marca.** Hoje há `sources_count`, mas não a lista de fontes |
| 11 | **AI referrals com Samsung e Hisense**, e com as demais LLMs | SimilarWeb | Fecha a assimetria de cobertura entre as fontes |

## Tier 4 — liga busca a negócio, que é o que o briefing cobra

O RFP pede explicitamente conversão, receita na loja e ROAS. Sem este bloco, o job termina em
demanda e presença e nunca chega em negócio.

| # | Export | Fonte | Destrava |
|---|---|---|---|
| 12 | **Analytics de `loja.electrolux.com.br`:** sessões por canal, conversão, receita, jornada | GA4 do cliente | O elo entre busca e venda |
| 13 | **Google Ads:** share de impressão, CPC real, termos de busca, conversões | Conta do cliente | O `CPC (USD)` do SEMrush é estimativa de mercado. Nenhuma decisão de verba se sustenta nele |
| 14 | **Shopping / PLA** | Google Merchant / Ads | `Popular Products` aparece com frequência nos SERP features; sem isso a disputa transacional fica ilegível |
| 15 | **Venda e sell-out** por categoria | Cliente | Fecha o ciclo com P1 e permite falar de incrementalidade em vez de tráfego |
| 16 | **SimilarWeb completo:** traffic overview, mix de canais, audience overlap e destinos | SimilarWeb | Quanto do tráfego da categoria passa por marketplace antes de chegar na marca |

## Tier 5 — fora do escopo deste job, mas nomeado para não ficar invisível

- **Escuta social** (P9): o dado de busca não enxerga **demanda latente** — ponto de entrada que
  o consumidor ainda não sabe verbalizar não vira keyword. Criar categoria é parte do desafio de
  ecossistema, e essa lente é a que fecha o vão.
- **SOV pago** (P2, Kantar IBOPE): para o triângulo de share ficar completo.

---

## Pendências de metadado dos arquivos já recebidos

1. `[a confirmar]` Critério de corte de cada export de keyword — top N por volume, filtro de
   seed, ou outro. Sem isso, comparação de volume entre marcas fica sem base.
2. `[a confirmar]` Janela temporal dos exports de keyword. Há série de 12 pontos em `Trend`, mas
   sem data de início declarada.
3. `[a confirmar]` Ferramenta de origem dos quatro arquivos `prompts_by_topic`. O padrão de nome
   e as colunas não correspondem aos demais exports do SEMrush.
4. `[a confirmar]` Confirmação de que o AI referrals é SimilarWeb — inferido pelo formato do
   export, confiança média.

---

## O que dá para fazer sem esperar nada disto

O Tier 1 destrava H1, mas não bloqueia o job inteiro. Com o pacote atual já é possível avançar
em: taxonomia de pontos de entrada sobre a demanda de aquisição; leitura de intenção e de
sazonalidade; mapa de quem ocupa o top 10 nas keywords existentes; e a leitura completa de AI
search em ChatGPT e Google AI Mode, incluindo posição e sentimento por marca nas 150 perguntas
não-branded.
