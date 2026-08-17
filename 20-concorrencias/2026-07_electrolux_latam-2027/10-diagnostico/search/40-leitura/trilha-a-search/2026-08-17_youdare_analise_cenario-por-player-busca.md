# Trilha A — Cenário por player, em busca

> **Regra de isolamento.** Este documento usa **apenas dado de busca**. Não cita, não usa e não
> antecipa nenhuma leitura de busca por IA. O cruzamento entre as duas fontes acontece na
> trilha C, e só depois que a trilha B existir de forma independente.

**M1 × P2+P4.** *A pergunta: o que o volume de busca revela sobre a jornada, a posição e a
trajetória de cada player da categoria?*

Fontes: `20-normalizado/keywords.csv` (4.965 keywords, 8 players) +
`00-raw/busca-convencional/2026-08-17_semrush_keywords_cauda-nao-branded.csv` (492 keywords com
volume, tratadas aqui como um nono player: o território sem dono).

---

## 1. O que esta fonte enxerga e o que não enxerga

**Enxerga:** demanda expressa e seu tamanho, a composição dela por tipo de necessidade, a forma
temporal ao longo de 12 meses, e o custo e a dificuldade de disputá-la.

**Não enxerga:** quem captura a demanda — as colunas de competidor vieram vazias nos nove
arquivos; demanda latente, que ainda não tem vocabulário; causalidade; e qualquer elo com
conversão ou receita.

**Assimetria de amostra — condição de leitura.** Os exports foram puxados com profundidade e
seed diferentes por player: Brastemp tem 1.998 keywords e Haier tem 44. **Volumes absolutos
entre players não são comparáveis.** Toda a leitura de jornada abaixo é feita por
**composição percentual dentro de cada player**, que é interna e portanto legítima.

Um caso específico exige ressalva: o seed da Samsung foi `geladeira samsung`, não `samsung`.
Por construção, o arquivo dela quase não contém busca pelo nome puro da marca, o que derruba
artificialmente a fatia de "marca e navegação" dela. **O 5,5% da Samsung é artefato de seed, não
achado.** Os demais players usaram seed de marca.

---

## 2. O cenário

| Player | kw | Volume/mês | KD | CPC | AI Overview no SERP | Intenção dominante |
|---|---:|---:|---:|---:|---:|---|
| Categoria (heads sem marca) | 65 | 6.869.800 | **47,7** | $0,15 | 28% | Comercial 62% |
| Brastemp | 1.998 | 2.949.270 | 31,6 | **$0,54** | 22% | Informacional 66% |
| Consul | 1.064 | 1.483.110 | 28,5 | $0,29 | 27% | Informacional 53% |
| **Electrolux** | 900 | 711.670 | **38,8** | $0,19 | **14%** | Informacional 40%, Comercial 34% |
| Midea | 101 | 552.800 | 36,8 | $0,24 | 25% | Informacional 50%, Navegacional 40% |
| **Território sem dono** | 492 | 207.600 | **21,0** | $0,29 | **58%** | Informacional 74% |
| Hisense | 493 | 172.660 | 27,2 | $0,12 | 49% | Informacional 52% |
| Samsung | 300 | 125.460 | 39,5 | $0,14 | 18% | Informacional 78% |
| Haier | 44 | 4.480 | 22,8 | $0,16 | 59% | Informacional 57% |

Nota sobre `AI Overview`: é uma **característica do SERP** medida pela ferramenta de busca —
com que frequência o Google apresenta um resumo gerado no topo daquela consulta. Está aqui
porque é dado de busca. Sua interpretação cruzada fica para a trilha C.

---

## 3. Jornada — o que a composição revela

Cada família de demanda corresponde a um estágio da relação do consumidor com a marca. A
distribuição entre elas descreve **onde a demanda de cada player está concentrada**.

| Estágio | Família | Electrolux | Brastemp | Consul | Samsung* | Midea | Hisense | Haier |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Descoberta** | marca e navegação | 24,8% | 17,9% | 15,1% | 5,5%* | 24,6% | **41,9%** | **62,1%** |
| **Escolha** | especificação de produto | 26,9% | 20,9% | 25,7% | 29,5% | **30,2%** | 16,9% | 2,9% |
| **Posse** | vida com o produto | 4,4% | 3,5% | **8,1%** | 4,6% | 0,0% | 2,7% | 1,3% |

\* artefato de seed, ver §1.

**Três arquétipos de jornada, lidos só pelo volume:**

**Descoberta de marca — Haier e Hisense.** Com 62,1% e 41,9% da demanda concentrada no nome da
marca, o que existe é gente perguntando *quem é essa marca*. Haier quase não tem demanda de
especificação (2,9%), o que significa que a curiosidade ainda não virou consideração de produto.
Hisense já tem 16,9% em especificação — está um passo à frente na mesma trajetória. Em Hisense
aparecem termos de validação no topo da lista: `hisense é boa` e `ar condicionado hisense é
bom` estão entre as cinco maiores. **A demanda deles é de reputação, não de produto.**

