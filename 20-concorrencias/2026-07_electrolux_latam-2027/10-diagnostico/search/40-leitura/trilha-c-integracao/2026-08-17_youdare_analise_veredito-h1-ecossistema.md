# Veredito de H1 — o território do ecossistema, medido

> **PROVISÓRIO — trilha C, integração.** Este documento cruza busca e IA, e foi produzido
> **antes** da regra de isolamento entre as fontes. Ele permanece porque o trabalho é válido,
> mas está sujeito a revisão depois que as trilhas A (busca isolada) e B (IA isolada)
> existirem de forma independente. Se qualquer das trilhas isoladas contradisser algo aqui,
> **a versão isolada prevalece**. Ler junto com `40-leitura/trilha-a-search/`.

**M1 × P4.** *A pergunta: existe demanda de "vida com o produto" fora da marca, qual o tamanho
dela, e o que isso sustenta na resposta ao case Brasil?*

Fontes: `2026-08-17_semrush_keywords_cauda-nao-branded.csv` (a lista de 2.000 keywords, rodada)
+ `00-raw/ai-search/topicos/` (10 arquivos de tópicos de IA com volume) + o dataset normalizado.

---

## Veredito

**H1 confirma-se na existência e não se sustenta na magnitude — e a magnitude nunca foi o
argumento certo.**

O território existe, é mensurável e está desocupado. Mas ele **não é grande em volume**:
representa 1,71% da demanda total medida em busca e 5,2% da demanda de categoria em IA. Quem
for à banca dizer que há um oceano de demanda escondida vai ser desmentido pelo primeiro
analista do cliente que puxar os números.

O que o dado sustenta é mais estreito e mais forte: **o ecossistema é um território barato,
desimpedido, informacional e recorrente — e a marca desaparece dele exatamente no momento em
que o consumidor mais precisa dela.**

---

## 1. O tamanho, medido

Rodamos 2.000 keywords não-branded construídas a partir do vocabulário real do corpus de IA.
Resultado: **519 com volume, somando 223.890 buscas/mês.**

| Família | Keywords | Com volume | Volume/mês | % |
|---|---:|---:|---:|---:|
| Peça e consumível | 437 | 75 | **54.550** | 24,4% |
| Assistência técnica | 573 | 121 | **41.510** | 18,5% |
| Instalação | 75 | 28 | **34.420** | 15,4% |
| Manutenção e limpeza | 103 | 41 | 27.000 | 12,1% |
| Defeito | 404 | 75 | 17.960 | 8,0% |
| Controle branded | 40 | 27 | 16.290 | 7,3% |
| Sinônimos | 80 | 45 | 12.100 | 5,4% |
| Manual e uso | 155 | 52 | 8.420 | 3,8% |
| Consumo e eficiência | 73 | 38 | 8.120 | 3,6% |
| Receita | 21 | 6 | 3.010 | 1,3% |
| Garantia | 23 | 5 | 290 | 0,1% |
| Descarte | 16 | 6 | 220 | 0,1% |

**223.890 é piso, não teto.** Foram 2.000 formulações curadas à mão, não a cauda inteira; só
26% retornaram dado, e o Brasil tem milhares de cidades além das 36 que testamos. O número
real é maior — mas não é ordem de grandeza maior, e é isso que importa para a recomendação.

**Proporção contra a demanda total medida:** 223.890 de 13,09 milhões = **1,71%**.

Em IA, com 5.947 tópicos únicos: **945.286 de volume em vida com o produto, 5,2% da demanda de
categoria.** A ordem de grandeza é consistente entre as duas fontes, com a IA mostrando o
território maior — coerente com assistente ser mais usado para pergunta do que para compra.

---

## 2. Por que volume é a métrica errada aqui

Comparar o ecossistema com a demanda de aquisição por volume é comparar coisas que se compram
de formas diferentes e a preços diferentes.

| Recorte | Keywords | Volume | **KD** | **CPC** | Intenção dominante |
|---|---:|---:|---:|---:|---|
| **Cauda de ecossistema** | 519 | 223.890 | **21,8** | $0,29 | **Informational 70%** |
| Cabeça de categoria | 65 | 6.869.800 | **47,7** | $0,15 | Commercial 62% |
| Cauda branded | 4.900 | 5.999.450 | 32,2 | $0,39 | Informational 58% |

**A dificuldade de ocupar o território de ecossistema é 2,2x menor que a das cabeças de
categoria.** E 70% da intenção é informacional, o que significa que ele se ocupa com
**conteúdo**, não com leilão — a moeda de entrada é produção editorial, não CPC.

Traduzindo para a decisão de verba: disputar `geladeira` (823.000 buscas, KD 47,7) é caro,
permanente e contra todo mundo. Ocupar `instalação de ar condicionado` (22.200, KD baixo) é
barato, durável e contra quase ninguém. **A pergunta não é qual território é maior. É qual real
marginal rende mais** — e é a doutrina D6 aplicada a território, não a canal.

E há um elo com AI search: **22% das keywords da cauda já disparam AI Overview.** O território
que a marca não ocupa em conteúdo é justamente onde o filtro de IA está sendo montado agora,
com fontes de terceiros.

---

## 3. O achado mais forte: a demanda existe, a frente existe, e elas não se encontram

O cliente criou frentes nomeadas para servir esse território. Medimos as duas pontas.

| Território | Demanda não-branded | Frente da marca | Razão |
|---|---:|---|---:|
| Instalação | `instalação de ar condicionado` **22.200** | `electrolux instala` **480** | **46x** |
| Assistência | `conserto de` geladeira, lavadora, fogão e ar-cond. **25.600** | `assistência técnica electrolux` **5.400** | 4,7x |
| **Todo o ecossistema** | **223.890** | soma das frentes nomeadas **8.250** | **27x** |

