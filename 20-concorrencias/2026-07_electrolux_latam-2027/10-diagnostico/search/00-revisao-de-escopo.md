# Revisão de escopo — o pacote de dados está fechado

Registro da decisão de 17/08/2026: **não haverá novos exports.** As pendências do
`10-dicionario/pedido-de-dados.md` deixam de ser "a confirmar" e passam a ser **limites
permanentes deste job**. Este arquivo prevalece sobre a carta do job onde houver conflito.

---

## 1. O que muda na hipótese central

**H1, como estava escrita, não é testável e não será testada.**

> *H1 original:* existe volume relevante de demanda de "vida com o produto" hoje capturada por
> terceiros, e esse volume é o tamanho de mercado do ecossistema medido em busca.

Testá-la exigiria o universo de keywords de serviço **não-branded**, que não virá. Sem ele não
existe numerador nem denominador: os oito arquivos são todos seeds de marca, e medem apenas a
fatia da demanda de ecossistema que já menciona um fabricante.

Conforme a carta do job, H1 permanece **hipótese declarada** e não sai como achado. O
entregável final vai dizer isso com estas palavras.

### O que entra no lugar — H1'

> **H1'** — o território do ecossistema está **desabitado**: nenhum player da categoria,
> incluindo a Electrolux, tem demanda mensurável atrelada aos territórios de serviço que
> declara ocupar. E a demanda de vida com o produto que existe no dado é predominantemente de
> **base instalada** — aparece no branded, não na categoria.

**Critério de refutação, escrito antes da análise final.** H1' é considerada não sustentada se:

- algum player do conjunto mostrar demanda relevante atrelada a um território de serviço que
  declara — hoje o maior é a Haier, com 2,1% do volume da própria marca;
- as frentes nomeadas da Electrolux mostrarem volume material na base dela — hoje somam 0,03%;
- a proporção de vida com o produto **não** for maior no recorte branded do que no de
  categoria — hoje é 12,1% contra 5,7%.

**O que se ganha e o que se perde na troca.** Perde-se o número de tamanho de mercado, que era
o argumento mais forte possível na banca. Ganha-se um diagnóstico de ocupação que é
verificável com o dado em mãos, defensável, e que nenhum concorrente de pitch terá — porque
depende de cruzar posicionamento declarado com demanda medida, e não de ter mais dado.

A ausência do número vira, ela própria, recomendação: **dimensionar esse território é a
primeira coisa que a agência faria ao entrar na conta.** Isso transforma uma lacuna em
proposta de trabalho.

---

## 2. Perguntas que mudam de status

Reclassificação sobre a lista de `20-perguntas-do-briefing.md`. **Novo agregado: 15
respondíveis, 10 parciais, 9 não respondíveis — e os 9 são definitivos.**

| # | Pergunta | Antes | Agora | Motivo |
|---|---|---|---|---|
| B2 | Quando a categoria é buscada sem marca, quem aparece no top 10? | OK | **NÃO** | As colunas `Competitors` e `Competitor on TOP 10` estão **vazias nos oito arquivos**. A coluna existe, o dado não veio |
| D4 | Quem são os captores que não são fabricantes? | PARC | **NÃO** | Mesma causa |
| E5 | A demanda migra para marketplace antes de chegar à marca? | PARC | **NÃO** | Mesma causa |
| D2 | As marcas asiáticas já aparecem na demanda? | PARC | **OK** | A lista da Haier chegou; Hisense e Midea já estavam |
| D3 | A Haier já disputa a demanda de serviço e pós-venda? | NÃO | **PARC** | Respondível para a demanda de marca dela (2,1%), não para o território da categoria |

Permanecem **não respondíveis, agora em definitivo**: A1 (tamanho da demanda de vida com o
produto), A4 (quem captura a demanda de serviço), C3 (relevância além da compra), F4 (o que a
IA responde em perguntas branded), G1 (valor da demanda não capturada) e G2 (ROAS e
contribuição para a receita).

---

## 3. Limpezas aplicadas

Pipeline em `20-normalizado/normalizar.py`, relatório em `20-normalizado/qualidade.md`.

| Dataset | Entrada | Saída limpa | O que foi removido |
|---|---:|---:|---|
| `keywords.csv` | 5.052 linhas em 8 arquivos | **4.965** | 11 duplicatas entre arquivos, 76 queries em idioma estrangeiro |
| `ai_prompts.csv` | 4.000 prompts + 150 perguntas | **4.045** | 105 prompts fora de categoria |
| `ai_respostas.csv` | 749 linhas em formato largo | **3.745** | convertido para formato longo: pergunta × provedor × marca |

Regras aplicadas, todas reversíveis a partir de `00-raw/`:

