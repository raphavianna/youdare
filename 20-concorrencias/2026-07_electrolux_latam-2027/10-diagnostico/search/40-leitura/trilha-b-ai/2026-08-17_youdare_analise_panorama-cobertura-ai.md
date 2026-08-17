# Panorama de IA — o tamanho da demanda mediada e quanto dela tem dono

**M1 × P4.** *A pergunta: qual o tamanho da conversa mediada por assistente, como ela se
distribui pela jornada, e quanto dela nenhuma marca ocupa?*

Fontes: 16 exports de tópico (`00-raw/ai-search/topicos/`) · 9 exports de prompt
(`00-raw/ai-search/2026-08-17_ai-prompts_*`) · 1 export de tópicos de marca
(`00-raw/ai-search/brand-topics/`). Normalizados por `20-normalizado/normalizar_ai.py`.

---

## 1. A regra de leitura que vem antes de qualquer número

**Todo export para em 1.000 linhas.** O universo é censurado por seed. Os percentuais deste
documento descrevem **demanda mapeada**, não demanda total, e cada seed novo alarga o mapa.
Isso não invalida a leitura; delimita o que ela mede.

**Os 16 exports de tópico foram semeados só com termos de categoria.** Nenhum seed carrega
nome de marca, então marca que aparece no nome de um tópico foi descoberta pela ferramenta e
não plantada por nós. **A cobertura por nome de tópico, portanto, não tem viés de seed**, e é a
medida primária deste material. Ela é sempre calculada sobre o total da demanda da categoria.

**Os exports de prompt, ao contrário, são semeados por marca.** Quatro dos cinco seeds são
nomes de fabricante, e três marcas do conjunto (Consul, Samsung e Haier) não têm seed nenhum.
Qualquer contagem de marca sobre o conjunto completo de prompts herda esse viés. Onde a leitura
depende de citação de marca, ela usa **só o recorte do seed sem marca** (943 respostas).

---

## 2. O universo

| Etapa | Tópicos | O que sai e por quê |
|---|---:|---|
| Exportados | 9.175 | 16 seeds de categoria |
| Brasil | 7.445 | 1.730 tópicos dos Estados Unidos ficam fora de todo agregado |
| **Sobre a categoria** | **3.056** | 59% do recorte Brasil é vazamento de clustering e não menciona aparelho |

**22,6 milhões de volume** e **82.919 prompts** dentro desses tópicos. Dos prompts, 3.410 foram
lidos um a um, em quatro provedores.

A leitura anterior trabalhava com 2.324 tópicos e 18,2 milhões de volume. Com a base ampliada,
**a posse sobe de 8,4% para 13,8%** da demanda mediada: ampliar o universo aumentou o peso do
território de vida com o produto, como se esperava, e agora isso está medido.

---

## 3. Cobertura geral: 81,2% da demanda não nomeia fabricante

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

É a mesma leitura do estágio 0 da parte de busca, em patamar mais alto: 54,1% da demanda de
busca não nomeia fabricante, contra 81,2% em IA.

Duas leituras que não estavam dadas:

**A Electrolux é a marca mais presente da categoria em IA**, com 5,7% do volume total, três
vezes a Brastemp. É a segunda fonte independente a apontar isso: a leitura de citação nas
respostas já colocava a marca em primeiro.

**As marcas fora do conjunto declarado somam mais que a líder**, 7,1% contra 5,7%. O conjunto
competitivo do briefing não cobre tudo que a IA nomeia, e a categoria em ambiente mediado é
mais fragmentada do que a disputa entre as sete sugere.

---

## 4. A jornada, e onde o descoberto se concentra

Estágio derivado por regra declarada: a família diz qual necessidade o tópico expressa, o
intent da ferramenta diz com que disposição. `informational` é 53,2% do volume e reúne
tanto "qual a melhor geladeira" quanto "como limpar a geladeira", e só o cruzamento separa as
duas.

