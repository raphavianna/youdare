# Impacto do pacote de 18/08 na base de IA

Registro do que entrou, do que foi descartado e do que mudou na leitura. A apresentação **não
foi regerada** — este documento é o entendimento antes de propagar.

---

## 1. O que entrou e o que saiu

Dez arquivos no pacote. **Cinco eram duplicatas** e foram descartados:

| Descartado | Motivo |
|---|---|
| `prompts_by_topic_fts_ar_condicionado_br` | Idêntico ao ancorado ontem |
| `prompts_by_topic_fts_maquina_de_lavar_br` | Idêntico ao ancorado ontem |
| `prompts_by_topic_fts_microondas_br` | Idêntico ao ancorado ontem |
| `topics_by_fts_ar_condicionado_br (1)` | **Zero tópicos inéditos** — mesmo export reordenado |
| `Desempenho_da_marca-loja_electrolux 18/08` | Texto idêntico ao de 17/08; todos os números iguais |

**Cinco entraram:**

| Entrou | O que é |
|---|---|
| `Desempenho da marca · consul.com.br` | AI Visibility, Google AI Mode — **primeiro relatório de concorrente** |
| `Desempenho da marca · midea.com.br` | AI Visibility, Google AI Mode — segundo concorrente |
| `prompts_by_topic · fritadeiras elétricas e air fryers` | 275 respostas, seed sem marca |

Os dois PDFs de AI Visibility que já estavam no repositório foram movidos para
`00-raw/ai-search/ai-visibility/` e renomeados com o domínio no nome, porque agora há quatro
relatórios de três domínios diferentes.

---

## 2. A regra que os relatórios de AI Visibility exigem

**Cada relatório monta o próprio universo de perguntas, em torno do domínio analisado.** A
consequência é medida e é grande:

| Onde a Electrolux é medida | SOV dela |
|---|---:|
| No relatório dela (Google AI Mode) | 12,4% |
| No relatório da Consul | **16,5%** |
| No relatório da Midea | 11,2% |

O mesmo player, na mesma plataforma, no mesmo período, com três valores. **Share of voice não
se compara entre relatórios.** A comparação válida é sempre entre players *dentro* do mesmo
relatório. O extrator (`normalizar_visibility.py`) grava o domínio de origem em cada linha
justamente para tornar esse erro impossível.

É a mesma classe de armadilha da cobertura contra ocupação, e precisa da mesma disciplina.

---

## 3. O que os relatórios de concorrente mostram

Lendo cada um por dentro, que é o que vale:

| Relatório | 1º | 2º | 3º | Dono do relatório |
|---|---|---|---|---|
| **Consul** | Brastemp 17,3% | **Electrolux 16,5%** | Consul 14,6% | 3º na própria casa |
| **Midea** | **Electrolux 11,2%** | Panasonic 10,6% | LG 10,3% | Midea é 5ª, com 8,2% |
| Electrolux · ChatGPT | Electrolux 14,7% | Consul 12,1% | Brastemp 8,8% | 1º |
| Electrolux · AI Mode | Electrolux 12,4% | Brastemp 11,6% | Consul 10,8% | 1º |

**Em dois dos três relatórios de concorrente, a Electrolux aparece mais que o dono da casa.** No
universo de perguntas construído em torno do domínio da Consul, ela é 16,5% contra 14,6% da
própria Consul. No da Midea, 11,2% contra 8,2%. Comparação interna, portanto válida.

É a sexta medida independente a apontar a mesma coisa: a Electrolux é a marca mais presente da
categoria em ambiente mediado por IA.

**E há um contraponto que não estava dado.** No relatório da Consul, quem lidera não é nenhuma
das duas: é a **Brastemp, com 17,3%**. A Brastemp não aparece como líder em nenhuma outra
medida do pacote — em cobertura por nome de tópico ela é 1,99%, terceira. Isso sugere que a
Brastemp é forte especificamente no território de perguntas em torno de lavanderia e cocção,
que é onde o domínio da Consul concentra.

