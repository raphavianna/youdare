# Haier no Brasil — leitura de busca

**M1 × P2+P4.** *A pergunta: a entrada da Haier no Brasil, que o briefing nomeia como ameaça
central pelo eixo de confiança de pós-venda, já se materializou em demanda de busca — e em
qual formato?*

Fonte: `00-raw/busca-convencional/2026-08-17_semrush_keywords_haier.csv`, 100 keywords, base
`br`, baixado em 17/08/2026. Reprodução: `30-analise/haier_analise.py`.
Contexto de negócio informado pela cadeira: **operação iniciada em março de 2026.**

---

## Achado principal

**A Haier ainda não é um problema de demanda. É um problema de território vago.**

A marca representa **0,76% da demanda de busca da Electrolux** na janela pós-lançamento, sua
demanda é majoritariamente **curiosidade de marca e não intenção de categoria**, sua pegada de
categoria está fora do core de disputa com a Electrolux, e **o eixo declarado da estratégia
dela — confiança de pós-venda — não existe em busca**: 1,3% do volume em serviço, 0,8% em
avaliação de confiança.

A consequência estratégica inverte a leitura defensiva. O entrante anunciou a intenção de
disputar o terreno de serviço e confiança, mobilizou estrutura para isso, **e ainda não
converteu nada disso em demanda**. A janela para a Electrolux ocupar esse território antes
está aberta — e é mensurável quanto ela ainda está aberta.

---

## 1. Correção de método: o volume médio subestima a marca

`Volume` no SEMrush é média dos 12 meses. Uma marca que começou a operar em março de 2026
carrega cinco meses de quase zero dentro dessa média. Comparar o volume médio da Haier com o
da Electrolux, sem correção, subestima a entrante.

Reconstruí a série mensal absoluta a partir de `Volume` e do campo `Trend`, sob a premissa de
que `Trend` é o índice mensal normalizado pelo pico (`vol_i = Volume × T_i / média(T)`).
Premissa declarada, não medida (R3, confiança média).

**Série mensal reconstruída, subconjunto PT-BR, do mais antigo ao mais recente:**

```
3.386  6.991  2.352  2.729  2.805  3.978  3.167 │ 7.016  6.307  4.607  5.103  5.318
                                      pré-março │ pós-março/26
```

| Medida | Haier | Electrolux | Haier / Electrolux |
|---|---:|---:|---:|
| Média 12 meses | 4.480 | 712.860 | 0,63% |
| **Média pós-março/26** | **5.670** | **745.910** | **0,76%** |
| Último mês | 5.318 | 727.204 | 0,73% |
| Termo puro da marca | 2.116 | 122.685 | 1,73% |

A correção importa — ela eleva a Haier de 0,63% para 0,76% —, **e não muda a conclusão de
ordem de grandeza**. O crescimento do ponto 7 ao 12 é de +68%, mas sobre base tão pequena que
o percentual é frágil como indicador. A série também tem um pico anterior ao lançamento (ponto
2, 6.991), o que indica ruído relevante nesse nível de volume.

---

## 2. Limpeza obrigatória: 40% do arquivo não é demanda brasileira

| Idioma da query | Keywords | Volume médio | % do volume |
|---|---:|---:|---:|
| Português | 45 | 4.380 | 59,5% |
| **Francês** | **27** | **1.690** | **23,0%** |
| **Inglês** | **26** | **1.240** | **16,8%** |
| Espanhol | 2 | 50 | 0,7% |

Mais da metade das keywords do arquivo está em francês ou inglês — `lave linge haier`,
`cave a vin haier`, `congelateur armoire haier`, `haier washing machine`, `haier fridge`. São
herança da operação internacional da marca capturada dentro da base `br`.

O padrão temporal confirma: quase todas têm assinatura `██▁▁▁▁▁▁▁▁▁▁` — pico no primeiro ponto
e zero depois, que é comportamento de dado espúrio ou descontinuado, não de demanda real.

