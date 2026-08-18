# Exports de IA — o que temos e o que falta

Estado após ancorar o pacote de 18/08. **Só material de IA.** Busca tem backlog próprio e não
entra aqui. Duplicatas foram removidas por hash de conteúdo, não por nome de arquivo.

---

## 1. O que já está ancorado

| Tipo | Qtd | Detalhe |
|---|---:|---|
| `topics_by_fts` de **categoria** | **19** | Entram no cálculo de cobertura |
| `topics_by_fts` de **marca** | 1 | `consul` — isolado, **fora** da cobertura (ver §3) |
| `prompts_by_topic` | 5 | `brastemp`, `eletrolux`, `geladeira`, `hisense`, `midea` |
| `brand_topics` | 1 | `brastemp.com.br` |
| AI Visibility (PDF) | 2 | ChatGPT e Google AI Mode, sobre `loja.electrolux.com.br` |
| Tráfego de LLM | 1 | 4 domínios, 12 meses |

**Seeds de categoria já rodados:** `air fryers` · `airfryer` · `ar condicionado` · `aspirador` ·
`climatizador` · `fogões e eletrodomésticos de cozinha` (BR e US) · `forno` · `freezer` (2
versões) · `geladeira` (BR e US) · `geladeiras e refrigeradores no Brasil` · `lava louça` ·
`liquidificador` · `máquinas de lavar roupas` · `máquina de lavar` · `micro-ondas` ·
`microondas`

---

## 2. O que o pacote de 18/08 acrescentou

Do zip vieram 18 arquivos. **13 eram duplicatas** — mesmo conteúdo já ancorado, inclusive um
PDF que difere só em metadado. Quatro CSVs entraram:

| Arquivo | Destino |
|---|---|
| `topics_by_fts_maquina_de_lavar_br` | tópicos de categoria |
| `topics_by_fts_micro_ondas_br` | tópicos de categoria |
| `topics_by_fts_microondas_br` | tópicos de categoria — export distinto do anterior, só 344 tópicos em comum |
| `topics_by_fts_consul_br` | **isolado**, fora da cobertura |

**O que isso mudou nos números:** universo de 9.175 para **10.198 tópicos**, categoria de 3.056
para **3.205**, volume de 22,6 para **23,4 milhões**. E a cobertura **não se moveu**: Electrolux
5,69%, sem marca 81,28%. Três seeds novos e a leitura fica de pé — é evidência de robustez.

---

## 3. Por que o seed `consul` ficou de fora

Ele devolveu 1.000 tópicos cujo topo é `Concursos Públicos Brasil`, `Consórcios no Brasil` e
`Portuguese Word Variants`: a ferramenta leu a raiz "consul". Dos 1.000, **114 carregam o nome
da marca e somam 706.994 de volume**. Incluí-los inflaria a cobertura da Consul de 1,14% para
cerca de 4%, **só por ela ter sido semeada** — o mesmo viés que já isola a leitura de citação
nos prompts.

O arquivo está no repositório, em `00-raw/ai-search/topicos-seed-branded/`, e pode ser usado
para leitura qualitativa da marca. Não entra em nenhum agregado de cobertura.

**Consequência para os próximos exports:** não rodar `topics_by_fts` com nome de marca. Para
medir marca, o instrumento certo é `brand_topics` por domínio.

---

## 4. Vale expandir? A curva de saturação responde

**Tópicos de categoria: saturado. Não vale.** Medindo quantos tópicos novos de categoria cada
seed acrescenta, na ordem em que foram rodados:

| Seed | Tópicos novos | Volume novo |
|---|---:|---:|
| Os 9 primeiros | 2.493 | 19,5 M |
| `aspirador`, `liquidificador` | 444 | 2,9 M |
| `geladeira`, `maquina-de-lavar`, `micro-ondas` | 237 | 1,1 M |
| `airfryer` (variante de `air fryers`) | 21 | 92 mil |
| `microondas-v2` (variante) | 13 | 72 mil |
| `freezer-v2` (variante) | **0** | **0** |

Variantes do mesmo termo não acrescentam nada. E o teste que decide: os três seeds de 18/08
entraram e **a cobertura não se moveu** — Electrolux 5,69% antes e depois. Rodar `cooktop`,
`coifa`, `secadora` vai acrescentar tópicos e não vai mudar nenhuma leitura.

**Tópicos de serviço: nunca testado. Vale, e é o único que pode mover a leitura.** A saturação
acima é da dimensão *categoria de produto*. A dimensão *necessidade de serviço* não foi
explorada nenhuma vez em 19 seeds.

