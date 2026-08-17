# Trilha B — Cenário por player, em busca mediada por IA

> **Revisão de base — leia junto com o panorama.** Este documento foi fechado sobre o universo
> de **2.324 tópicos** disponível na época. O pacote de exports foi ampliado depois e a base
> passou a **3.056 tópicos de categoria** e 22,6 milhões de volume. Dois números aqui mudaram
> com a base maior: a soma dos momentos de posse vai de **8,4% para 13,8%**, e as famílias de
> tópico foram reclassificadas. A leitura de cobertura por marca e a de jornada valem na versão
> do panorama, em `2026-08-17_youdare_analise_panorama-cobertura-ai.md`. O que se mantém deste
> documento é a leitura de **citação, posição e sentimento nas respostas**, que vem de outra
> fonte (150 perguntas) e não foi afetada.

> **Regra de isolamento.** Este documento usa **apenas dado de IA**. Não cita, não usa e não
> antecipa nenhuma leitura de busca tradicional. O cruzamento acontece na trilha C.

> **Registro desta etapa.** Planejamento, insight e tendência: demanda, jornada, volume e
> termos. Nada de eficiência de compra.

**M1 × P4.** *A pergunta: onde a marca existe dentro da resposta de IA, em que momento da
jornada, e para onde essa demanda está indo?*

Fontes: `20-normalizado/ai_respostas.csv` (150 perguntas não-branded × 5 provedores × 5 marcas)
· `00-raw/ai-search/topicos/` (2.324 tópicos únicos de categoria, com volume) ·
`00-raw/ai-search/2026-08-17_similarweb_ai-referrals_...` (12 meses, 4 domínios).

---

## 1. O que esta fonte enxerga e o que não enxerga

**Enxerga:** se a marca é citada quando o consumidor pergunta sem nomear ninguém; em que
posição dentro da resposta; com que carga de sentimento; quais temas concentram a demanda
mediada por assistente; e quanto tráfego real chega ao site vindo de LLM ao longo de 12 meses.

**Não enxerga:** quais fontes o modelo usou para montar a resposta — temos a contagem de fontes,
não a lista; o que a IA responde quando perguntam pela marca **pelo nome**, porque só veio o
recorte não-branded; e qualquer elo com venda.

**Cobertura desigual de players — condição de leitura.** As três fontes cobrem conjuntos
diferentes: as respostas cobrem Electrolux, Consul, Brastemp, Midea e Samsung; o tráfego cobre
apenas quatro domínios, sem Samsung, Hisense e Haier; e os tópicos **não têm dimensão de marca**
— descrevem a demanda da categoria, não de quem a atende. Hisense e Haier praticamente não
existem nesta trilha.

---

## 2. Cobertura: quando o consumidor não nomeia ninguém, quem a IA nomeia

Das 150 perguntas não-branded, em quantas cada marca aparece:

| Marca | Agregado | ChatGPT | Gemini | Google AI Mode | Perplexity |
|---|---:|---:|---:|---:|---:|
| **Electrolux** | **33%** | **25%** | 9% | 9% | 7% |
| Consul | 28% | 21% | 9% | 8% | 5% |
| Brastemp | 22% | 15% | 7% | 8% | 5% |
| Samsung | 13% | 11% | 1% | 3% | 3% |
| Midea | 11% | 8% | 1% | 1% | 3% |

**A Electrolux é a marca mais citada da categoria em resposta de IA.** Lidera no agregado e em
todos os quatro provedores. É a melhor notícia desta trilha e não estava dada.

**Mas a presença é concentrada em uma plataforma.** No ChatGPT a marca aparece em 25% das
perguntas; nos outros três, entre 7% e 9% — uma queda de dois terços. E o padrão vale para
todos os players, o que indica característica das plataformas, não fraqueza de marca: Gemini,
Google AI Mode e Perplexity citam marca com muito menos frequência do que o ChatGPT.

Consequência de planejamento: **a presença da categoria em IA hoje é, essencialmente, presença
no ChatGPT.** Qualquer leitura de "estamos bem em IA" que não separe plataforma está lendo
ChatGPT e chamando de IA.

---

## 3. Como a marca é falada quando aparece

