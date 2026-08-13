---
name: concorrencia
description: Conduz o trabalho de uma concorrência (pitch) de ponta a ponta — leitura de briefing, diagnóstico, território, tese, plano e defesa. Use quando o trabalho for responder a um RFP, um case de concorrência, ou um pitch para cliente novo ou projeto novo em cliente existente.
---

# Máquina de concorrência

Conduz um pitch pelos sete estágios. Antes de qualquer coisa, leia o `CLAUDE.md` da pasta da
concorrência e o `_sumario.md` do `00-briefing/`. Não trabalhe de memória da conversa quando
existe arquivo.

## Os estágios e o que cada um exige

**00 · Briefing.** Material cru do cliente. A saída deste estágio é o `_sumario.md`: fatos
extraídos, com fonte, sem interpretação. Números vindos de extração de slide entram marcados
para conferência. Este estágio termina com a lista de lacunas — o que o cliente disse que
mandaria e ainda não mandou, e o que o briefing não responde.

**10 · Diagnóstico.** Categoria, dados, benchmark, cenário competitivo. Este é o estágio da
P1 e da P2: onde a marca está no funil declarado, qual a pressão da categoria, qual a distância
entre share of voice, share of social e share of market. Toda leitura sai no padrão de insight.

**20 · Território.** Cultura, jornada, audiência, conversa. Consome de P9 e de P4 — o que as
pessoas dizem espontaneamente e o que perguntam à busca. A saída é o mapa de pontos de entrada
de categoria e os territórios vagos. Ver `00-cadeira/metodo/cognitive-mapping.md`.

**30 · Tese.** A resposta em uma frase e o raciocínio que a sustenta. Uma tese declara: por
qual elo da cadeia causal ela age, por que esse elo e não outro, e o que precisaria ser
verdade para ela estar errada. Tese que não pode estar errada não é tese.

**40 · Plano.** Canais, momentos, verba, KPI e regra de otimização, no modelo de
`00-cadeira/metodo/funil-fragmentado.md` — sete campos por momento. Split marca/ativação por
D1, com o benchmark declarado como benchmark. Onde faltar margem ou meta, entregue cenários
com premissa declarada em vez de travar (D8).

**50 · Entrega.** Deck, defesa e anexos. Cada número do deck tem fonte rastreável. Cada
recomendação tem prova declarada.

**99 · Pós-mortem.** Ganhou ou perdeu, e por quê. Alimenta `70-aprendizado` do cliente e o
backlog de M4.

## Regras da prática

- **Responda o que foi perguntado, na ordem em que foi perguntado.** Banca de concorrência lê
  procurando o que pediu. Reorganizar a estrutura do RFP por elegância própria custa ponto.
- **Critério de avaliação declarado é checklist.** Cada critério recebe uma resposta explícita
  e uma prova. Critério sobre dado, AI ou gestão de projeto se responde com método e case
  auditável, não com adjetivo.
- **Lacuna do briefing é oportunidade de defesa.** Briefing sem margem ou sem meta: modele em
  cenários e mostre como a resposta se move em cada um. Isso demonstra método na banca.
- **Nunca invente número de mercado** (R2). Em concorrência, um benchmark sem fonte que a banca
  conhece melhor que você é o jeito mais rápido de perder credibilidade.
- **Feche cada entrega com "o que eu faria a seguir".**