**Analisar o arquivo sem essa limpeza infla a Haier em cerca de 40%.** Todas as leituras deste
documento usam apenas o subconjunto PT-BR.

---

## 3. A demanda é curiosidade de marca, não intenção de compra

Composição do volume corrente, subconjunto PT-BR:

| Família | Keywords | Volume | % |
|---|---:|---:|---:|
| **Marca pura / curiosidade** | 5 | 2.835 | **53,3%** |
| Ar condicionado | 15 | 1.188 | 22,3% |
| TV | 4 | 689 | 13,0% |
| Adega | 7 | 255 | 4,8% |
| Geladeira / MDA | 2 | 258 | 4,8% |
| **Serviço / pós-compra** | 3 | 68 | **1,3%** |
| **Confiança / avaliação** | 2 | 43 | **0,8%** |
| Comunicação / patrocínio | 1 | 19 | 0,4% |

Mais da metade do volume está em `haier`, `haier brasil`, `marca haier`,
`haier eletrodomésticos` e `haier elegance`. As pessoas estão perguntando **quem é essa
marca** — não *quero comprar uma geladeira Haier*.

Esse é o estágio mais inicial possível de formação de demanda, e é exatamente o que se espera
de uma marca com cinco meses de operação e investimento em familiaridade. Não é fraqueza da
Haier; é o calendário dela.

### Onde o crescimento é sustentado e onde é pico isolado

Distinguir importa, porque razão entre médias não separa as duas coisas. Olhando os três
últimos pontos da série:

**Alta sustentada** — três keywords: `haier brasil` (0,54 → 0,66 → 1,00 → 1,00),
`haier eletrodomésticos` (0,18 → 1,00 → 1,00 → 1,00) e `geladeira haier` (0,52 → 0,66 → 1,00 →
1,00). Duas de identidade de marca, uma de categoria MDA — e é a única keyword de categoria
core que mostra formação real de demanda.

**Pico isolado, não tendência** — todo o cluster de ar condicionado mostra um salto único no
ponto 8 e retorno à linha de base. Isso é evento — promoção, sazonalidade de verão ou ação
pontual —, não formação de demanda. Ler a razão `últimos 5 / primeiros 7` sem olhar a forma da
série teria classificado esse cluster como "subindo 3x", o que seria falso.

---

## 4. A pegada de categoria está fora do core de disputa

Ar condicionado, TV e adega somam **40,1%** do volume da Haier. Geladeira e demais MDA somam
**4,8%**.

Duas implicações. A primeira: a marca não está, hoje, disputando busca nas categorias em que a
Electrolux é forte — a colisão frontal ainda não começou. A segunda, mais interessante: o
cluster de ar condicionado é **plano ao longo dos 12 meses**, o que indica presença anterior ao
lançamento oficial. A Haier já estava no Brasil por essa porta antes de "chegar".

---

## 5. O eixo declarado da estratégia deles não existe em busca

O briefing descreve a Haier entrando com confiança de pós-venda como diferencial: mais de 1.000
pontos técnicos, mais de 200 posições de atendimento, expertise em casa conectada.

Na busca, isso soma **2,1% do volume** — 1,3% em serviço e pós-compra, 0,8% em avaliação de
confiança. São cinco keywords: `adega haier assistencia tecnica` (20/mês), `adega haier manual`,
`adega haier 42 garrafas manual`, `ar condicionado haier é bom` (30/mês) e
`ar condicionado portátil haier é bom` (30/mês).

**A infraestrutura foi anunciada. A demanda por ela não existe.** Isso pode significar duas
coisas, e a distinção importa: ou a estrutura ainda não gerou base instalada suficiente para
produzir busca de pós-compra — o que é questão de tempo e vai mudar —, ou o argumento de
confiança não está pegando. O dado de busca sozinho não separa as duas. `[a confirmar: base
instalada e volume de vendas da Haier no Brasil — resolveria a ambiguidade]`

---

## 6. Divergência entre o briefing e o dado, na comunicação