1. **Deduplicação por keyword** — o registro de maior volume prevalece; a origem completa fica
   na coluna `fontes`.
2. **Filtro de idioma** — francês, inglês e espanhol capturados na base `br`. Heurística por
   vocabulário, deliberadamente conservadora: na dúvida, mantém como português.
3. **Filtro de categoria** — prompts sobre saúde, conferências e conteúdo em latim presentes
   nos arquivos `prompts_by_topic`.
4. **Reconstrução do volume corrente** — `vol_i = Volume × T_i / média(T)`. Corrige a distorção
   que a média de 12 meses impõe a marcas de entrada recente. Premissa declarada, confiança
   média.
5. **Respostas de IA de formato largo para longo** — habilita leitura por marca, por provedor e
   por família.

Nada foi apagado: `00-raw/` e o zip original permanecem intactos, e o pipeline é reexecutável.

---

## 3B. A forma exata da lacuna — corrigido

Registro de uma correção. Eu vinha descrevendo a limitação como "todos os seeds são de marca,
logo o dado é cego para o ecossistema". Isso está **errado na letra**: existe um arquivo
não-branded, e ele não é pequeno em peso. A descrição correta é outra, e é mais útil.

**Composição branded × não-branded no dataset limpo (4.965 keywords, 12,87M de volume):**

| Origem | Keywords | Volume | % do volume | Branded? |
|---|---:|---:|---:|---|
| `genericas` | 65 | 6.869.800 | **53,4%** | 0% branded |
| `electrolux` | 900 | 711.670 | 5,5% | 100% branded |
| `brastemp` | 1.998 | 2.949.270 | 22,9% | 100% branded |
| `consul` | 1.064 | 1.483.110 | 11,5% | 100% branded |
| `midea` | 101 | 552.800 | 4,3% | 99% branded |
| `hisense` | 493 | 172.660 | 1,3% | 100% branded |
| `samsung` | 300 | 125.460 | 1,0% | 100% branded |
| `haier` | 44 | 4.480 | 0,03% | 100% branded |

Os arquivos de marca **não contêm termo genérico nenhum** — uma única keyword não-branded em
todos eles somados. E o arquivo de genéricas é composto exclusivamente de **cabeças de
categoria**: `air fryer` (823.000), `geladeira` (823.000), `ar condicionado` (673.000),
`microondas` (550.000). Mediana de 3 palavras; 11 das 65 têm uma palavra só.

**O dataset tem dois quadrantes de quatro:**

|  | Cabeça | Cauda longa |
|---|---|---|
| **Não-branded** | presente — 65 kw, 105k de volume médio | **ausente** |
| **Branded** | presente | presente — 4.899 kw, 1.224 de volume médio |

O quadrante ausente é a **cauda não-branded**, e é exatamente onde vive a demanda de serviço,
uso, defeito e como-fazer — ninguém digita "assistência técnica" em duas palavras.

**Consequência para a leitura.** A composição de vida com o produto mede 4,41% no branded e
0,26% no não-branded. A razão de 16,7x entre os dois **não deve ser citada**: ela é artefato do
não-branded ser uma amostra só de cabeças, que por construção não pode conter cauda de serviço.
O 0,26% não é evidência de ausência de demanda — é evidência de que cabeça é cabeça.

A comparação legítima da mesma natureza é a do corpus de IA — 12,1% no branded contra 5,7% na
categoria —, porque lá os dois recortes têm a mesma forma. É essa razão, de 2,1x, que sustenta
H1'. A de busca entra apenas como direção coerente, nunca como número.

## 4. O que o job entrega com o pacote fechado

**Entrega:**
- Leitura completa de AI search — cobertura, posição e sentimento por marca em 150 perguntas
  não-branded × 5 provedores, mais 12 meses de tráfego real vindo de LLM.
- Diagnóstico de territórios anunciados e vagos, para Electrolux, Haier e sustentabilidade.
- Composição da demanda de categoria por família e por intenção, sobre 4.965 keywords limpas.
- A leitura do vão entre awareness e consideração pela ótica de busca branded vs não-branded.
- Inventário de perguntas que a marca poderia responder com conteúdo próprio — o material mais
  rico e menos explorado do pacote.
- O seed list derivado empiricamente, pronto para quando houver como puxar.

**Não entrega, e vai dizer isso:**
- Tamanho de mercado do ecossistema em volume de busca.
- Quem captura cada keyword hoje.
- Qualquer elo entre busca e receita, conversão ou ROAS.
- A leitura de AI search em perguntas branded.

Essa lista de "não entrega" vira uma seção do entregável final, com o que resolveria cada
item. Lacuna declarada é método; lacuna preenchida por suposição não é (R5).