| Marca | Posição média na resposta | Sentimento médio |
|---|---:|---:|
| Brastemp | **2,4** | 67,4 |
| **Electrolux** | 2,6 | **58,1** |
| Midea | 2,7 | 63,2 |
| Consul | 3,0 | **70,5** |
| Samsung | 3,4 | 46,3 |

A Electrolux tem a segunda melhor posição — quando citada, aparece cedo na resposta. E tem o
**segundo pior sentimento do conjunto**, à frente apenas da Samsung, e abaixo de Consul e
Brastemp.

**A tensão desta trilha está aqui: a marca é a mais citada e a pior falada entre as três
grandes.** Aparecer mais e ser descrita com carga menos positiva que os dois concorrentes
diretos é um problema de **conteúdo da menção**, não de volume de menção. Ganhar mais citação
não resolve; muda a escala do problema.

`[a confirmar: o sentimento aqui é classificação automática do fornecedor, sem critério
publicado. Serve como comparação relativa entre marcas na mesma medida — não como nível
absoluto.]`

---

## 4. Jornada: em que momento a marca aparece e em qual ela some

Cobertura da Electrolux por tipo de pergunta, contra os concorrentes:

| Família da pergunta | n | Electrolux | Consul | Brastemp | Midea | Samsung |
|---|---:|---:|---:|---:|---:|---:|
| Peça e consumível | 4 | **75%** | 50% | 50% | 0% | 0% |
| Aquisição e comparação | 26 | **38%** | 23% | 15% | 15% | 0% |
| Consumo e eficiência | 8 | 38% | 38% | 38% | 0% | 12% |
| Especificação de produto | 4 | 25% | 50% | 50% | 25% | 25% |
| **Manutenção e cuidado** | 4 | **0%** | 25% | 25% | 0% | 0% |
| **Receita e preparo** | 3 | **0%** | 0% | 0% | 0% | 0% |

**A marca é forte onde se decide a compra e desaparece onde se convive com o produto.** Em
aquisição e comparação, 38% e a liderança do conjunto. Em manutenção e cuidado, **zero** — e
Consul e Brastemp aparecem. Em receita, zero para todo mundo.

Ressalva de tamanho: as famílias de posse têm n entre 3 e 4 perguntas. **São indicativas, não
conclusivas** — a amostra de 150 perguntas não-branded é dominada por questões de compra, o que
por si só já diz algo sobre o recorte que a ferramenta considera relevante.

---

## 5. A demanda mediada por IA: onde ela se concentra

2.324 tópicos únicos sobre a categoria, somando 18,18 milhões de volume.

| Momento | Família de tópico | Tópicos | Volume | % |
|---|---|---:|---:|---:|
| Posse | **uso e receita** | 18 | **410.094** | **2,3%** |
| Posse | **limpeza e manutenção** | 34 | **343.758** | **1,9%** |
| Escolha | comparação e modelo | 17 | 283.195 | 1,6% |
| Posse | peça e filtro | 42 | 229.497 | 1,3% |
| Posse | consumo e energia | 14 | 174.403 | 1,0% |
| Posse | instalação | 24 | 159.868 | 0,9% |
| Posse | defeito e problema | 13 | 103.942 | 0,6% |
| Posse | assistência e conserto | 43 | 79.148 | 0,4% |
| Aquisição | preço e compra | 14 | 77.673 | 0,4% |
| — | demais (produto e categoria) | — | 16.319.214 | 89,8% |

**A soma de todos os momentos de posse é 8,4% da demanda mediada por IA** — quatro vezes mais
que aquisição por preço e compra (0,4%) e cinco vezes mais que comparação de modelo (1,6%).
Dentro do que é relação com o produto, a IA é usada muito mais para **conviver** do que para
**comprar**.

E há uma coincidência interna a esta trilha que vale registrar: **as duas maiores famílias de
posse — uso e receita (410 mil) e limpeza e manutenção (344 mil) — são exatamente as duas em
que a Electrolux tem 0% de cobertura nas respostas.** É o maior volume de demanda mediada por
IA da categoria, e a marca não está nele.

---

## 6. Trajetória: o tráfego que chega de LLM

