# Panorama de IA — o tamanho da demanda mediada e quanto dela tem dono

**M1 × P4.** *A pergunta: qual o tamanho da conversa mediada por assistente, como ela se
distribui pela jornada, e quanto dela nenhuma marca ocupa?*

Fontes: 16 exports de tópico (`00-raw/ai-search/topicos/`) · 9 exports de prompt
(`00-raw/ai-search/2026-08-17_ai-prompts_*`) · 1 export de tópicos de marca
(`00-raw/ai-search/brand-topics/`). Normalizados por `20-normalizado/normalizar_ai.py`.

---

## 1. A regra de leitura que vem antes de qualquer número

**Todo export para em 1.000 linhas.** O universo é censurado por seed. Os percentuais deste
documento descrevem **demanda mapeada**, não demanda total — e cada seed novo alarga o mapa.
Isso não enfraquece a leitura: fixa o que ela é.

**Os 16 exports de tópico foram semeados só com termos de categoria.** Nenhum seed carrega
nome de marca. Marca que aparece no nome de um tópico foi descoberta pela ferramenta, não
plantada por nós — **por isso a cobertura por nome de tópico não tem viés de seed** e é a
medida primária deste material.

**Os exports de prompt, ao contrário, são semeados por marca.** Quatro dos cinco seeds são
nomes de fabricante e três marcas do conjunto — Consul, Samsung e Haier — não têm seed nenhum.
Qualquer contagem de marca sobre o conjunto completo de prompts herda esse viés. Onde a leitura
depende de citação de marca, ela usa **só o recorte do seed sem marca** (943 respostas).

---

## 2. O universo

| Etapa | Tópicos | O que sai e por quê |
|---|---:|---|
| Exportados | 9.175 | 16 seeds de categoria |
| Brasil | 7.445 | 1.730 tópicos dos Estados Unidos ficam fora de todo agregado |
| **Sobre a categoria** | **3.056** | 59% do recorte Brasil é vazamento de clustering — não menciona aparelho |

**22,6 milhões de volume** e **82.919 prompts** dentro desses tópicos. Dos prompts, 3.410 foram
lidos um a um, em quatro provedores.

Contra a leitura anterior — 2.324 tópicos e 18,2 milhões — é outro dataset. E a diferença muda
uma conclusão: com a base ampliada, **a posse sobe de 8,4% para 13,8%** da demanda mediada.
Ampliar o universo aumentou o peso do território de vida com o produto, que era exatamente o
que se esperava e agora está medido.

---

## 3. Cobertura geral: quatro em cada cinco reais de atenção não têm dono

| | Tópicos | Volume | % |
|---|---:|---:|---:|
| **Sem marca nenhuma** | 2.275 | **18.370.167** | **81,2%** |
| Outras marcas (LG, Philco, Mondial, Britânia…) | 308 | 1.597.615 | 7,1% |
| **Electrolux** | 200 | 1.286.687 | **5,7%** |
| Brastemp | 112 | 431.319 | 1,9% |
| Midea | 49 | 354.286 | 1,6% |
| Samsung | 39 | 292.360 | 1,3% |
| Consul | 75 | 265.013 | 1,2% |
| Hisense | 8 | 57.379 | 0,3% |
| Haier | 2 | 2.994 | 0,01% |

**É o análogo direto do estágio 0 do deck de busca — e aqui ele é maior.** Em busca, 54,1% da
demanda não nomeia fabricante. Em IA, 81,2%.

Duas leituras que não estavam dadas:

**A Electrolux é a marca mais presente da categoria em IA.** 5,7% do volume, três vezes a
Brastemp. É liderança real, e é a segunda fonte independente a dizer isso — a leitura de
cobertura em resposta já apontava a marca em primeiro.

**As marcas fora do conjunto declarado somam mais que a líder.** 7,1% contra 5,7%. A categoria
em IA é mais fragmentada do que a disputa entre as sete sugere, e o conjunto competitivo
declarado no briefing não é o conjunto que a IA nomeia.

---

## 4. A jornada, e onde o descoberto se concentra

Estágio derivado por regra declarada: a família diz qual necessidade o tópico expressa, o
intent da ferramenta diz com que disposição. `informational` é 53,2% do volume e cobre tanto
"qual a melhor geladeira" quanto "como limpar a geladeira" — só o cruzamento separa as duas.

| Estágio | Volume | % | Prompts | **Sem marca** |
|---|---:|---:|---:|---:|
| Exploração de categoria | 11.220.497 | 49,6% | 45.050 | 75,7% |
| **Escolha e compra** | 6.688.851 | 29,6% | 16.948 | **93,3%** |
| **Posse** | 3.114.923 | 13,8% | 11.048 | **89,4%** |
| Descoberta de marca | 1.584.710 | 7,0% | 9.873 | 54,1% |

**A escolha é o estágio mais desocupado da jornada.** 93,3% do volume do momento em que a
compra se decide não nomeia fabricante nenhum. É contraintuitivo e é o achado mais acionável
desta leitura: espera-se que a marca exista onde se escolhe, e é justamente ali que ela menos
existe na conversa mediada.

