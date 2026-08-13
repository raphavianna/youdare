# Nomenclatura

## Arquivos

```
AAAA-MM-DD_<origem>_<tipo>_<descricao-em-kebab-case>.<ext>
```

- **origem** — de quem veio: `electrolux`, `youdare`, `kantar`, `meta`.
- **tipo** — o que é: `briefing`, `case`, `plano`, `report`, `tese`, `dado`, `deck`, `ata`,
  `analise`, `modelo`.
- **descricao** — em kebab-case, sem acento, específica o bastante para o arquivo ser
  encontrado sem abrir.

Exemplos:
```
2026-07-31_electrolux_briefing_deck-agencias.pdf
2026-09-20_youdare_deck_proposta-latam-2027.pptx
2026-08-15_youdare_analise_share-of-social-lavanderia-co.md
```

## Pastas

- **Cliente:** `10-clientes/<cliente-em-kebab-case>/`
- **Concorrência:** `20-concorrencias/AAAA-MM_<cliente>_<projeto>/` — o ano-mês é o do início
  do processo, não o da entrega.
- **Estágios:** prefixo numérico de dois dígitos, com saltos de dez, para permitir inserção
  posterior sem renumerar tudo.

## Versionamento

Não use `v1`, `v2`, `final`, `final-real` no nome do arquivo. O git é o versionamento. Quando
uma versão precisar ser preservada como marco (por exemplo, o que foi efetivamente enviado ao
cliente), mova a cópia para `90-arquivo/` com a data do envio no nome.

## Idioma

Nomes de arquivo e de pasta em português sem acento, em kebab-case. Termos técnicos de mídia
em inglês onde é padrão de mercado (`brand-lift`, `share-of-voice`, `retail-media`).
