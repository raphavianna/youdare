---
description: Gera o material executivo de dados, insights e tendências da concorrência para as áreas internas, via frontend-slides
---

Você vai produzir o material executivo de dados, insights e tendências da concorrência
Electrolux LATAM 2027, para apresentação às áreas internas da Youdare.

## Antes de qualquer coisa: leia as fontes

Todo número deste material vem de arquivo. Leia, nesta ordem, e não produza nada antes:

1. `20-concorrencias/2026-07_electrolux_latam-2027/CLAUDE.md` — o contexto da concorrência
2. `.../10-diagnostico/search/00-briefing/_sumario.md` — os fatos do briefing do cliente
3. `.../10-diagnostico/search/40-leitura/trilha-a-search/` — a leitura de busca, isolada
4. `.../10-diagnostico/search/40-leitura/trilha-b-ai/` — a leitura de IA, isolada
5. `.../10-diagnostico/search/40-leitura/trilha-c-integracao/` — a integração e o veredito
6. `.../10-diagnostico/search/20-normalizado/keywords.csv` — 4.965 keywords por player, com
   família, categoria, intenção, volume e série de 12 meses
7. `.../10-diagnostico/search/20-normalizado/ai_respostas.csv` — pergunta × provedor × marca
8. `.../10-diagnostico/search/00-revisao-de-escopo.md` — os limites do pacote

Quando precisar de um recorte que não está nas leituras, calcule a partir dos CSVs
normalizados. Registre o cálculo num script em `.../30-analise/` para que qualquer número do
deck possa ser reproduzido.

## Regra que vale para todos os slides, sem exceção

**Nenhum número entra neste material sem estar nos arquivos acima ou ser calculável a partir
deles.** Não estime, não arredonde de memória, não complete uma série incompleta e não invente
benchmark de mercado. Se um slide que você planejou precisa de um número que não existe,
**troque o slide** — não preencha a lacuna.

Esta regra vale para as duas partes do material, para o apêndice e para qualquer texto de
apoio, não apenas para o primeiro caso.

## O que este material é e o que ele não é

**É:** um panorama de dados, insights e tendências sobre o mercado, os players e a jornada do
consumidor, para que estratégia, criação, IPs e produtos trabalhem em cima.

**Cada slide entrega o dado e a leitura dele:** a observação com número e recorte, a causa
provável quando o dado sustentar, e a implicação para o negócio da marca.

**Não é, e você não vai fazer:** recomendação de território, de mensagem, de plano de mídia ou
de ação. Essa decisão pertence às áreas que vão receber o material. Pare na implicação.

## Estrutura — duas partes

**Abertura (3 a 4 slides).** O que foi medido e contra quem: o conjunto competitivo declarado
pelos arquivos, o tamanho do dataset, o recorte Brasil, e o desafio do briefing em uma linha —
converter reconhecimento de marca em intenção de compra no momento da decisão.

**PARTE 1 — OS PLAYERS (18 a 22 slides).** Um bloco por player, na ordem: Electrolux, Brastemp,
Consul, Samsung, Midea, Hisense, Haier. Cada bloco cobre, quando o dado existir:

- **Estado atual** — composição da demanda por estágio de jornada (descoberta, escolha, posse),
  volume, intenção dominante, e as maiores consultas.
- **Evolução recente** — a série de 12 meses em share relativo à categoria, não em volume
  bruto. Todos os players têm pico nos mesmos meses porque a categoria é sazonal; a leitura de
  crescimento só vale depois de descontar isso.
- **Categorias e produtos** — em quais categorias do portfólio a demanda daquele player se
  concentra, e como isso se compara ao conjunto.
- **Presença em IA** — cobertura nas respostas, posição e sentimento, para os players que as
  fontes de IA cobrem. Electrolux, Brastemp, Consul, Samsung e Midea estão nas respostas;
  Hisense e Haier não. Diga isso no slide em vez de deixar o espaço vazio.

Feche a parte 1 com 2 a 3 slides **comparativos entre todos os players**, lado a lado.

**PARTE 2 — A JORNADA (12 a 16 slides).** A leitura da categoria por momento do consumidor:

- Os três estágios — descoberta, escolha, posse — com o peso de cada um e quem ocupa cada um.
- O território que nenhum player reivindica, e o que ele contém.
- A demanda mediada por IA: onde ela se concentra e como se compara à demanda de busca.
- Categorias e produtos: onde a demanda da categoria está, por momento da jornada.
- As convergências e as divergências entre as duas fontes.

**Fechamento (2 a 3 slides).** Os achados mais fortes do material, em forma de dado com
leitura. Sem recomendação.

**Apêndice.** Método, fontes, e — obrigatoriamente — a lista nominal dos números do deck que
são frágeis, com o motivo de cada um: amostra pequena, artefato de seed, coluna de dado vazia,
cobertura parcial de player, classificação automática. Quem for construir em cima precisa
conseguir checar.

