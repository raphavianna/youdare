# Triangulação de medição

Nenhuma lente decide sozinha. As três se corrigem.

```
        EXPERIMENTO
     (causal, estreito)
       /           \
      /  calibra    \  corrige viés
     /               \
   MMM  ----------  ATRIBUIÇÃO
(alocação,          (operação,
 agregado)           granular)
```

## O papel de cada lente

- **Experimento** — holdout, geo-lift, conversion lift, brand lift. Prova causal forte em
  janela curta e escopo estreito. Caro em custo de oportunidade: exige suspender ou reter
  investimento em algum lugar.
- **MMM** — a única lente que compara todos os canais na mesma moeda e a única que enxerga
  offline, preço, distribuição, sazonalidade e fatores externos. Entrega separação entre venda
  base e incremental, curva de saturação por canal e efeito de arrasto (adstock e meia-vida).
  Fraca em granularidade e sensível à especificação. Ferramentas abertas de referência: Google
  Meridian e Meta Robyn, além de fornecedores contratados.
- **Atribuição** — granular, rápida, barata, auto-relatada e enviesada. Opera o dia a dia.

## Hierarquia para decisão de verba

Quando as três divergirem: **experimento > MMM > atribuição**.

A divergência em si é diagnóstico. Padrões recorrentes:

| Padrão | Leitura mais provável |
|---|---|
| Atribuído >> incremental | O canal captura demanda criada em outro lugar |
| Incremental >> atribuído | O canal cria demanda que outro canal colhe (típico de marca e de vídeo) |
| MMM aponta saturação, atribuição segue bem | ROI médio bom, ROI marginal ruim (D6) |
| Brand lift positivo, venda estável | O efeito está no elo de marca e ainda não chegou ao comportamento; olhe horizonte |

## Cadência de calibragem

Trimestral: recalibrar o MMM contra os experimentos rodados no período. Anual: revisar
especificação do modelo e o conjunto de variáveis externas.

## Lacunas a preencher por cliente
`[a confirmar: fornecedor de MMM, existência de BHT em onda ou contínuo, e histórico de
experimentos por cliente — registrar em 00-cadeira/stack/inventario-de-fontes.md]`