**Sentimento, com ressalva.** Electrolux 41% no ChatGPT e 71% no AI Mode; Consul 89%; Midea
100%. Como cada número é do dono dentro do próprio universo, **não são estritamente
comparáveis** — mas a distância é grande demais para ser ignorada, e reforça o que as 150
perguntas já indicavam: a Electrolux é a mais citada e a pior falada entre as grandes.

---

## 4. O achado principal: a curva de citação por necessidade

Com o seed de air fryer, a amostra limpa chega a **3.599 respostas** e a família `uso e receita`
sai do limbo com n=201. A curva agora está completa, e é o dado mais forte do pacote:

| Família | n | Cita alguma das sete |
|---|---:|---:|
| Marca e loja | 26 | **50,0%** |
| Comparação e modelo | 591 | 39,9% |
| Especificação de produto | 798 | 39,1% |
| Garantia e suporte | 28 | 32,1% |
| Preço e compra | 516 | 28,1% |
| Manutenção e limpeza | 36 | 25,0% |
| Produto e categoria | 1.214 | 24,1% |
| Peça e filtro | 47 | 19,1% |
| Consumo e energia | 68 | 11,8% |
| **Uso e receita** | **201** | **3,5%** |
| **Instalação** | **38** | **0,0%** |

**Quanto mais a pergunta se afasta da compra, menos a IA nomeia fabricante.** De 50% quando a
pergunta é sobre loja, a 0% quando é sobre instalar. Não há degrau: é uma descida contínua ao
longo de onze famílias.

Duas leituras que isso destrava e que o material ainda não tem:

**Instalação responde zero.** Nenhuma das sete marcas é citada em nenhuma das 38 respostas sobre
instalação. A única marca que aparece é Tramontina, duas vezes. E instalação é uma frente
nomeada da Electrolux — a marca criou o Instala, e o assistente responde sobre instalar sem
citar quem instala.

**Uso e receita responde 3,5%.** Com n=201, é a família com amostra sólida e menor citação. O
briefing nomeia "pesquisar uma receita" como ponto de entrada do consumidor na marca; o dado diz
que nesse ponto de entrada a marca não existe, e nenhum concorrente também.

---

## 5. O que mudou nos números do material

| Medida | Antes | Agora |
|---|---:|---:|
| Amostra limpa de prompts | 943 | **3.599** |
| Famílias com leitura possível | 5 | **11** |
| Taxa geral de citação | 23,6% | 29,2% |
| Relatórios de AI Visibility | 0 digeridos | **4, de 3 domínios** |
| Tópicos de categoria | 3.205 | 3.205 (sem mudança) |
| Cobertura Electrolux | 5,69% | 5,69% (sem mudança) |

A base de tópicos não se moveu porque nada de tópico entrou. A base de prompts quase quadruplicou.

---

## 6. O que ainda falta

**Duas famílias a dois casos do corte:** `assistência e conserto` (n=18) e `defeito e problema`
(n=18). Ambas precisam de 20. Um seed de `conserto de geladeira` ou `assistência técnica`
fecharia as duas de uma vez, e são justamente as duas famílias mais centrais à tese de serviço.

**`topics_by_fts` de serviço:** nenhum dos 19 seeds de tópico é de serviço. A posse segue medida
em 9,6% e nada no pacote de hoje testou se esse é o piso.

**`brand_topics` por domínio:** os PDFs de AI Visibility entregam SOV e sentimento, mas **não
substituem** o `brand_topics`, que é o que dá visibility por tópico e permite calcular ocupação.
Os dois medem coisas diferentes.

---

## 7. Limites desta leitura

- **SOV não se compara entre relatórios de AI Visibility.** Cada um tem universo próprio.
- **O sentimento de cada relatório é do dono, dentro do universo dele.** Comparação entre
  relatórios é indicativa, não conclusiva.
- **`uso e receita` com 3,5% depende do seed de air fryer**, que concentra receita. A leitura é
  de família, não da categoria toda.
- **`instalação` tem n=38.** Zero é zero, mas com amostra pequena.
- **O conjunto competitivo muda por relatório** — o da Midea traz Panasonic e LG, o da Consul
  traz LG. As sete marcas do briefing não são o conjunto que a ferramenta monta.