Total: 35 a 45 slides, apêndice incluído.

## Composição de cada slide

**80% do slide é dado: gráfico, tabela, número grande, matriz ou série. 15 a 20% é texto.**
Na prática, cada slide tem no máximo cerca de **60 a 70 palavras** de texto, distribuídas em
um título afirmativo e uma ou duas frases curtas de leitura.

- **O título afirma o achado**, não nomeia o assunto. "Electrolux é a mais citada em IA e a
  pior falada entre as três grandes" funciona; "Presença em IA" não.
- **Um slide, um achado.** Se há dois achados, há dois slides.
- **Sem bullet descritivo.** Se o texto está descrevendo o que o gráfico mostra, corte o texto.
  O texto existe para dizer o que o gráfico **significa**.
- **Todo número no gráfico**, não no texto. O texto não repete número que já está visível.
- Todo slide carrega a **fonte** em rodapé discreto: qual arquivo e qual recorte.

## Construção

Use a skill **`/frontend-slides`** para construir a apresentação em HTML.

Use a skill **`/dataviz`** antes de definir os gráficos: num material que é 80% dado, a escolha
de forma, escala e cor decide se o achado aparece ou se perde. Vale especialmente para as
séries de 12 meses, para as composições por estágio de jornada e para as matrizes de player ×
categoria.

Português do Brasil, com termos técnicos de mídia em inglês onde é padrão de mercado.
Identidade visual neutra, de agência — este é material interno da Youdare, não peça de marca
Electrolux.

## Antes de gerar, planeje

Em `<planejamento>`, antes de produzir qualquer slide: liste os achados disponíveis nas três
trilhas, escolha quais sustentam um slide inteiro sozinhos, distribua-os na estrutura das duas
partes, e para cada slide declare o achado, o elemento visual e a fonte. Descarte
explicitamente o que não couber. Depois construa.

## Critério de aceitação

O material está pronto quando: todo número é rastreável a um arquivo; nenhum slide ultrapassa
o orçamento de texto; todo título afirma um achado; os sete players têm bloco próprio com a
cobertura de dado declarada quando parcial; as duas partes existem na ordem certa; o apêndice
lista os números frágeis pelo nome; e não há nenhuma recomendação de território, mensagem ou
ação em lugar nenhum.

<examples>

<example>
Contexto: slide de evolução de um player.
Fraco: título "Evolução da demanda — Brastemp", gráfico de linha com o volume mensal bruto e
três bullets descrevendo a curva.
Forte: título "Brastemp perde 14% de share de demanda em 12 meses"; gráfico de linha do share
relativo à categoria, com a linha da Brastemp destacada e as demais em cinza; um número grande
"0,86"; e uma frase: "A curva bruta sobe porque a categoria é sazonal e todos os players picam
nos mesmos meses. Contra a categoria, a Brastemp cai." Fonte em rodapé.
</example>

<example>
Contexto: slide de jornada comparando players.
Fraco: tabela com sete players e doze famílias de demanda, todos os números em corpo pequeno.
Forte: título "Só a Consul converteu base instalada em demanda de pós-compra"; gráfico de
barras empilhadas com os três estágios — descoberta, escolha, posse — para os sete players,
ordenado pela fatia de posse, com Consul e Electrolux destacadas; uma frase: "Consul tem 8,1%
da demanda em vida com o produto; Electrolux, 4,4%, apesar de posicionamento superior."
</example>

<example>
Contexto: um slide planejado precisa de um número que não existe nos arquivos — por exemplo,
quanto da demanda de serviço cada player captura hoje.
Fraco: estimar a captura a partir do volume, ou apresentar a demanda como se fosse captura.
Forte: trocar o slide. Substituir por um que o dado sustenta — por exemplo, o tamanho e a
composição da demanda que nenhum player reivindica — e registrar no apêndice que a captura por
player não é medível com este pacote, porque a coluna de competidor veio vazia.
</example>

<example>
Contexto: slide de categoria e produto por player.
Fraco: lista de categorias por player em texto corrido.
Forte: título "Ar condicionado concentra a demanda de pós-compra da categoria"; matriz de calor
com players nas linhas e categorias nas colunas, célula colorida pelo peso da categoria dentro
do player; uma frase de leitura sobre o padrão que a matriz revela. Todo número na matriz,
nenhum repetido no texto.
</example>

<example>
Contexto: um player tem cobertura parcial nas fontes — Hisense e Haier não aparecem nas
respostas de IA.
Fraco: omitir o slide de IA daquele player sem explicação, ou preencher com o dado de busca
fingindo que é de IA.
Forte: manter o slide com a estrutura dos demais, exibir o que existe de busca, e marcar
visualmente o quadrante de IA como "sem cobertura nesta fonte", com a razão em cinco palavras.
A ausência de dado é informação sobre a fonte, e o leitor precisa vê-la.
</example>

</examples>
