# Dicionário de dados — search Electrolux Brasil

Etapa 1 do job. Inventário e auditoria de tudo que foi recebido, antes de qualquer análise.
Fonte imutável: `_inbox/dataelux.zip` (4,7 MB, 21 arquivos, recebido em 17/08/2026). Os
arquivos canônicos, já deduplicados e renomeados, estão em `00-raw/`.

---

## 1. Resultado da revisão de duplicatas

**21 arquivos recebidos → 16 canônicos. 5 descartados por duplicação.** Nada foi perdido: os
originais permanecem no zip.

### 1.1 Os seis PDFs eram dois relatórios, não um

Os seis PDFs têm nome idêntico e diferem só pelo sufixo `(1)` a `(5)`. Hash de arquivo não
resolve — os seis são diferentes byte a byte, porque o SEMrush carimba o momento da exportação.
Comparando o **texto extraído**, aparecem dois documentos distintos:

| Grupo | Páginas | Cópias | Plataforma | Arquivos originais |
|---|---|---|---|---|
| A | 45 | 4 | **ChatGPT** | `(1)`, `(2)`, `(3)`, `(4)` |
| B | 43 | 2 | **Google AI Mode** | `(5)`, sem sufixo |

Os dois grupos **não são duplicatas entre si**: é o mesmo relatório "Desempenho da marca"
rodado para duas plataformas de IA diferentes, com prioridades estratégicas e números
distintos. Deduplicar por "mesmo relatório" teria descartado uma das duas plataformas.

Ancorados: um de cada grupo. Descartadas 4 cópias.

### 1.2 O par de planilhas de respostas de IA

`...answers_non-branded_2026-08-14 (1).xlsx` e `...2026-08-14.xlsx` têm o mesmo tamanho e
hashes de arquivo diferentes, mas o **conteúdo é idêntico**: aba única `Data`, 750 linhas × 24
colunas, mesmo hash de conteúdo. Duplicata real. Descartada 1 cópia.

O `.csv` de mesmo nome **não é duplicata a descartar**: é o mesmo relatório em outro formato,
com o texto completo das respostas preservado. Mantidos os dois — o CSV é o canônico para
pipeline, o XLSX fica como recebido.

### 1.3 Keywords: sem redundância entre arquivos

| Arquivo | Linhas | Keywords únicas | Duplicata interna |
|---|---:|---:|---:|
| Electrolux branded | 904 | 904 | 0 |
| Genéricas de categoria | 65 | 65 | 0 |
| Brastemp | 2.000 | 2.000 | 0 |
| Consul | 1.082 | 1.082 | 0 |
| Hisense | 500 | 500 | 0 |
| Midea | 101 | 101 | 0 |
| Samsung | 300 | 300 | 0 |
| **Total** | **4.952** | **4.941 únicas** | **0** |

Apenas **11 keywords** aparecem em mais de um arquivo, todas no par Brastemp × Consul, e
**nenhuma com volume divergente** — os valores batem entre arquivos. A base está limpa e os
arquivos são complementares, não redundantes.

---

## 2. Busca convencional — `00-raw/busca-convencional/`

Sete exports de keyword do SEMrush, base `br`, baixados em 17/08/2026.

| Arquivo | Marca / recorte | Linhas | Formato |
|---|---|---:|---|
| `2026-08-17_semrush_keywords_electrolux-branded.xlsx` | Electrolux, seed `eletrolux` | 904 | xlsx, 36 col |
| `2026-08-17_semrush_keywords_genericas-categoria.xlsx` | genéricas de categoria, sem seed de marca | 65 | xlsx, 36 col |
| `2026-08-17_semrush_keywords_brastemp.csv` | Brastemp | 2.000 | csv, 18 col |
| `2026-08-17_semrush_keywords_consul.csv` | Consul | 1.082 | csv, 18 col |
| `2026-08-17_semrush_keywords_hisense.csv` | Hisense | 500 | csv, 18 col |
| `2026-08-17_semrush_keywords_midea.csv` | Midea | 101 | csv, 18 col |
| `2026-08-17_semrush_keywords_samsung.csv` | Samsung | 300 | csv, 18 col |

**Schema divergente entre os dois formatos — exige normalização na etapa 4.** Os XLSX trazem
36 colunas com `Content reference 1..10` e `Competitor on TOP 10 #1..10` **expandidos**; os CSV
trazem 18 colunas com os mesmos campos **colapsados** em `Content references` e `Competitors`.
São o mesmo dado em estruturas diferentes.

