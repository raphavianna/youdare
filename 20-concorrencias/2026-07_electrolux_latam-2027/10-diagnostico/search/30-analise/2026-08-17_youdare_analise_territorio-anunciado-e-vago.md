# Territórios anunciados e vagos — pré-leitura pelo dado de IA

**M1 × P2+P4.** *A pergunta: quais territórios os players desta categoria declaram ocupar sem
ter demanda atrelada — e o que isso abre para a Electrolux?*

Método: `00-cadeira/metodo/posicionamento-vs-demanda.md`.
Fontes: 4.000 prompts de IA por tópico + 150 perguntas não-branded do AI answers + as bases de
keyword já ancoradas. Reprodução: `30-analise/territorio_analise.py`.

---

## Por que esta leitura foi possível agora

O Tier 1 do pedido de dados — keywords de serviço não-branded — ainda não chegou, e sem ele não
dá para **dimensionar** o território do ecossistema em volume de busca. Mas os 4.000 prompts e
as 150 perguntas não-branded são a única fatia do pacote **que não foi filtrada por nome de
marca**. Eles não dão volume, e dão duas coisas que faltavam: a **composição** do território e
a **linguagem real** com que ele é formulado.

Isto é pré-leitura, não a medição. A medição continua dependendo do Tier 1.

---

## Achado 1 — três territórios anunciados e vagos, não um

O padrão que apareceu na Haier não é dela. É da categoria.

| Território declarado | Quem declara | Demanda medida | Quadrante |
|---|---|---|---|
| **Confiança de pós-venda** — mais de 1.000 pontos técnicos, mais de 200 posições de atendimento | Haier, no briefing | 2,1% do volume de busca da marca | **Anunciado e vago** |
| **Frentes de serviço** — Instala, Projeta, Cuida, Electrolux Pro, Shopclub, Outlets, Afiliados | Electrolux, no briefing e no RFP | **0,03%** do volume de busca da própria marca | **Anunciado e vago** |
| **Sustentabilidade e Coleta Consciente** | Electrolux, citada nas prioridades do relatório de AI visibility | **zero** perguntas em 4.749 do corpus de IA | **Anunciado e vago** |

Três marcas de território, três estruturas montadas, e demanda atrelada perto de zero nas três.

**A leitura que isso permite é mais forte do que a leitura sobre a Haier isolada.** Não estamos
diante de um concorrente que falhou em executar: estamos diante de uma **categoria inteira que
comunica serviço e não construiu demanda por ele**. O território não está disputado — está
desabitado.

Para a defesa, isso muda o argumento. Deixa de ser "a Electrolux deveria falar de ecossistema"
— opinião — e passa a ser "o ecossistema é o único território relevante que nenhum player da
categoria ocupou, e há um entrante que já anunciou que vai tentar". Isso é diagnóstico.

**Ressalva obrigatória, do próprio método:** território sem busca pode ser antecipação ou aposta
errada, e o que separa os dois é a inclinação da série, não o nível. Para as frentes da
Electrolux e para a sustentabilidade eu ainda **não tenho série** — só a foto. Enquanto não
tiver, a leitura correta é "vago", não "promissor". `[a confirmar: série histórica de busca das
frentes nomeadas — sai do Tier 1]`

---

## Achado 2 — a demanda de ecossistema é de base instalada, não de aquisição

Classifiquei o corpus de IA numa taxonomia derivada do próprio dado. Compare o tópico
não-branded com o branded:

| Recorte | n | **Vida com o produto** | Aquisição (comparação + especificação + marca) |
|---|---:|---:|---:|
| Tópico `geladeira` — categoria, **não-branded** | 1.000 | **5,7%** | 45,0% |
| Tópico `eletrolux` — **branded** | 1.000 | **12,1%** | 45,4% |
| 150 perguntas não-branded (AI answers) | 150 | 10,7% | 32,0% |
| Todos os 4.000 prompts | 4.000 | 7,4% | 38,8% |

**A demanda de vida com o produto é mais do que o dobro quando a marca já está na cabeça da
pessoa** — 12,1% no branded contra 5,7% na categoria.

A leitura: quem ainda não escolheu marca pergunta **como comprar**; quem já tem a marca pergunta
**como conviver com o produto**. Isso reposiciona o ecossistema dentro do funil. Ele não é um
território de topo para conquistar consumidor novo — é um território de **retenção, recompra e
defesa de base instalada**, que é precisamente o que o case Brasil pede ao falar em "maior
recorrência de relacionamento" e "relevância além do momento de compra".