| Estágio | Volume | % | Prompts | **Sem marca** |
|---|---:|---:|---:|---:|
| Exploração de categoria | 11.220.497 | 49,6% | 45.050 | 75,7% |
| **Escolha e compra** | 6.688.851 | 29,6% | 16.948 | **93,3%** |
| **Posse** | 3.114.923 | 13,8% | 11.048 | **89,4%** |
| Descoberta de marca | 1.584.710 | 7,0% | 9.873 | 54,1% |

**A escolha é o estágio mais desocupado da jornada.** 93,3% do volume do momento em que a
compra se decide não nomeia fabricante nenhum. É o achado mais acionável desta leitura:
espera-se que a marca exista no estágio da decisão, e é nele que ela menos aparece na conversa
mediada.

**A posse pesa o dobro da descoberta e está 89,4% vazia.** Os maiores tópicos sem marca do
estágio são `Ar condicionado 9000 BTU (split/inverter)` (263.219), `Air Fryer: Receitas e Usos`
(189.428) e `Robo Aspirador e Limpeza` (167.007). É o mesmo vão que a parte de busca já mostrou, agora
medido por outra fonte e com quatro vezes mais base.

**Descoberta é o único estágio em que as marcas ocupam quase metade**, o que é esperado, já
que o estágio é definido por nomear a marca. O dado relevante é ele valer só 7,0% do volume.

---

## 5. Ocupação real: presença e ocupação medem coisas diferentes

Esta medida existe por domínio e está calculada para `brastemp.com.br`.

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

**A marca com a maior base instalada da categoria ocupa 8,2% da demanda mediada por IA.** Esse
é o patamar de quem lidera em base instalada, e situa o tamanho do território vago para os
demais players.

A ocupação é mais baixa na posse, 4,9%. É a terceira fonte independente a apontar o mesmo vão,
agora em outra marca, o que indica característica da categoria em ambiente mediado e não um
problema específico da Electrolux.

**Alcance desta medida.** Ela existe por domínio e está calculada para um domínio do conjunto.
A comparação entre players depende de ter a mesma medida para cada um, e até lá a leitura de
cobertura por marca é a do nome do tópico, sobre o total da demanda.

---

## 6. Os prompts: a maioria das respostas não traz fabricante

Recorte limpo, só as 943 respostas do seed sem marca. É o único em que citar um fabricante é
decisão do modelo e não eco do prompt.

| Família | n | Cita alguma das sete |
|---|---:|---:|
| Preço e compra | 235 | 33,2% |
| Comparação e modelo | 189 | 22,2% |
| Produto e categoria | 363 | 21,2% |
| Consumo e energia | 76 | 11,8% |
| Peça e filtro | 34 | **8,8%** |

**23,6% das respostas nomeiam alguma das sete marcas.** O padrão é específico: perguntas
explícitas de marca, como `Quais são os melhores fabricantes de geladeiras comerciais para
supermercados?` e `Quais marcas de geladeira são mais confiáveis no Brasil e onde comprar?`,
costumam ser respondidas **sem citar nenhuma delas**, e sem substituí-las por outro fabricante.

Uma resposta cita 2,8 marcas em média e apoia-se em 7,4 fontes. Não há segunda página: a marca
não citada fica fora do resultado que o consumidor lê.

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
  diferentes, e toda comparação entre as duas fontes é de posição relativa dentro de cada uma.
- **Cobertura, neste material, é sempre sobre o total da demanda da categoria.** Nunca sobre a
  fatia já ocupada pelas marcas.

---

## O que eu faria a seguir

1. **Abrir a defesa pelo par 81,2% e 93,3%**, o que já está feito no slide 3 do material. Com
   ele, "ocupar o ecossistema" deixa de ser ambição de posicionamento e passa a ser um espaço
   medido, com tamanho e endereço.
2. **Estender a medida de ocupação aos demais domínios do conjunto.** É a medida mais dura do
   pacote e hoje está calculada para um concorrente, não para o cliente.
3. **Fechar a integração com a trilha C.** A posse aparece vazia em busca, em citação de IA e
   em ocupação de domínio. A convergência entre três fontes independentes é o argumento mais
   forte que este diagnóstico produziu até aqui.