**Escolha de produto — Midea, Electrolux e Brastemp.** A maior fatia está em especificação:
capacidade, tecnologia, modelo. O consumidor sabe da marca e está decidindo qual item. É a
jornada de marca estabelecida com portfólio conhecido.

**Posse — Consul.** Com **8,1% em vida com o produto**, quase o dobro da Electrolux, é o player
com a jornada mais madura em busca: base instalada grande o suficiente para gerar demanda de
pós-compra visível. É o retrato de uma marca de volume com muitos aparelhos em uso.

**A leitura desconfortável para o cliente:** a Electrolux tem 4,4% em vida com o produto, contra
8,1% da Consul. Sendo a Electrolux uma marca de posicionamento superior — o briefing a coloca em
*justified premium* —, seria esperado que sua base gerasse relação de pós-compra ao menos
equivalente. Ela gera metade.

---

## 4. Tendência — quem cresce, depois de descontar a sazonalidade

A leitura bruta da série de 12 meses engana: **todos os players têm pico nos mesmos meses 7 a 9,
inclusive as cabeças de categoria.** Isso é sazonalidade da categoria, não desempenho de player.
Medir crescimento sem descontar isso produziria um falso positivo para todo mundo.

A correção é dividir a série de cada player pela série das cabeças de categoria, que serve de
baseline de demanda. O resultado é a evolução do **share relativo de demanda**.

| Player | Inclinação bruta | **Inclinação vs categoria** | Forma do share relativo | Leitura |
|---|---:|---:|---|---|
| Hisense | 1,60 | **1,40** | ▃▆▅▄▄▅▆██▅▅▅ | **ganha share** |
| Haier | 1,56 | **1,36** | ▄█▃▃▃▅▃▆▆▅▅▆ | **ganha share** |
| Midea | 1,19 | 1,06 | ▇▇▇█▇█████▇█ | estável |
| Consul | 1,07 | 0,97 | █▇██▇▇▇▇▇▇▇█ | estável |
| **Electrolux** | 1,08 | **0,99** | ▇███▇▇█▆▇███ | **estável** |
| Brastemp | 0,95 | **0,86** | ████▇█▇▆▇▇▇█ | **perde share** |
| Samsung | 0,95 | **0,85** | ███████▆▇▇▇█ | **perde share** |

A correção muda três leituras. A Midea parecia crescer 19% e está estável. A Electrolux parecia
crescer 8% e está parada. E Brastemp e Samsung, que pareciam apenas estáveis, estão **perdendo
share de demanda** — 14% e 15% respectivamente.

**O crescimento de demanda da categoria está concentrado nos dois entrantes**, e em nenhum dos
players estabelecidos. Ressalva de escala: Hisense e Haier crescem sobre bases pequenas — juntos
somam 177.140 contra 711.670 da Electrolux. É movimento de trajetória, não de volume.

**Dentro da Electrolux, a decomposição por família mostra onde o pouco movimento acontece:**

| Família | Volume médio | Inclinação | Forma |
|---|---:|---:|---|
| defeito | 2.410 | **1,43** | ▆▅▄▄▄▄▅▇█▆▅▆ |
| garantia | 1.310 | 1,32 | ▂▄▂▂▇▂▆▄▃▄█▂ |
| peça e consumível | 18.530 | **1,29** | ▅▅▆▆▆▇▇█▇▇█▇ |
| manual e uso | 520 | 1,24 | ▇▇▅▃▇▇▃▇█▇▅▇ |
| especificação de produto | 191.340 | 1,17 | ▆▆▆▆▆▆█▇█▇▇▇ |
| marca e navegação | 176.370 | 0,96 | ▆▆▆▆▆▆█▆▆▆▆▆ |
| assistência e reparo | 8.500 | 0,93 | █▄▇█▅▆██▅▆▅▆ |
| **frente nomeada** | 2.130 | **0,75** | ▅▄█▃▆▃▇▄▅▄▄▄ |
| manutenção e cuidado | 140 | 0,72 | ▄▃▅▅▆▇█▃▅▃▃▆ |

As famílias que crescem na Electrolux são as de **posse** — defeito, garantia, peça, manual. A
que mais cai é **frente nomeada**, a 0,75. As estruturas que a marca criou perdem demanda
enquanto a demanda espontânea de pós-compra sobe. As duas curvas vão em direções opostas.

---

## 5. Custo e dificuldade — onde a demanda é cara e onde é barata

| Recorte | KD | CPC |
|---|---:|---:|
| Cabeças de categoria | **47,7** | $0,15 |
| Samsung | 39,5 | $0,14 |
| **Electrolux** | **38,8** | $0,19 |
| Midea | 36,8 | $0,24 |
| Brastemp | 31,6 | **$0,54** |
| Consul | 28,5 | $0,29 |
| Hisense | 27,2 | $0,12 |
| Haier | 22,8 | $0,16 |
| **Território sem dono** | **21,0** | $0,29 |

