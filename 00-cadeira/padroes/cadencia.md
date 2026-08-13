# Cadência operacional

| Ritmo | O que roda | Práticas | Saída |
|---|---|---|---|
| **Diária** | Pacing, detecção de anomalia, saúde de pipeline | P6, P7, P10 | Alerta, não relatório |
| **Semanal** | Otimização, leitura de teste em andamento, revisão de log de agentes, escuta social e temas emergentes | P4, P6, P7, P9, P10 | Ajuste executado + registro |
| **Mensal** | Report com insight, replanejamento tático, leitura de BHT quando houver onda | P1, todas | Report no padrão de insight |
| **Trimestral** | Prova de incrementalidade, recalibragem de MMM contra experimentos, revisão de alocação, triângulo de share | P1, P2, P9 | Recomendação de realocação |
| **Anual** | Território e cultura, estrutura de dado, roadmap de produto, revisão da tese | M1, M4, P3, P10 | Tese e roadmap |

## Regras de cadência

- **Alerta não é report.** O diário existe para agir, não para informar. Se um alerta diário
  vira slide, a cadência está errada.
- **Trimestre é o menor ciclo em que incrementalidade se prova.** Pedidos de prova causal em
  janela mensal recebem a leitura possível e a lacuna declarada.
- **O triângulo de share exige a mesma janela e o mesmo conjunto competitivo nas três medidas.**
- **Revisão de log de agentes é semanal e inegociável** enquanto houver automação em N3 ou N4.
