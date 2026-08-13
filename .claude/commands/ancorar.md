---
description: Classifica os arquivos do _inbox no estágio correto do pipeline e registra no manifesto
---

Ancore os arquivos que estão no `_inbox/` da pasta de trabalho atual.

Para cada arquivo, nesta ordem:

1. **Leia o suficiente para classificar.** Não classifique por nome de arquivo — nome mente.
   Em PDF, extraia o texto; em planilha, leia cabeçalho e primeiras linhas; em deck, leia os
   títulos de seção.

2. **Escolha o estágio** conforme a definição da pasta:
   - `00-briefing/` — o que o cliente entregou, cru, sem interpretação da agência.
   - `10-diagnostico/` — categoria, dados, benchmark, cenário competitivo.
   - `20-territorio/` — cultura, jornada, audiência, conversa.
   - `30-tese/` — a tese de mídia e dados que sustenta a resposta.
   - `40-plano/` — canais, funil, verba, KPI, regra de otimização.
   - `50-entrega/` — deck, defesa, anexos enviados ao cliente.
   - `99-pos-mortem/` — resultado e aprendizado.

   Em pasta de cliente, use os estágios daquele `CLAUDE.md`.

3. **Renomeie** para `AAAA-MM-DD_<origem>_<tipo>_<descricao-kebab>.<ext>`, conforme
   `00-cadeira/padroes/nomenclatura.md`. A data é a do documento quando houver metadado
   confiável; caso contrário, a de recebimento.

4. **Registre no `_manifesto.md`** da pasta: data de recebimento, nome original, estágio,
   nome ancorado e o motivo da classificação. Crie o manifesto se não existir.

5. **Pergunte quando o estágio não for óbvio** (R7). Não adivinhe. Diga qual informação
   resolveria a dúvida — normalmente é o período do dado, a origem ou o uso pretendido.

Ao terminar, liste o que foi ancorado, o que ficou pendente de decisão, e as lacunas de
material que a leitura revelou.