O briefing cita **Eliana** (para construir familiaridade) e **Liverpool Football Club** como
movimentos de comunicação da Haier no Brasil.

| Termo buscado no arquivo | Keywords encontradas |
|---|---|
| `eliana` | **nenhuma** |
| `liverpool` | **nenhuma** |
| `roland garros` | 1 — `haier roland garros`, 30/mês |
| `patrocínio` | nenhuma |

**Ressalva importante, para não sobre-ler:** campanha com celebridade gera busca pelo nome da
celebridade, não necessariamente pela combinação `marca + celebridade`. A ausência de
`haier eliana` **não prova** que a campanha não rodou. O teste correto seria um export com seed
em `eliana` isolada, ou brand lift.

O que o dado sustenta com segurança é mais modesto e ainda assim útil: **nenhum dos dois
investimentos citados produziu, até aqui, associação buscável com a marca**. E o único
patrocínio com assinatura em busca é Roland Garros, que não está no briefing.

---

## 7. O que isso muda na tese

A leitura defensiva óbvia seria: "a Haier vem aí com serviço, a Electrolux precisa se defender".
O dado sustenta uma leitura mais forte e mais acionável.

**O território de serviço e confiança está vago.** O entrante o declarou como eixo, montou
estrutura para ele, e não o ocupa em busca. Não há evidência, no que temos, de que a Electrolux
o ocupe também — as frentes nomeadas da marca (Instala, Projeta, Cuida, Pro) somam 0,03% do
volume da base dela.

Isso reposiciona a recomendação. Não é "reagir à Haier". É **ocupar primeiro um terreno que o
concorrente já sinalizou publicamente que pretende tomar, e fazê-lo enquanto ele ainda é 0,76%
da demanda da marca**. A urgência não vem do tamanho atual da ameaça — vem da janela.

E há um espelho útil para a defesa: o cliente descreve o próprio desafio como converter
reconhecimento de marca em intenção de compra. A Haier está no mesmo problema, um estágio
atrás — 53% da demanda dela é gente perguntando quem ela é. **Quem resolver esse vão primeiro
ganha o território.** O argumento serve para os dois casos do briefing.

---

## Limites desta leitura

- **A série mensal é reconstruída**, não medida. Depende da premissa sobre o campo `Trend`
  (R3, confiança média).
- **Volume nesse patamar é ruidoso.** Diferenças de algumas centenas de buscas entre meses não
  sustentam conclusão.
- **O arquivo é branded.** Mede a demanda que já usa o nome Haier. Não mede a disputa da marca
  em busca genérica de categoria, que exigiria Organic Positions dela nas keywords não-branded
  (Tier 2 do pedido de dados).
- **Não há dado de share.** Sem posição orgânica, não dá para dizer quanto dessa demanda a
  própria Haier captura, nem quanto vaza para marketplace.
- **A ausência de sinal de serviço é sobre a demanda de marca da Haier**, não sobre o tamanho
  do território de serviço na categoria. Esse número continua dependendo do Tier 1.
- **A separação de idioma é heurística**, por padrão de vocabulário, e tem casos de fronteira:
  `haier electronics` e `haier appliances`, por exemplo, são classificadas como estrangeiras
  por conterem termo em inglês, embora possam ser digitadas por brasileiros. O efeito é
  conservador — subestima ligeiramente a Haier — e não altera nenhuma conclusão de ordem de
  grandeza. A regra completa está no script.

---

## O que eu faria a seguir

1. **Dimensionar o território vago**, que é o Tier 1 do pedido de dados: keywords de serviço e
   pós-compra não-branded. Sem isso, "o território está vago" é uma frase; com isso, vira um
   número que a banca não contesta.
2. **Rodar `eliana` isolada como seed** e verificar se há assinatura de campanha. Custo
   marginal, e fecha a única ambiguidade relevante deste documento.
3. **Repetir esta leitura em três meses.** A inclinação da Haier é a variável a monitorar, não
   o nível — e este documento já é a linha de base contra a qual comparar.