E é a mesma razão pela qual a Haier não tem essa demanda: base instalada de cinco meses não
gera pergunta de pós-compra. Não é fraqueza de posicionamento dela — é o calendário. O que
significa que **essa demanda vai aparecer para a Haier**, e a única variável sob controle da
Electrolux é chegar antes.

---

## Achado 3 — o vocabulário real do território

Extraído das perguntas classificadas nas famílias de vida com o produto. É a matéria-prima do
seed list do Tier 1, e ele nasce do que as pessoas efetivamente perguntam, não de suposição.

| Família | Perguntas no corpus | Formulações reais observadas |
|---|---:|---|
| Assistência técnica | 91 | `assistência técnica <marca> <cidade>` · `autorizada <marca> em <cidade>` · `onde encontrar assistência perto de mim` · `como agendar manutenção` |
| Peça e consumível | 82 | `filtro para <modelo>` · `qual lâmpada é certa para minha geladeira <marca>` · `refil <código>` · `filtro hepa` |
| Garantia | 91 | `garantia de procedência` · `quais lojas oferecem melhor suporte ao cliente e garantia` |
| Consumo e eficiência | 111 | `comparar consumo de energia e garantia` · `consumo em kWh` · `selo Procel` |
| Manutenção e cuidado | 40 | `quais cuidados de uso, limpeza e segurança devo ter com <produto>` · `baixa necessidade de manutenção e maior durabilidade` |
| Uso e manual | 31 | `manual <produto> <modelo> pdf` · `como limpar <produto> sem danificar <parte>` |
| Instalação | 23 | `como configurar, instalar e manter <produto>` |
| **Descarte e sustentabilidade** | **0** | — |

Três observações que mudam o seed list:

**A busca de serviço é geolocalizada.** `assistência técnica <marca> <cidade>` e
`autorizada <marca> em <cidade>` são o padrão. O export precisa de seed com cidade, ou vai
subdimensionar a família inteira.

**A busca de peça é por código de modelo.** `refil pe12b`, `filtro para suggar`, `aspirador
erg26`. Isso significa demanda de altíssima intenção, longa cauda, e provavelmente capturada
hoje por marketplace. É a família mais promissora para D2C.

**Manual é uma porta de entrada subestimada.** `manual ar condicionado electrolux inverter
12.000 btus pdf` é demanda de alguém que já comprou, está com o produto na mão, e vai para o
Google porque não achou na marca. Cada uma dessas buscas é um contato de relacionamento que a
marca está entregando para terceiro.

---

## Limites desta leitura, declarados

- **Cobertura da classificação: 50%.** Cerca de metade do corpus não casou com nenhuma família
  da taxonomia. Os percentuais acima são share do conjunto classificado, não do total. Um
  classificador por expressão regular chega até aqui; classificação confiável nesse volume é
  trabalho de engenharia com amostra auditada e erro medido, e é o que a Etapa 3 precisa
  construir.
- **Prompt de IA não é busca.** O corpus mede a demanda mediada por assistente, que tem
  composição diferente da busca tradicional — tende a ser mais conversacional e mais
  informacional. Usar como proxy de busca superestima a fatia informacional.
- **2,6% do corpus está fora de categoria.** Há prompts em latim, sobre conferência de saúde
  (HIMSS) e sobre serviços médicos dentro dos arquivos `prompts_by_topic`. Foram excluídos das
  contas, mas o achado importa: **o dataset tem contaminação e qualquer share calculado sobre
  ele sem limpeza está errado.** `[a confirmar: origem e método de coleta destes arquivos]`
- **Sem série temporal** para os territórios da Electrolux e para sustentabilidade. Sem
  inclinação, não dá para separar antecipação de aposta errada — só dá para dizer "vago".
- **O corpus de vocabulário tem duplicatas** (as 150 perguntas aparecem uma vez por provedor).
  Isso não afeta as formulações extraídas, mas afetaria contagem — as contagens de share foram
  feitas sobre os conjuntos únicos.

---

## O que eu faria a seguir

1. **Fechar o seed list do Tier 1 com o vocabulário acima**, incluindo os três padrões que eu
   não teria adivinhado: cidade na busca de assistência, código de modelo na busca de peça, e
   `manual` como família própria. Já registrado em `10-dicionario/pedido-de-dados.md`.
2. **Pedir a série histórica das frentes nomeadas** — Instala, Projeta, Cuida, Pro, Shopclub.
   Sem inclinação, o quadrante "anunciado e vago" não se resolve entre antecipação e aposta
   errada, e essa distinção muda a recomendação.
3. **Construir o classificador de verdade na Etapa 3.** 50% de cobertura é o teto de regex; a
   taxonomia precisa de método com erro medido antes de virar número em deck.