Frentes nomeadas, uma a uma: `electrolux outlet` 4.400 · `electrolux cuida` 2.400 ·
`electrolux instala` 480 · `electrolux projeta` 320 · `electrolux shopclub` 320 ·
`garantia estendida electrolux` 170 · `electrolux pro` 140 · `coleta consciente electrolux` 20 ·
`peça original electrolux` **0**.

**Correção de um número que publiquei antes.** Eu havia estimado as frentes nomeadas em 0,03%
do volume da marca, a partir da base branded — que não continha esses termos. Medido
diretamente, elas somam 8.250/mês, ou **7,5% da busca pelo termo `eletrolux`** (110.000). São
maiores do que eu disse, e continuam pequenas frente à demanda que existiriam para atender.

`instalação de ar condicionado` sozinha tem **46x mais demanda que a frente inteira criada
para instalação**. Isso não é um problema de comunicação de submarca. É a demonstração de que
a estrutura foi construída e a porta de entrada nunca foi.

**Sustentabilidade fica confirmada como território anunciado e vago:** `coleta consciente
electrolux` tem 20 buscas/mês e a família de descarte inteira soma 220 — 0,1% da cauda.

---

## 4. O achado que muda o argumento: quando quebra, ninguém lembra da marca

Os 40 termos de controle branded existiam para medir que fatia da demanda de serviço já chega
com a marca na cabeça. **Média dos pares: 40,4% branded — ou seja, 60% da demanda de serviço
está em disputa aberta.** Mas a média esconde o essencial, que é a variação por família:

| Família | % que menciona a marca | Leitura |
|---|---:|---|
| **Manual** | **89%** | Quem procura manual já sabe de quem é o produto. Território naturalmente da marca — e hoje entregue a terceiros |
| Assistência técnica | 4,5% a 50% | Varia por categoria; em ar condicionado só 4,5% menciona marca |
| **Defeito** | **0%** | `geladeira não liga` 320/mês · `máquina de lavar não liga` 320/mês — **nenhuma busca equivalente com a marca** |

**Defeito é 100% não-branded.** No momento em que o produto para de funcionar, o consumidor não
digita a marca — digita o sintoma. É o instante de maior fragilidade da relação, de maior
disposição a gastar, e de maior probabilidade de decidir trocar de marca. E é exatamente ali
que a disponibilidade mental da Electrolux é **zero**.

Isso reposiciona a tese de ecossistema. Ela não é sobre vender mais serviço. É sobre **estar
presente no momento em que a marca hoje desaparece** — e esse momento é mensurável, tem 17.960
buscas/mês só na nossa amostra, e é o único ponto da jornada em que a base instalada decide se
recompra ou troca.

---

## 5. Ar condicionado é onde o ecossistema é maior — nas duas fontes

Em busca, das dez maiores keywords da cauda, cinco são de ar condicionado, incluindo a maior de
todas. Em IA, os quatro maiores tópicos de vida com o produto são
`Ar condicionado: peças e funcionamento` (93.398), `Limpeza de Ar Condicionado` (80.659),
`Instalação de Ar Condicionado` (60.532) e `Limpeza de Máquina de Lavar` (58.643).

A convergência entre duas fontes independentes é o tipo de sinal que sustenta recomendação.
Ar condicionado é a categoria com maior densidade de demanda de ecossistema, provavelmente por
combinar instalação obrigatória, manutenção periódica e consumo de energia visível na conta.

---

## 6. Limites desta leitura

- **223.890 é uma amostra curada, não um censo da cauda.** 2.000 formulações, 519 com dado. O
  número é piso e serve para ordem de grandeza, não para modelagem de receita.
- **Ainda não sabemos quem captura.** As colunas de competidor vieram vazias de novo. "O
  território está vago" continua apoiado em posicionamento declarado × demanda medida.
- **Os arquivos de tópicos de IA têm vazamento de clustering.** 57,6% dos tópicos únicos não
  são sobre a categoria — `Limpeza de Sofás e Estofados` está no arquivo de lava-louças. Todos
  os números de IA deste documento usam só os 2.324 tópicos que mencionam o aparelho.
- **Tópicos se repetem entre arquivos.** `Ar condicionado: peças e funcionamento` aparece
  idêntico em dois arquivos; a deduplicação por nome foi aplicada antes de qualquer soma.
- **Um arquivo é dos Estados Unidos** (`fog_es_e_eletrodom_sticos_de_cozinha_us`) e foi
  excluído de todos os agregados.
- **Volume zero não é ausência de busca** — é ausência de dado da ferramenta. 1.481 das 2.000
  keywords não retornaram volume, e parte delas tem demanda real abaixo do piso de reporte.

---

## O que eu faria a seguir

1. **Levar o par 22.200 × 480 para a defesa como abertura do case Brasil.** É um número, é
   verificável pelo cliente em cinco minutos, e demonstra o diagnóstico inteiro numa linha: a
   estrutura existe, a demanda existe, e a marca não fez a ponte.
2. **Construir o argumento de território pelo custo de ocupação, não pelo volume.** KD 21,8
   contra 47,7 e 70% de intenção informacional dizem que esse território se toma com conteúdo
   e é 2,2x mais barato de ocupar. É a leitura de D6 aplicada a território.
3. **Fazer do momento de defeito o coração da tese criativa.** É o único ponto da jornada com
   0% de presença de marca, alta carga emocional e decisão de recompra embutida. Nenhum
   concorrente está lá, e o dado prova que ninguém está.
