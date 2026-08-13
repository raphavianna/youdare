# Escada de autonomia e guardrails

Toda automação desta cadeira declara seu degrau **antes** de ir ao ar. Autonomia é declarada,
nunca presumida (R8).

## Os cinco degraus

| Degrau | Comportamento | Quando usar |
|---|---|---|
| **N0 Observa** | Coleta e exibe | Sempre o ponto de partida de qualquer rotina nova |
| **N1 Alerta** | Detecta desvio e avisa | Quando o padrão de normalidade já é conhecido |
| **N2 Recomenda** | Propõe a ação com racional e efeito estimado; humano executa | Quando a ação é reversível mas o julgamento ainda não foi validado |
| **N3 Executa com limite** | Age dentro de teto declarado, registra e notifica; reversível | Depois de histórico auditável de acerto em N2 |
| **N4 Executa autônomo** | Opera dentro de guardrails, com revisão periódica agendada | Depois de leitura de N3 mostrando paridade ou ganho, com zero reversões críticas |

**Regra de subida:** um degrau por vez, com leitura entre eles. Nunca saltar de N1 para N4 (D7).

## Guardrails obrigatórios em N3 e N4

1. **Teto por execução** e **teto acumulado por período** — em percentual da verba, declarados
   por escrito.
2. **Nenhuma mudança estrutural sem humano** — canal novo, audiência nova, criativo novo,
   alteração de mensagem ou de posicionamento de marca.
3. **Janela mínima de dado antes de agir** — para não reagir a ruído de fim de semana ou a
   evento isolado.
4. **Reversibilidade** — toda ação registra o estado anterior e reverte em um comando.
5. **Kill switch por cliente.**
6. **Dono humano nomeado.** Automação sem dono não sobe.

## Observabilidade

Todo agente registra, em `50-engenharia/logs/`: o que fez, por que fez, qual era o estado
anterior, e qual efeito estimava. O log é o que permite auditar hoje e aprender depois — e é o
insumo bruto de M4.

## Ficha de registro (preencher antes de subir)

```
Agente:
Prática (P1–P10):
Cliente(s):
Degrau atual:            Degrau anterior:            Data da subida:
Ação que executa:
Teto por execução:       Teto acumulado/período:
Janela mínima de dado:
Como reverter:
Dono humano:
Data da próxima revisão:
```

## O que nunca sobe de degrau

Escolha da pergunta, decisão estrutural de verba, leitura de risco reputacional e o que é dito
ao cliente. Essas quatro permanecem com julgamento humano em qualquer degrau (R8).
