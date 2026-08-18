# AI Visibility — share of voice e sentimento, por plataforma

**M1 × P4.** *A pergunta: quanto do espaço de resposta a marca ocupa em cada assistente, e como
ela é falada lá dentro?*

Fonte: dois relatórios de Desempenho da Marca sobre `loja.electrolux.com.br`, um por plataforma,
88 páginas. Extraídos por `20-normalizado/normalizar_visibility.py` para `ai_visibility.csv`.
Estavam no repositório desde 17/08 e nenhum número deles tinha entrado no material.

---

## 1. O que esta fonte acrescenta

Ela traz uma medida que **nenhuma outra fonte do pacote tem**: *share of voice* em resposta de
IA, por marca e por plataforma. As outras medidas do material respondem quanto da demanda
carrega o nome da marca (cobertura) ou quanto de um tópico um domínio ocupa (ocupação). Esta
responde **quanto do espaço de fala a marca toma quando o assistente responde**.

Também é a primeira fonte a medir sentimento com série temporal e a decompor o que puxa a
percepção para cima e para baixo.

**Ressalva de escopo, e ela importa.** O relatório é construído sobre o domínio da loja,
`loja.electrolux.com.br`, não sobre a marca Electrolux inteira. As perguntas em que a loja
aparece são majoritariamente de compra, canal e serviço em torno da compra. Isso não invalida a
leitura, mas explica por que ela é mais favorável à marca do que as demais do pacote.

---

## 2. Share of voice: a marca lidera nas duas plataformas

| Marca | ChatGPT | Google AI Mode |
|---|---:|---:|
| **Electrolux** | **14,7%** | **12,4%** |
| Consul | 12,1% | 10,8% |
| Brastemp | 8,8% | 11,6% |
| Samsung | 5,9% | 3,2% |
| Midea | 4,7% | 1,2% |
| **Outras** | **53,7%** | **60,5%** |

**A Electrolux lidera em share of voice nos dois assistentes.** É a quinta medida independente
do pacote a apontar a mesma coisa — cobertura por nome de tópico, citação nas respostas, tráfego
de LLM, presença agregada e agora share of voice.

**E "outras" é maioria absoluta nas duas.** 53,7% e 60,5% do espaço de fala não pertence a
nenhuma das cinco marcas medidas. É a quarta medida independente a dizer que o espaço é
majoritariamente de ninguém, agora em unidade diferente das anteriores.

**A ordem do segundo lugar inverte entre plataformas.** No ChatGPT, Consul é segunda (12,1%) e
Brastemp terceira (8,8%). No Google AI Mode, Brastemp é segunda (11,6%) e Consul terceira
(10,8%). Nenhuma leitura de posição competitiva em IA se sustenta sem separar plataforma.

---

## 3. O sentimento inverte entre plataformas, e é a leitura mais desconfortável

| | ChatGPT | Google AI Mode |
|---|---:|---:|
| Sentimento favorável | **41%** | **71%** |

A mesma marca, no mesmo dia, com percepção quase oposta dependendo do assistente. Não é ruído
de amostra: são dois relatórios completos, com série temporal, gerados pela mesma ferramenta.

E dentro do ChatGPT o relatório mede o vão contra o concorrente direto: **40,54% de menções
positivas para a Electrolux contra 53,12% da Consul**. É a segunda fonte independente a colocar
a Consul acima da Electrolux em percepção — a leitura de sentimento das 150 perguntas já dava
70,5 contra 58,1.

**Consequência de planejamento.** Qualquer meta de percepção em IA precisa ser definida por
plataforma. Uma média entre 41% e 71% descreveria uma marca que não existe.

---

## 4. O que puxa a percepção, segundo o próprio relatório

O relatório do ChatGPT decompõe em sete fatores de força e sete de fraqueza. O padrão é nítido.