Dois fatos que saltam.

**A demanda da própria Electrolux é a segunda mais difícil de sustentar entre os players**, com
KD 38,8 — acima de Brastemp, Consul, Hisense e Haier. Dificuldade alta em busca de marca
própria indica disputa de terceiros pelo nome: varejo, marketplace e afiliados competindo pelas
consultas que trazem o nome da marca. `[a confirmar: quem ocupa essas posições — coluna de
competidor veio vazia]`

**O CPC da Brastemp é 2,8x o da Electrolux** — $0,54 contra $0,19. A demanda da Brastemp é
comercialmente muito mais disputada, o que é coerente com ela ser a maior base de volume da
categoria neste dataset.

---

## 6. O nono player: o território sem dono

As 492 keywords não-branded com volume formam um bloco que nenhum player reivindica: **207.600
buscas/mês**, com o perfil mais distinto do dataset.

**KD 21,0 — o mais baixo de todos.** É a demanda mais fácil de ocupar da categoria, 2,3x mais
fácil que as cabeças. **Intenção informacional em 74% do volume**, contra 62% comercial nas
cabeças — território que se ocupa com conteúdo, não com leilão. E **58% das consultas exibem
AI Overview no SERP**, a maior taxa do dataset junto com a Haier.

Composição interna: peça 26,3% · assistência 20,0% · instalação 16,6% · manutenção 13,0% ·
defeito 8,7% · sinônimos 5,8% · manual 4,1% · consumo 3,9% · receita 1,4%.

A maior consulta isolada é `instalação de ar condicionado`, com 22.200 buscas/mês — sozinha,
10,7% de todo o território.

---

## 7. Leitura por player

**Electrolux** — jornada de escolha de produto, demanda estável sem ganho de share, e a
segunda maior dificuldade de defesa do próprio nome. A fatia de posse (4,4%) é metade da
Consul, apesar de posicionamento superior. As famílias de pós-compra crescem, as frentes
nomeadas encolhem.

**Brastemp** — a maior base de demanda e a mais cara ($0,54). **Perde share a 0,86.** Jornada
de escolha, com posse baixa (3,5%) para o tamanho da base.

**Consul** — a jornada mais madura da categoria: 8,1% em posse, o dobro da Electrolux. Estável
em share, KD e CPC moderados. É o player que melhor converteu base instalada em relação
buscável.

**Samsung** — leitura limitada pelo seed. **Perde share a 0,85**, a maior queda do conjunto, e
tem o maior KD (39,5). Intenção 78% informacional.

**Midea** — 40% de intenção navegacional, o maior do conjunto: a demanda dela é gente indo
direto ao nome. Zero em vida com o produto, coerente com base instalada recente. Estável.

**Hisense** — **ganha share a 1,40**, o maior movimento do conjunto. Jornada de descoberta,
com termos de validação de reputação no topo (`hisense é boa`). KD 27,2 e CPC $0,12: barata de
disputar. Ressalva: o share relativo mostra pico nos meses 8-9 e recuo depois — parte do
crescimento pode ser evento, não tendência.

**Haier** — **ganha share a 1,36**, sobre a menor base do conjunto (4.480). 62,1% da demanda no
nome da marca: estágio inicial de formação. KD 22,8, o menor entre marcas.

---

## 8. Limites desta trilha

- **A taxonomia cobre entre 33% e 89% do volume por player**; "não classificado" é categoria
  legítima e aparece em todas as contas. Os percentuais de composição são share do conjunto
  classificado quando indicado.
- **Volume absoluto entre players não é comparável** — profundidade de export diferente.
- **A Samsung tem seed de categoria**, não de marca; a composição dela não é comparável às
  demais no eixo de descoberta.
- **A série mensal é reconstruída** a partir de `Volume` e `Trend`, sob premissa declarada.
- **Ninguém sabe quem captura** — coluna de competidor vazia em todos os arquivos.
- **Hisense e Haier crescem sobre bases pequenas.** Percentual de crescimento em base pequena é
  frágil como indicador e não deve ser apresentado sem o número absoluto ao lado.

---

## O que eu faria a seguir

1. **Fechar a trilha B** — a leitura de IA, isolada, sem consultar este documento. É a condição
   para que a convergência ou a divergência entre as duas signifique alguma coisa.
2. **Levar o par Consul 8,1% × Electrolux 4,4% para a conversa de tese.** É uma comparação
   entre marcas do mesmo mercado, com o mesmo instrumento, e aponta um vão de relação com a
   base instalada que não depende de nenhuma hipótese.
3. **Registrar a queda das frentes nomeadas (0,75) como o dado mais acionável desta trilha.** É
   a única série da Electrolux que cai enquanto a demanda espontânea correspondente sobe.