| Domínio | ago/25 | jul/26 | 1º semestre | 2º semestre | Variação |
|---|---:|---:|---:|---:|---:|
| **loja.electrolux.com.br** | 8.569 | **46.261** | 12.231 | 21.448 | **+75%** |
| brastemp.com.br | 8.578 | 23.311 | 7.646 | 12.818 | +68% |
| consul.com.br | 4.094 | 23.434 | 4.070 | 9.590 | **+136%** |
| midea.com.br | 220 | 7.530 | 1.987 | 4.321 | +117% |

**O canal está explodindo para todo mundo.** A loja da Electrolux saiu de 8,6 mil para 46,3 mil
visitas mensais vindas de assistente em doze meses — uma multiplicação por 5,4 ponta a ponta.

E a Electrolux **ganha participação dentro dele**: de 39,9% do tráfego de LLM dos quatro
domínios no primeiro mês para **46,0% no último**. Sai na frente em volume absoluto e em share.

Ressalva: os valores vêm com casas decimais, o que indica estimativa modelada e não contagem.
E há células `N/A` em meses iniciais de concorrentes — ausência de dado, não zero.

---

## 7. Leitura por player

**Electrolux** — a marca mais citada da categoria em IA, com boa posição na resposta, e o
tráfego de LLM crescendo mais rápido que o mercado em volume absoluto. Três fragilidades: o
sentimento é o segundo pior do conjunto; a presença é fortemente dependente do ChatGPT; e a
cobertura zera exatamente nas famílias de posse que concentram o maior volume de demanda
mediada por IA.

**Consul** — o **melhor sentimento do conjunto** (70,5) e a segunda maior cobertura, com o
maior crescimento de tráfego de LLM (+136%). Aparece em manutenção e cuidado, onde a Electrolux
não aparece. É a marca mais bem falada da categoria dentro das respostas.

**Brastemp** — a **melhor posição média** (2,4): quando citada, é das primeiras. Sentimento
alto (67,4). Cobertura menor que Electrolux e Consul. Também presente em manutenção.

**Midea** — cobertura baixa (11%) e quase inexistente fora do ChatGPT, mas sentimento
razoável (63,2) e tráfego de LLM crescendo +117% sobre base pequena. Está entrando.

**Samsung** — pior sentimento (46,3) e pior posição (3,4) do conjunto, com cobertura de 13%.
É citada pouco, tarde e com carga menos positiva.

**Hisense e Haier** — fora do alcance desta trilha. Não estão nas respostas nem no tráfego.

---

## 8. Limites desta trilha

- **As famílias de posse têm n muito pequeno** nas 150 perguntas (3 a 4 cada). Indicativas, não
  conclusivas.
- **Só temos o recorte não-branded.** O que a IA diz quando perguntam pela Electrolux pelo nome
  não está no pacote — e é justamente a conversa de quem já é cliente.
- **Não sabemos quais fontes os modelos citam.** Há contagem, não lista.
- **O sentimento é classificação automática** sem critério publicado; vale como comparação
  relativa, não como nível.
- **Os arquivos de tópicos têm vazamento de clustering** — 57,6% dos tópicos únicos não são
  sobre a categoria e foram excluídos; os números aqui usam só os 2.324 que mencionam aparelho.
- **Um arquivo de tópicos é dos Estados Unidos** e ficou fora de todos os agregados.
- **O tráfego de LLM é estimativa modelada**, não contagem.
- **Hisense e Haier não têm cobertura** nesta trilha.

---

## O que eu faria a seguir

1. **Levar a tensão citação × sentimento como o achado principal desta trilha.** A marca é a
   mais citada e a pior falada entre as três grandes. É um problema de conteúdo da menção, e
   não se resolve com mais presença.
2. **Registrar a dependência de ChatGPT como risco de concentração.** 25% de cobertura lá e 7%
   a 9% nos outros três significa que a posição da categoria em IA está apoiada numa plataforma
   só — e nenhuma decisão de conteúdo deveria ser tomada sem separar isso.
3. **Fechar a trilha C.** Com A e B independentes, a comparação entre elas passa a significar
   alguma coisa — e é lá que as lacunas e as oportunidades ficam visíveis.