Campos comuns: `Database` · `Keyword` · `Seed keyword` · `Page` · `Topic` · `Page type` ·
`Tags` · `Volume` · `Keyword Difficulty` · `CPC (USD)` · `Competitive Density` ·
`Number of Results` · `Intent` · `SERP Features` · `Trend` (12 valores, série mensal) ·
`Click potential`.

Campos que importam para este job em particular: **`Intent`** (Navigational, Informational,
Commercial, Transactional) é o que separa demanda de aquisição de demanda de vida com o
produto; **`SERP Features`** registra presença de `AI Overview`, que é a ponte entre os dois
universos de dado; **`Trend`** dá a série de 12 pontos para sazonalidade; e
**`Competitor on TOP 10`** revela quem captura cada keyword, incluindo captores que não são
marca de eletrodoméstico.

### Assimetria de amostra — declarar em toda comparação
Os arquivos têm tamanhos muito diferentes (Brastemp 2.000 vs Midea 101). Isso **não** significa
que a Brastemp tem 20× mais demanda: significa que o export foi puxado com profundidade
diferente por marca. Qualquer comparação de volume entre marcas precisa ser feita sobre base
comparável — por keyword em comum ou por recorte de topo — nunca sobre a soma bruta dos
arquivos. `[a confirmar: qual critério de corte foi usado em cada export — top N por volume,
filtro de seed, ou outro]`

---

## 3. AI search — `00-raw/ai-search/`

| Arquivo | O que é | Cobertura |
|---|---|---|
| `2026-08-17_semrush_ai-visibility_desempenho-marca-chatgpt.pdf` | Relatório "Desempenho da marca" para `loja.electrolux.com.br` | 45 páginas, plataforma ChatGPT |
| `2026-08-17_semrush_ai-visibility_desempenho-marca-google-ai-mode.pdf` | Mesmo relatório, outra plataforma | 43 páginas, Google AI Mode |
| `2026-08-14_semrush_ai-answers_non-branded-brasil.csv` | Posição e sentimento por marca em respostas de IA a perguntas não-branded | 749 linhas = **150 perguntas × 5 provedores** |
| `2026-08-14_semrush_ai-answers_non-branded-brasil.xlsx` | Mesmo dado, formato alternativo | 750 × 24 |
| `2026-08-17_similarweb_ai-referrals_electrolux-vs-concorrentes.xlsx` | Tráfego de referência vindo de LLMs, por mês e por LLM, para 4 domínios | 12 meses: 2025-08 a 2026-07 |
| `2026-08-17_ai-prompts_topico-eletrolux.csv` | Prompts e respostas por tópico | 1.000 linhas |
| `2026-08-17_ai-prompts_topico-geladeira.csv` | idem | 1.000 linhas |
| `2026-08-17_ai-prompts_topico-hisense.csv` | idem | 1.000 linhas |
| `2026-08-17_ai-prompts_topico-midea.csv` | idem | 1.000 linhas |

### 3.1 AI answers non-branded
Colunas: `Question` · `Provider` · para cada marca, `(position)`, `(position diff)`,
`(sentiment score)`, `(sentiment score diff)` · `Competitors` · `Answer` (texto integral).

Provedores: `All AI Platforms` (150), `ChatGPT` (150), `Gemini` (150), `Perplexity` (150),
`Google AI Mode` (149). A linha de `All AI Platforms` é agregado — **não somar com as demais**,
sob pena de contar cada pergunta duas vezes.

Marcas rastreadas: **Electrolux, Consul, Brastemp, Midea, Samsung**.

### 3.2 AI referrals
Colunas: `Month` · `LLM` · `loja.electrolux.com.br` · `brastemp.com.br` · `consul.com.br` ·
`midea.com.br`. LLMs presentes: ChatGPT, Perplexity, Others. País: Brazil. Janela:
01/08/2025 a 31/07/2026.

Cuidados: há `N/A` em células de concorrente em meses iniciais — ausência de dado, não zero. E
os valores vêm com casas decimais (ex.: 8568,999...), o que indica **estimativa modelada**, não
contagem. Métrica-proxy, a declarar em todo uso (R4).

Origem inferida: SimilarWeb, pelo formato do export — aba `Report Details` com país, janela e
data de download. **Confiança média** (R3); confirmar com quem puxou.