**O que sustenta:** conveniência e mecânica de loja (cashback, carteira digital, assinatura
recorrente de filtro), inovação de produto (VaporBake, PerfectCook360, fornos air fryer),
**serviços oficiais em torno da compra** (instalação, assistência técnica, garantia estendida
com rede autorizada), foco em eficiência energética e inverter, confiança de canal — comprar no
oficial é mais seguro —, sortimento especializado e logística reversa.

**O que trava, e tudo tem a mesma natureza:** complexidade de garantia e reembolso, frete grátis
e parcelamento condicionais, cobertura de serviço restrita por CEP, informação técnica
incompleta na página, regras de cashback percebidas como restritivas, estoque indisponível, e
**a loja oficial nem sempre ter o melhor preço contra marketplaces**.

Nenhum dos sete pontos de fraqueza é sobre produto. **Todos são sobre regra, condição e
cobertura de serviço.** A marca não tem um problema de percepção de produto em IA; tem um
problema de percepção de *letra miúda*.

---

## 5. A nuance que corrige o material

O relatório afirma que **a Electrolux já é percebida como marca de conveniência e serviço
completo** dentro do ChatGPT, com 36 menções de conveniência, 9 de instalação e 8 de compra
protegida. Isso parece contradizer a leitura central do material, de que a marca está ausente
do território de posse.

Não contradiz, e a distinção precisa estar no deck:

- **O que a marca já tem** é percepção de serviço **em torno da compra** — instalação, garantia,
  logística reversa, canal seguro. Isso aparece quando alguém pergunta sobre comprar.
- **O que a marca não tem** é presença nas perguntas de **vida com o produto** — como limpar,
  por que não gela, qual peça trocar. Ali a cobertura é de 2,58% e a citação é zero nas
  famílias de manutenção.

O ativo existe e está no lugar errado da jornada. Isso é uma notícia melhor do que "a marca não
tem serviço": significa que há **repertório a mover**, não repertório a construir.

---

## 6. Onde as perguntas se concentram

Distribuição de tópico das perguntas no ChatGPT:

| Território | Peso |
|---|---:|
| Cocção (fogões, fornos, cooktops, micro-ondas, coifas, air fryer) | 26,5% |
| Lavanderia e lava-louças | 24,5% |
| Clima, água e limpeza (ar-condicionado, purificador, aspirador) | 20,5% |
| **Loja, serviços, preço e políticas** | **13,5%** |
| Refrigeração e freezers | 9% |
| Pequenos eletros e preparo | 6% |

**13,5% das perguntas são sobre loja, serviço, preço e política** — o território de ecossistema
do briefing, já existindo como assunto espontâneo em IA. É o quarto maior bloco, acima de
refrigeração.

E o relatório registra que mais de 60% das consultas tratam de energia, água e kWh, e que uma em
cada três cita instalação, garantia, descarte ou filtro.

---

## 7. Limites

- **O escopo é o domínio da loja**, não a marca inteira. A leitura é mais favorável por isso.
- **Share of voice e cobertura não se comparam.** Uma mede espaço de fala na resposta; a outra,
  quanto da demanda carrega o nome da marca. Denominadores diferentes.
- **O conjunto medido tem cinco marcas.** Hisense e Haier ficam fora, e "outras" agrega tudo o
  mais, inclusive varejistas.
- **O critério de sentimento não é publicado.** Serve como comparação relativa entre marcas na
  mesma medida e entre plataformas, não como nível absoluto.
- **Os fatores de força e fraqueza são texto gerado pela ferramenta**, não medição. Entram como
  leitura qualitativa declarada.

---

## O que eu faria a seguir

1. **Levar a inversão de sentimento entre plataformas para o deck.** 41% contra 71% na mesma
   marca é o tipo de dado que muda como a liderança define meta, e nenhuma outra fonte do
   pacote enxergaria isso.
2. **Corrigir a leitura de posse no material com a nuance do §5.** A marca tem repertório de
   serviço na cabeça do assistente; ele está preso ao momento da compra.
3. **Usar os sete pontos de fraqueza como brief direto para o entregável de commerce.** Todos
   são de regra e condição, e todos são resolvíveis sem tocar em produto.
