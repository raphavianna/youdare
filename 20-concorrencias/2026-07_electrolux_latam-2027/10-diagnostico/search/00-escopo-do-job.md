# Carta do job — Inteligência de search para o pitch Electrolux

**Célula da matriz:** M1 × P4, com fronteira em P2 (campo competitivo) e P9 (sinal de cultura).

**Pergunta do job:** quando a categoria da casa é acionada, quanta demanda existe, em quais
momentos, quem a captura hoje, e o que isso implica para o pedido central do case Brasil — sair
de marca de produtos para marca-ecossistema.

**Papel assumido:** Head de Data & Insights da conta. O produto desta etapa é planejamento,
insight e tendência — insumo para estratégia, criação, mídia, social, retail e D2C. Não é o
plano de mídia nem a estratégia; é o que os sustenta.

---

## 1. Escopo

- **Mercado:** Brasil. Colômbia fora do escopo nesta rodada. Se vier dado de CO nos exports,
  fica segregado e não entra em nenhum agregado.
- **Fontes:** SEMrush (majoritário) e SimilarWeb. Busca convencional e busca mediada por IA.
- **Conjunto competitivo:** **declarado pelos arquivos.** Os players são extraídos dos exports
  recebidos e registrados como o denominador de todo share produzido neste job. Ausência
  relevante é sinalizada, nunca preenchida por conhecimento geral (R2).
- **Dois denominadores possíveis:** se o dado permitir, o conjunto competitivo do *produto*
  (fabricantes) e o do *ecossistema* (marketplaces, conteúdo, assistência independente) são
  registrados separadamente. Não se misturam num share único.

## 2. Postura de hipótese

**H1 — hipótese líder, a confirmar ou refutar.** Existe volume relevante de demanda de "vida
com o produto" — instalação, assistência, peça, manutenção, uso, receita, consumo, garantia,
troca, descarte — hoje capturada por terceiros, e esse volume é o tamanho de mercado do
ecossistema medido em busca.

**Critério de refutação, escrito antes da análise.** H1 é considerada **não sustentada** se o
dado mostrar qualquer um destes:
- a demanda de vida com o produto for marginal frente à demanda de aquisição na taxonomia de
  pontos de entrada;
- ela existir mas a Electrolux já a capturar em proporção semelhante à sua posição na demanda
  de aquisição, o que significaria que o ecossistema já está construído e o problema é de
  percepção, não de presença;
- ela existir e estar concentrada em pontos de entrada que a marca não tem direito nem meio de
  ocupar.

Sem um resultado possível que a derrube, H1 não é hipótese e não sai daqui como achado.

**Leitura em duas passagens, ambas obrigatórias:**

1. **Passe dirigido** — responde a lista numerada de perguntas derivada do briefing, com H1
   entre elas. Cada pergunta sai marcada: confirmada · refutada · parcialmente respondida ·
   não respondível com este dado.
2. **Passe aberto** — varredura sem hipótese, procurando sinal forte onde ninguém perguntou. O
   resultado vai para **achados não solicitados**, cada um amarrado depois ao ponto do briefing
   que ele responde. Achado forte que não responde a nenhum ponto permanece registrado: o
   briefing não é o limite do que o dado sabe.

H1 é candidata a ser o achado principal. Não é o único, e não é premissa.

## 3. Etapas

| # | Etapa | Saída |
|---|---|---|
| 0 | Organizar o repo | Estrutura, zona de pouso, esta carta |
| 1 | Inventário e auditoria dos arquivos | Dicionário de dados: o que é, período, escopo, device, método, unidade, lacunas |
| 2 | Briefing → lista numerada de perguntas | Critério de aceitação do job, cada pergunta amarrada a prática e entregável do RFP |
| 3 | Taxonomia de pontos de entrada + classificação | Taxonomia bottom-up reconciliada com a Brand House; classificador de keyword e prompt, com amostra auditada e erro medido |
| — | Construção do prompt de execução | Feita aqui, quando a forma real do dado e a lista de perguntas existem |
| 4 | Estrutura de busca convencional | Onde está a demanda, quanta, em que forma, quem captura |
| 5 | Estrutura de AI search | Onde a marca aparece no filtro, em que posição da síntese, citando qual fonte |
| 6 | Integração pela taxonomia + cenários | Matriz de prioridade, dimensionamento do ecossistema, 2 a 4 cenários |
| 7 | Cobertura vs briefing + handoff | O que ficou respondido e o que não; um brief por entregável |

**A integração acontece pela taxonomia de pontos de entrada, nunca pela métrica.** Busca
convencional entrega volume; AI search entrega presença e citação. Empilhar as duas produz
equivalência falsa. A taxonomia é a chave de junção porque keyword e prompt de assistente não
se juntam entre si, mas ambos respondem ao mesmo momento de vida do consumidor.

## 4. Limites declarados do dado

Busca mede **demanda expressa e presença**. Não mede percepção de marca, elasticidade a preço
ou distribuição, e não estabelece causalidade.

Ponto cego relevante para este briefing: **não enxerga demanda latente.** Ponto de entrada de
categoria que o consumidor ainda não sabe verbalizar não aparece em keyword nenhuma — e criar
categoria é parte do desafio de ecossistema. Esse vão será nomeado, não coberto por suposição,
e a lente que o fecha é escuta social (P9) e BHT (P1).

Volume de SEMrush é **métrica-proxy de demanda**, estimada por modelo. SimilarWeb é modelado a
partir de painel e clickstream. Ambos entram com a ressalva declarada (R4).

## 5. Em aberto

- `[a confirmar: origem da taxonomia de pontos de entrada. Default adotado — derivar bottom-up
  do dado e reconciliar depois com a Brand House do cliente, porque a distância entre "como o
  mercado pergunta" e "como a marca se organiza" é insight em si.]`
- `[a confirmar: formato da entrega final. Default adotado — canônico em markdown no padrão de
  insight, mais dataset normalizado e gráficos; deck como derivação posterior.]`
- `[a confirmar: escala dos arquivos. Acima de alguns milhares de linhas, a etapa 3 vira
  engenharia com classificador e amostra auditada, não leitura manual.]`
