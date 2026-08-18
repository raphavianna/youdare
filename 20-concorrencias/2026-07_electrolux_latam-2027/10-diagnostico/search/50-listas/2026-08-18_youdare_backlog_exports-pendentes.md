# Exports pendentes — o que puxar e o que cada um destrava

Estado em 18/08. Ordem é de prioridade: o bloco 1 destrava um slide que hoje fala de
concorrente e não do cliente; os blocos 2 e 3 corrigem viés e ampliam o universo.

---

## O que já temos

| Tipo de export | Quantidade | Detalhe |
|---|---:|---|
| `topics_by_fts` | 16 seeds | Todos de categoria, nenhum com nome de marca |
| `prompts_by_topic` | 5 seeds | `brastemp`, `eletrolux`, `geladeira`, `hisense`, `midea` |
| `brand_topics` | 1 domínio | `brastemp.com.br` |

---

## Bloco 1 · `brand_topics` por domínio — prioridade máxima

**O que destrava.** A medida de **ocupação** (visibility × volume), que é a mais dura do
pacote. Hoje ela existe só para a Brastemp, então o slide de ocupação do deck fala de um
concorrente e não do cliente. Com os domínios abaixo, ela vira comparação entre players.

| # | Domínio | Por quê |
|---|---|---|
| 1 | `loja.electrolux.com.br` | É o cliente. Sem ele, a medida não responde a pergunta da banca |
| 2 | `electrolux.com.br` | O institucional é domínio distinto da loja e pode cobrir tópicos diferentes |
| 3 | `consul.com.br` | Player que lidera posse em busca — o benchmark interno da categoria |
| 4 | `midea.com.br` | Entrante com maior crescimento de tráfego de LLM |
| 5 | `samsung.com.br` | Maior cobertura de posse em IA do conjunto (3,19%) |
| 6 | domínio BR da Hisense | Hoje fora de toda leitura de IA |
| 7 | domínio BR da Haier | Hoje fora de toda leitura de IA |

`brastemp.com.br` já veio e não precisa ser repetido.

---

## Bloco 2 · `prompts_by_topic` — corrige o viés de seed

**O que destrava.** Hoje a contagem de marca dentro das respostas é enviesada: quatro dos
cinco seeds são nomes de fabricante e três marcas do conjunto não têm seed nenhum. Por isso
a leitura de citação usa só as 943 respostas do seed `geladeira`. Com os seeds abaixo, a
amostra limpa cresce e o ranking de citação passa a ser defensável.

**Seeds de marca que faltam** — as três sem seed nenhum hoje:

- `consul`
- `samsung`
- `haier`

**Seeds sem marca** — cada um amplia o recorte limpo, que é o que sustenta a leitura:

- `ar condicionado`
- `máquina de lavar`
- `micro-ondas`

---

## Bloco 3 · `topics_by_fts` — amplia o universo mapeado

**O que destrava.** O universo é censurado em 1.000 linhas por seed. Cada seed novo alarga o
mapa. Os seeds de serviço abaixo são o mesmo quadrante que a lista de cauda fechou em busca, e
hoje não existe nenhum seed de serviço na base de IA — o que provavelmente **subestima a
posse**.

**Seeds de serviço e vida com o produto** — o buraco atual:

- `assistência técnica`
- `conserto de eletrodoméstico`
- `instalação`
- `peça de reposição`
- `manutenção`
- `garantia estendida`
- `manual`

**Categorias ainda não semeadas:**

- `micro-ondas` · `cooktop` · `coifa` · `secadora` · `lava e seca` · `purificador` ·
  `adega` · `cafeteira`

---

## Campos que precisam vir no export

| Export | Campos que decidem |
|---|---|
| `topics_by_fts` | `volume`, `volume_trend`, `intents`, `prompts_count` |
| `prompts_by_topic` | `prompt`, `llm`, `brief_response`, `relevance_score` e — se existir — **`mentioned_brands` por nome**, não só a contagem |
| `brand_topics` | `name`, `visibility`, `mentions`, `volume`, `volume_trend`, `intents` |

**O campo que mais muda o trabalho é `mentioned_brands` por nome.** Hoje sabemos que uma
resposta cita 2,8 marcas em média, mas não sabemos quais sem ler o texto — as marcas do
material vêm de busca de string na resposta, que é aproximação declarada. Com o campo, vira
medição.

---

## O que fica sem resposta mesmo com tudo isso

- **Quem captura cada consulta em busca.** A coluna de competidores veio vazia nos oito
  arquivos originais. Depende de posições orgânicas dos domínios captores.
- **O que a IA responde quando perguntam pela marca pelo nome.** Só veio o recorte sem marca.
- **Quais fontes os modelos citam.** Há contagem de fontes, não a lista.