### 3.3 Prompts por tópico
Colunas: `prompt` · `llm` · `brief_response` · `mentioned_brands_count` · `sources_count` ·
`relevance_score`. 4.000 prompts no total.

Distribuição por LLM:

| Tópico | chatgpt | gemini | google_ai_mode | google_ai_overview |
|---|---:|---:|---:|---:|
| eletrolux | 139 | 144 | 151 | 566 |
| geladeira | 194 | 195 | 200 | 411 |
| hisense | 182 | 220 | 186 | 412 |
| midea | 179 | 178 | 185 | 458 |

`google_ai_overview` domina a amostra em todos os tópicos — qualquer leitura agregada por LLM
precisa ponderar isso, ou o resultado descreve o AI Overview e não "a busca por IA".

`[a confirmar: ferramenta de origem destes quatro arquivos. O padrão de nome e as colunas não
correspondem aos demais exports do SEMrush. Não foi atribuída origem no nome do arquivo para
não registrar informação errada.]`

---

## 4. Conjunto competitivo declarado pelos arquivos

Conforme a carta do job, o denominador vem dos arquivos, não de conhecimento geral.

| Player | Keywords | AI answers | AI referrals | Prompts por tópico |
|---|:-:|:-:|:-:|:-:|
| **Electrolux** | sim | sim | sim | sim |
| **Brastemp** | sim | sim | sim | — |
| **Consul** | sim | sim | sim | — |
| **Midea** | sim | sim | sim | sim |
| **Samsung** | sim | sim | — | — |
| **Hisense** | sim | — | — | sim |

**A cobertura é assimétrica e isso limita o que pode ser comparado.** Samsung não está no AI
referrals; Hisense não está no AI answers; Brastemp e Consul não têm arquivo de prompts por
tópico. Nenhuma leitura pode tratar os seis como um painel completo — cada comparação declara
quais players a fonte cobre.

Aparecem ainda, no corpo dos relatórios de AI visibility, captores que **não são fabricantes**:
marketplaces (Magalu, Amazon) e fontes institucionais e editoriais (ex.: conteúdo sobre
INMETRO). Esses são o conjunto competitivo do **ecossistema**, distinto do conjunto competitivo
do **produto** — e são exatamente os atores relevantes para testar H1.

---

## 5. Alerta de método sobre os PDFs

Os dois relatórios de AI visibility contêm uma seção de "Prioridades estratégicas urgentes"
gerada pela própria ferramenta — recomendações escritas por IA dentro do SEMrush, com títulos
como *Turn Service Into Shield*, *Defend SOV Leadership* e *Service As Visibility Moat*.

**Isso é insumo, não achado.** São hipóteses da máquina sobre o dado dela, não análise nossa, e
entram no trabalho como material a verificar contra os dados brutos. Nenhuma dessas frases
pode aparecer em entregável como se fosse conclusão da agência (R3).

Registro de interesse, porém: essas recomendações apontam espontaneamente para menções de
conveniência, instalação e proteção, e para a disputa de referência técnica contra fontes de
terceiros. É a direção de H1 — o que reforça a necessidade do critério de refutação escrito
antes da análise, para não confundir eco de ferramenta com evidência.

---

## 6. Lacunas do dado recebido

- `[a confirmar: critério de corte de cada export de keyword — sem isso, comparação de volume entre marcas fica sem base]`
- `[a confirmar: janela temporal dos exports de keyword. Os arquivos trazem série de 12 pontos em Trend, mas não a data de início declarada]`
- `[a confirmar: ferramenta de origem dos quatro arquivos de prompts por tópico]`
- `[a confirmar: origem do AI referrals — inferida como SimilarWeb, confiança média]`
- **Sem dado de posição orgânica atual da Electrolux** (Organic Research / Position Tracking): dá para ver quem está no top 10 por keyword, mas não a evolução de posição da marca.
- **Sem dado de search paga**: nenhum export de campanha, share de impressão ou custo real. `CPC (USD)` é estimativa de mercado, não custo praticado.
- **Sem dado de tráfego do site próprio** além do AI referrals: não dá para fechar o elo entre busca e conversão em `loja.electrolux.com.br`.
- **Sem cobertura das frentes nomeadas do briefing** — Instala, Projeta, Cuida, Pro, Shopclub, Afiliados: ainda não sei se existem keywords dessas frentes nos arquivos. Verificar na etapa 3.