**Prompts sem marca: subdimensionado. É onde expandir mais rende.** A amostra limpa — a única
em que citar um fabricante é decisão do modelo e não eco do prompt — tem **943 respostas de um
único seed**. Consequência medida: cinco famílias ficam com n abaixo de 20 e **não têm leitura
possível hoje**:

`assistência e conserto` · `instalação` · `manutenção e limpeza` · `garantia e suporte` ·
`marca e loja`

São exatamente as famílias de posse. O material afirma que a posse é o território vago, mas
**não consegue dizer se a IA nomeia marca nas perguntas de posse**, porque a amostra não
comporta. Cada seed sem marca novo multiplica essa base.

**Prompts de marca: baixa prioridade.** Os quatro seeds existentes já trazem 651 a 724 prompts
cada, e o ganho de somar `consul`, `samsung` e `haier` é de completude, não de leitura nova.

---

## 5. O que falta — em ordem de prioridade

### ~~Bloco A · `prompts_by_topic` sem marca~~ — **FEITO em 18/08**

`ar condicionado`, `máquina de lavar` e `micro-ondas` rodados e ancorados. A amostra limpa foi
de 943 para **3.404 respostas** e destravou três das cinco famílias: `marca e loja` (50,0% de
citação), `garantia e suporte` (32,1%) e `manutenção e limpeza` (25,0%).

E entregou um achado: **`instalação`, com n=38, responde 0,0%** — nenhuma das sete marcas é
citada em nenhuma resposta sobre instalação. A única marca que aparece é Tramontina, duas vezes.

**Ainda abaixo de 20:** `assistência e conserto` (14) · `defeito e problema` (18) ·
`uso e receita` (12). Viram o Bloco A-2.

### Bloco A-2 · `prompts_by_topic` — fecha as três famílias restantes

- `assistência técnica`
- `conserto de geladeira`
- `receitas air fryer`

Nenhum tem nome de marca, então a amostra continua limpa.

### Bloco B · `topics_by_fts` de serviço — o teste que falta

Nenhum dos 19 seeds é de serviço. Com a taxonomia corrigida a posse mede **9,6%**, e mais
seeds de produto não mexem nisso. Estes dizem se 9,6% é o tamanho real ou o piso:

- `assistência técnica`
- `conserto de eletrodoméstico`
- `instalação`
- `peça de reposição`
- `manutenção`
- `garantia estendida`
- `manual`

### Bloco C · `brand_topics` por domínio

Destrava a medida de **ocupação**, hoje calculada só para um concorrente. É o que falta para o
slide de ocupação falar do cliente.

- `loja.electrolux.com.br`
- `electrolux.com.br`
- `consul.com.br`
- `midea.com.br`
- `samsung.com.br`
- domínio BR da Hisense
- domínio BR da Haier

### Bloco D · `prompts_by_topic` de marca — completude

`consul` · `samsung` · `haier`. Fecham o conjunto, mas não abrem leitura nova.

### Não rodar

**Mais categorias de produto** (`cooktop`, `coifa`, `secadora`, `lava e seca`, `purificador`,
`adega`, `cafeteira`) e **variantes de termo já rodado**. A curva de saturação da §4 mostra que
acrescentam tópicos e não movem nenhum número.

**`topics_by_fts` com nome de marca.** O instrumento certo para medir marca é `brand_topics`.

---

## 6. Campos que decidem

| Export | Campos |
|---|---|
| `topics_by_fts` | `volume`, `volume_trend`, `intents`, `prompts_count` |
| `prompts_by_topic` | `prompt`, `llm`, `brief_response`, `relevance_score` e — se existir — **`mentioned_brands` por nome** |
| `brand_topics` | `name`, `visibility`, `mentions`, `volume`, `volume_trend`, `intents` |

`mentioned_brands` por nome continua sendo o campo que mais mudaria o trabalho: hoje as marcas
citadas vêm de busca de string no texto da resposta, aproximação declarada.

---

## 7. Material ancorado e ainda não digerido

- **Os dois PDFs de AI Visibility**, 88 páginas sobre `loja.electrolux.com.br`, com Share of
  Voice (14,66% contra 12,45% da Consul) e sentimento por plataforma. Nenhum script os lê e
  nenhum número deles está no material. **Digerir antes de gastar cota no Bloco A** — pode
  cobrir parte do que se pediria para o domínio do cliente.