**A posse pesa o dobro da descoberta e está 89,4% vazia.** Os maiores tópicos sem marca do
estágio são `Ar condicionado 9000 BTU (split/inverter)` (263.219), `Air Fryer: Receitas e Usos`
(189.428) e `Robo Aspirador e Limpeza` (167.007). É o mesmo vão que a busca já tinha mostrado,
agora medido por outra fonte e com quatro vezes mais base.

**Descoberta é o único estágio em que as marcas ocupam quase metade.** Faz sentido — é o
estágio definido por nomear a marca. Que ele seja só 7,0% do volume é a informação.

---

## 5. Ocupação real: aparecer não é ocupar

Esta é a medida do ponto 4, e ela existe por domínio. Só um domínio foi exportado.

**Brastemp — `brastemp.com.br`**, 1.000 tópicos, 621 dentro do universo mapeado de categoria:

| Medida | Valor | O que é |
|---|---:|---|
| **Presença** | **19,2%** | Volume dos tópicos em que a marca aparece de algum modo |
| **Ocupação** | **8,2%** | A mesma presença, ponderada pela visibilidade dentro de cada tópico |
| Visibilidade mediana | 35 | Nos tópicos em que aparece, ocupa cerca de um terço do espaço |

| Estágio | Presença | Ocupação | **Descoberto** |
|---|---:|---:|---:|
| Exploração de categoria | 18,6% | 8,2% | 81,4% |
| Descoberta de marca | 15,5% | 7,7% | 84,5% |
| Escolha e compra | 23,2% | 9,8% | 76,8% |
| **Posse** | 14,5% | **4,9%** | **85,5%** |

**A marca com a maior base instalada da categoria ocupa 8,2% da demanda mediada por IA.** Se
esse é o teto de quem lidera em base, o território vago não é resíduo — é a regra da categoria.

E a ocupação é mais baixa justamente na posse, 4,9%. Terceira fonte independente a apontar o
mesmo vão, agora em outra marca: não é um problema da Electrolux, é uma característica de como
a categoria inteira se comporta em ambiente mediado.

**O que falta.** Seis domínios sem export: `loja.electrolux.com.br`, `consul.com.br`,
`midea.com.br`, `samsung.com.br`, e os domínios BR de Hisense e Haier. O método está montado e
provado numa marca; os outros entram sem nenhuma mudança de estrutura.

---

## 6. Os prompts: a IA responde sem nomear fabricante

Recorte limpo — só as 943 respostas do seed sem marca, o único em que citar um fabricante é
decisão do modelo e não eco do prompt:

| Família | n | Cita alguma das sete |
|---|---:|---:|
| Preço e compra | 235 | 33,2% |
| Comparação e modelo | 189 | 22,2% |
| Produto e categoria | 363 | 21,2% |
| Consumo e energia | 76 | 11,8% |
| Peça e filtro | 34 | **8,8%** |

**Só 23,6% das respostas nomeiam alguma das sete marcas.** E o padrão é específico: perguntas
explícitas de marca — `Quais são os melhores fabricantes de geladeiras comerciais para
supermercados?`, `Quais marcas de geladeira são mais confiáveis no Brasil e onde comprar?` —
são respondidas **sem citar nenhuma delas**. A IA não está escolhendo outro fabricante; está
respondendo sem fabricante.

Uma resposta cita 2,8 marcas em média e apoia-se em 7,4 fontes. Quem não está citado não perde
posição — não existe na resposta. Não há segunda página em IA.

---

## 7. Limites

- **Teto de 1.000 linhas por export.** Todo percentual é sobre demanda mapeada.
- **A cobertura por nome de tópico mede o que é perguntado**, não quem a IA cita ao responder.
  São perguntas diferentes e o material as mantém separadas.
- **As marcas nas respostas vêm de busca de string no texto.** A ferramenta entrega a contagem,
  não os nomes. Aproximação declarada.
- **`sources_count` vem zero em 20% das linhas** porque o Google AI Mode não reporta fontes.
  Ausência de dado, não ausência de fonte.
- **O estágio é regra, não medição** — família cruzada com intent, com cortes em 25% e 45%.
- **A ocupação existe para um domínio de sete.**
- **1.730 tópicos dos Estados Unidos** ficaram fora de todos os agregados e seguem disponíveis.
- **Volume de IA e volume de busca não se somam.** Medem coisas diferentes, em unidades
  diferentes. Toda comparação entre as duas fontes é de posição relativa dentro de cada uma.

---

## O que eu faria a seguir

1. **Abrir a defesa pelo par 81,2% e 93,3%.** Quatro em cada cinco reais de atenção mediada não
   têm dono, e no momento da escolha são nove em cada dez. Transforma "ocupar o ecossistema" de
   ambição de marca em espaço mensurável e vago — que é o que a banca precisa ver.
2. **Puxar os seis exports de `brand_topics` pendentes.** É o único bloqueio real do panorama:
   a ocupação por domínio é a medida mais dura do pacote e hoje existe para um concorrente, não
   para o cliente.
3. **Fechar a integração com a trilha C.** A posse aparece vazia em busca, em cobertura de IA e
   agora em ocupação de domínio — três fontes independentes. Convergência tripla é o argumento
   mais forte que este diagnóstico produziu até aqui.
