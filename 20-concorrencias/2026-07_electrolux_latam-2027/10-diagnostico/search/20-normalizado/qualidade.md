# Relatório de limpeza — gerado por `normalizar.py`

| Etapa | n |
|---|---:|
| lidas:electrolux | 904 |
| lidas:generico | 65 |
| lidas:brastemp | 2,000 |
| lidas:consul | 1,082 |
| lidas:hisense | 500 |
| lidas:midea | 101 |
| lidas:samsung | 300 |
| lidas:haier | 100 |
| keywords brutas | 5,052 |
| keywords unicas | 5,041 |
| removidas dedup | 11 |
| idioma estrangeiro | 76 |
| fora de categoria | 0 |
| keywords limpas | 4,965 |
| prompts brutos | 4,000 |
| prompts fora categoria | 105 |
| perguntas nao branded | 150 |
| prompts limpos | 4,045 |
| ai respostas linhas longo | 3,745 |

## Regras aplicadas

1. **Deduplicação por keyword.** Mesma keyword em mais de um arquivo fica com o registro de maior volume; a origem completa é preservada na coluna `fontes`.
2. **Filtro de idioma.** Queries em francês, inglês e espanhol capturadas na base `br` são removidas do dataset limpo. A classificação é heurística por vocabulário e conservadora.
3. **Filtro de categoria.** Prompts sobre saúde, conferências e conteúdo em latim presentes nos arquivos `prompts_by_topic` são removidos.
4. **Reconstrução de volume corrente.** `vol_i = Volume × T_i / média(T)`, sob a premissa de que `Trend` é o índice mensal normalizado pelo pico. Premissa declarada, confiança média.
5. **Respostas de IA convertidas de formato largo para longo** — uma linha por pergunta × provedor × marca.

## Limites conhecidos

- As colunas `Competitors` / `Competitor on TOP 10` e `Content references` estão **vazias em todos os oito arquivos**. Não é possível saber quem ocupa o top 10 de cada keyword.
- A linha `Provider = All AI Platforms` é agregado dos demais provedores e não deve ser somada com eles.
- A cobertura da taxonomia é parcial; `nao classificado` é uma categoria legítima e aparece no dataset.
