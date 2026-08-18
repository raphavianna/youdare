# Qualidade — base de demanda mediada por IA

Gerado por `20-normalizado/normalizar_ai.py`. Dois datasets: `topicos.csv` e `prompts.csv`.

## Tópicos

- **10198** tópicos únicos em **18** exports · **8468** Brasil · 1730 Estados Unidos
- **3205** tópicos mencionam aparelho e formam a base de categoria — 62% do
  recorte Brasil é vazamento de clustering e fica fora de todo agregado
- Volume da categoria no Brasil: **23,443,233** · prompts declarados: **86,817**
- Sem marca nenhuma no nome: **19,054,264** (81.3% do volume da categoria)

**Teto de 1.000 linhas por export.** Todo arquivo para em 1.000 tópicos. O universo é
censurado por seed: os números acima descrevem *demanda mapeada*, não demanda total. Cada seed
novo alarga o mapa, e nenhum percentual daqui deve ser lido como participação sobre o universo.

**Os seeds de tópico não carregam nome de marca.** São todos termos de categoria
(air_fryers, airfryer, ar_condicionado, aspirador, climatizador, fog_es_e_eletrodom_sticos_de_cozinha, forno, freezer, geladeira, geladeiras_e_refrigeradores_no_brasil, lava_lou_a, liquidificador, m_quinas_de_lavar_roupas, maquina-de-lavar, micro-ondas, microondas-v2). Marca que aparece no nome de um tópico foi
descoberta organicamente — por isso a leitura de cobertura por nome de tópico **não tem viés de
seed** e é a medida primária deste material.

## Prompts

- **4987** pares prompt × provedor únicos, de 3410 prompts distintos
- Provedores: chatgpt, gemini, google_ai_mode, google_ai_overview
- Seeds: brastemp, eletrolux, geladeira, hisense, midea

**Estes têm viés de seed e a contagem de marca sobre eles é enviesada.** Quatro dos seeds são
nomes de marca — brastemp, eletrolux, hisense, midea — e nenhum é Consul,
Samsung ou Haier. Marca com seed próprio aparece mais por construção. Serve para **exemplo de
prompt e leitura de conteúdo**, nunca para ranking de cobertura.

Marcas encontradas no texto das respostas, para registro do viés:
- brastemp: 1026 de 4987 respostas (20.6%)
- midea: 984 de 4987 respostas (19.7%)
- electrolux: 939 de 4987 respostas (18.8%)
- consul: 163 de 4987 respostas (3.3%)
- hisense: 129 de 4987 respostas (2.6%)
- panasonic: 38 de 4987 respostas (0.8%)
- lg: 31 de 4987 respostas (0.6%)
- samsung: 22 de 4987 respostas (0.4%)

## Outras ressalvas

- `mentioned_brands_count` traz a **contagem**, não os nomes. As marcas aqui vêm de busca de
  string no texto da resposta — aproximação declarada, não campo da ferramenta.
- `sources_count` vem zero em ~20% das linhas porque o Google AI Mode não reporta fontes.
  Ausência de dado, não ausência de fonte.
- Os 1730 tópicos dos Estados Unidos ficam fora de todos os agregados do Brasil.
- Tópicos duplicados entre exports são atribuídos ao primeiro arquivo que os traz.
