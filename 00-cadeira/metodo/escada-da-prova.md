# Escada da prova

Quatro degraus. Quanto mais alto, mais caro e mais lento — e mais defensável. A pergunta não é
"qual é o melhor", é "qual degrau esta decisão exige".

| Degrau | O que é | Custo e prazo | Serve para | Não serve para |
|---|---|---|---|---|
| 1 · Correlação | Duas séries se movem juntas | Baixo, imediato | Levantar hipótese | Decidir verba |
| 2 · Atribuição | Plataforma credita a conversão a si dentro de uma janela | Baixo, diário | Operar o dia a dia, comparar criativos dentro do mesmo canal | Comparar canais, provar valor |
| 3 · Teste incremental | Grupo exposto vs controle: holdout, geo-lift, conversion lift, brand lift | Médio, semanas | Provar causa em escopo estreito; calibrar o degrau 4 | Ler efeito de longo prazo e interação entre canais |
| 4 · Modelagem (MMM) | Econometria sobre séries agregadas | Alto, ciclos | Alocação entre todos os canais numa moeda só; offline, preço, distribuição, sazonalidade | Granularidade de audiência e criativo |

## Regras de uso

- **Nunca chame degrau 2 de degrau 3.** Atribuição é auto-relatada e enviesada a favor de quem
  reporta. Chamar isso de incrementalidade é o erro mais caro da disciplina.
- **O degrau 3 calibra o 4.** Experimentos corrigem o viés de especificação do MMM; MMM sem
  calibragem experimental é um modelo bem ajustado a um passado que pode estar errado.
- **O degrau 4 orienta o 2.** A alocação sai do MMM, a operação diária roda na atribuição.
- **Divergência é informação.** Quando o atribuído é muito maior que o incremental, o canal
  provavelmente captura demanda em vez de criar.

## Como escolher o degrau

| A decisão é... | Degrau mínimo |
|---|---|
| Trocar criativo, ajustar bid, realocar dentro do mesmo canal | 2 |
| Aumentar ou cortar verba de um canal | 3 |
| Redesenhar o mix entre práticas | 4, calibrado por 3 |
| Defender o valor do marketing para o board | 4 + 3 |
