"""
Normaliza as duas bases de demanda mediada por IA num par de CSVs auditaveis.

  topicos.csv  — um topico unico por linha (nome, volume, prompts, intent, familia,
                 marcas citadas no nome, pais)
  prompts.csv  — um par prompt x provedor por linha, com as marcas encontradas no
                 texto da resposta

Regra de cobertura desta base: so entram em `topicos/` os exports semeados com
termos de CATEGORIA. Marca que aparece no nome de um topico ali foi descoberta
organicamente, e a leitura de cobertura nao tem vies de seed.

Exports semeados com nome de marca vivem em `topicos-seed-branded/` e ficam FORA
de todo agregado de cobertura. Motivo medido: o seed `consul` devolveu 1.000
topicos cujo topo e "Concursos Publicos Brasil", "Consorcios no Brasil" e
"Portuguese Word Variants" — a ferramenta leu a raiz "consul". Dos 1.000, 114
carregam o nome da marca e somam 706.994 de volume; inclui-los inflaria a
cobertura da Consul em quase 4x, so por ela ter sido semeada.

Os exports de prompt tambem sao semeados por marca; qualquer contagem sobre eles
herda esse vies e e marcada.

Uso: python3 normalizar_ai.py  ->  20-normalizado/topicos.csv, prompts.csv, qualidade_ai.md
"""
import csv, re, glob, os, collections
from pathlib import Path
csv.field_size_limit(10**7)

B = Path(__file__).resolve().parent.parent
RAW, OUT = B/"00-raw"/"ai-search", B/"20-normalizado"

def num(x):
    try: return int(float(str(x or 0).replace(",", "")))
    except: return 0

# ---------------------------------------------------------------- vocabulario
# aparelho mencionado: separa o que e categoria do vazamento de clustering
RX_APARELHO = re.compile(
    r"geladeira|refrigerad|freezer|frigobar|lava.?lou[çc]a|m[aá]quina de lavar|lavadora|"
    r"lava.?e.?seca|secadora|fog[aã]o|cooktop|forno|micro.?ondas|air.?fryer|fritadeira|"
    r"ar.?condicionado|climatizador|coifa|depurador|adega|purificador|aspirador|"
    r"liquidificad|eletrodom|cafeteira|batedeira|ferro de passar|ventilador|"
    r"processador de alimentos|panela el[ée]trica", re.I)

# conjunto competitivo declarado + o entorno que a IA cita junto
MARCAS = [
    ("electrolux", r"electrolux|eletrolux"), ("brastemp", r"brastemp"), ("consul", r"consul"),
    ("samsung", r"samsung"), ("midea", r"midea"), ("hisense", r"hisense"), ("haier", r"haier"),
    ("lg", r"\bLG\b"), ("philco", r"philco"), ("mondial", r"mondial"), ("britania", r"brit[âa]nia"),
    ("panasonic", r"panasonic"), ("continental", r"continental"), ("esmaltec", r"esmaltec"),
    ("atlas", r"\batlas\b"), ("fischer", r"fischer"), ("mueller", r"m[uü]eller"),
    ("tramontina", r"tramontina"), ("arno", r"\barno\b"), ("oster", r"\boster\b"),
    ("whirlpool", r"whirlpool"), ("gree", r"\bgree\b"), ("tcl", r"\bTCL\b"), ("elgin", r"elgin"),
]
RX_MARCAS = [(m, re.compile(rx, re.I)) for m, rx in MARCAS]
NUCLEO = {"electrolux", "brastemp", "consul", "samsung", "midea", "hisense", "haier"}

# familia = a necessidade que o topico expressa. Mesma gramatica do deck de busca:
# classifica pela necessidade, nunca pelo nome comercial de um servico.
FAMILIAS = [
    ("assistencia e conserto", r"assist[êe]ncia|conserto|consertar|t[ée]cnic|reparo|autorizad|manuten[çc][aã]o corretiva"),
    ("defeito e problema",     r"defeito|problema|n[aã]o (gela|liga|seca|funciona|esquenta|centrifuga)|erro\b|c[oó]digo de erro|barulho|vazand|vazamento|piscand|parou de"),
    ("peca e filtro",          r"pe[çc]a|filtro|componente|borracha|correia|resist[êe]ncia|termostato|compressor|g[aá]s refrigerante|cesto|prateleira"),
    ("instalacao",             r"instala|instalar"),
    ("manutencao e limpeza",   r"limpe|limpar|manuten|cuidado|higieniz|degel|descong|desentup|conserva[çc]"),
    ("uso e receita",          r"receita|preparo|como usar|modo de|dicas de uso|assar|fritar|tempo de|temperatura para"),
    # Especificacao vem ANTES de consumo: quem procura "9000 BTU inverter" esta
    # escolhendo o aparelho, nao medindo a conta de luz. `inverter` e `split` sao
    # tecnologia de produto, e capacidade em BTU, litros ou kg e atributo de compra.
    ("especificacao de produto", r"\d[\d\.\s]*btus?\b|\binvert(er)?\b|\bsplit\b|wind.?free|multi.?split|"
                                 r"\d[\d\.]*\s*(litros?|kg)\b|frost.?free|\binox\b|duplex|side.?by.?side|"
                                 r"french.?door|\b(110|127|220)v?\b|bivolt|\d+\s*(bocas|portas)\b|"
                                 r"\bcapacidade\b|\bpolegadas\b"),
    ("consumo e energia",      r"consumo|kwh|energia|economia de|selo|procel|inmetro|gasta|quanto custa para"),
    ("garantia e suporte",     r"garantia|suporte|manual|atendimento|sac\b|reclama"),
    ("preco e compra",         r"pre[çc]o|comprar|oferta|promo[çc]|barat|custo|desconto|black friday|parcel|frete"),
    ("comparacao e modelo",    r"melhor|compar|\bvs\b|modelo|escolher|qual\b|review|avalia|ranking|vale a pena|diferen[çc]a entre"),
    ("marca e loja",           r"loja|onde comprar|site oficial|revendedor|outlet|magazine|casas bahia|mercado livre"),
]
RX_FAMILIAS = [(f, re.compile(p, re.I)) for f, p in FAMILIAS]
# familias que descrevem vida com o produto — o eixo de posse do material
POSSE = {"assistencia e conserto", "defeito e problema", "peca e filtro", "instalacao",
         "manutencao e limpeza", "uso e receita", "garantia e suporte"}

CATEGORIAS = [
    ("geladeira", r"geladeira|refrigerad|frigobar"), ("lavanderia", r"m[aá]quina de lavar|lavadora|lava.?e.?seca|secadora|roupa"),
    ("ar condicionado", r"ar.?condicionado|climatizador|split|\bbtus?\b"), ("coccao", r"fog[aã]o|cooktop|forno(?!.*micro)|coifa|depurador"),
    ("air fryer", r"air.?fryer|fritadeira"), ("micro-ondas", r"micro.?ondas"), ("lava-loucas", r"lava.?lou[çc]a"),
    ("freezer", r"freezer"), ("aspirador", r"aspirador"), ("liquidificador", r"liquidificad"),
    ("adega", r"adega"), ("purificador", r"purificador"),
]
RX_CATEGORIAS = [(c, re.compile(p, re.I)) for c, p in CATEGORIAS]

def primeiro(rx_lista, texto, default="nao classificado"):
    for nome, rx in rx_lista:
        if rx.search(texto or ""): return nome
    return default

# ESTAGIO: a jornada nesta base sai de duas leituras cruzadas — a familia diz qual
# necessidade o topico expressa, o intent da ferramenta diz com que disposicao ela e
# expressa. Nenhuma das duas resolve sozinha: `informational` cobre tanto "qual a
# melhor geladeira" quanto "como limpar a geladeira", e a familia nao distingue quem
# pesquisa para comprar de quem pesquisa para usar.
DESCOBERTA = {"marca e loja"}
ESCOLHA    = {"comparacao e modelo", "preco e compra", "especificacao de produto"}
# Consumo e energia e a unica familia genuinamente transversal: "quanto gasta"
# tanto compara aparelhos antes da compra quanto explica a conta de quem ja tem.
# Ela nao entra em posse por definicao — o intent decide.
AMBIGUAS  = {"consumo e energia"}

def estagio(familia, it):
    if familia in AMBIGUAS:
        return "escolha" if it.get("commercial", 0) + it.get("transactional", 0) >= 0.35 else "posse"
    if familia in POSSE: return "posse"
    if familia in ESCOLHA: return "escolha"
    if familia in DESCOBERTA: return "descoberta"
    if it.get("navigational", 0) >= 0.25: return "descoberta"
    if it.get("commercial", 0) + it.get("transactional", 0) >= 0.45: return "escolha"
    return "exploracao de categoria"

def marcas_em(texto):
    return [m for m, rx in RX_MARCAS if rx.search(texto or "")]

def intents(campo):
    """`task:2;informational:43;...` -> dict normalizado em fracao"""
    d = {}
    for parte in (campo or "").split(";"):
        if ":" in parte:
            k, v = parte.split(":", 1)
            try: d[k.strip()] = float(v)
            except: pass
    t = sum(d.values()) or 1
    return {k: v/t for k, v in d.items()}

# ---------------------------------------------------------------- topicos
vistos, linhas = {}, []
por_arquivo = collections.Counter()
for fp in sorted(glob.glob(str(RAW/"topicos"/"*.csv"))):
    base = os.path.basename(fp)
    pais = "us" if base.endswith("_us.csv") else "br"
    # o seed vive no nome do arquivo; nenhum deles carrega nome de marca
    seed = re.sub(r"^\d{4}-\d{2}-\d{2}_ai-topicos_|_(br|us)\.csv$", "", base)
    for r in csv.DictReader(open(fp, encoding="utf-8-sig")):
        nome = (r.get("name") or "").strip()
        if not nome or nome in vistos: continue
        vistos[nome] = True
        por_arquivo[base] += 1
        it = intents(r.get("intents"))
        mk = marcas_em(nome)
        linhas.append({
            "topico": nome, "pais": pais, "seed": seed,
            "volume": num(r.get("volume")), "prompts": num(r.get("prompts_count")),
            "eh_categoria": int(bool(RX_APARELHO.search(nome))),
            "familia": primeiro(RX_FAMILIAS, nome, "produto e categoria"),
            "estagio": estagio(primeiro(RX_FAMILIAS, nome, "produto e categoria"), it),
            "categoria": primeiro(RX_CATEGORIAS, nome, "sem categoria"),
            "marcas": "|".join(mk),
            "marcas_nucleo": "|".join([m for m in mk if m in NUCLEO]),
            "eh_branded": int(bool(mk)),
            "trend": ";".join(str(x) for x in (r.get("volume_trend") or "").split(";")),
            **{f"int_{k}": round(it.get(k, 0), 4) for k in
               ("informational", "commercial", "transactional", "navigational", "task")},
        })

with open(OUT/"topicos.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)

# ---------------------------------------------------------------- prompts
pares = {}
for fp in sorted(glob.glob(str(RAW/"2026-*_ai-prompts_topico-*.csv"))):
    seed = re.sub(r"^.*_topico-|\.csv$", "", os.path.basename(fp))
    for r in csv.DictReader(open(fp, encoding="utf-8-sig")):
        p, llm = (r.get("prompt") or "").strip(), (r.get("llm") or "").strip()
        if not p or not llm: continue
        resp = r.get("brief_response") or ""
        ch = (p, llm)
        if ch in pares:                       # mesmo par vindo de dois seeds
            pares[ch]["seeds"].add(seed); continue
        pares[ch] = {
            "prompt": p, "provedor": llm, "seeds": {seed},
            "familia": primeiro(RX_FAMILIAS, p, "produto e categoria"),
            "categoria": primeiro(RX_CATEGORIAS, p, "sem categoria"),
            "eh_categoria": int(bool(RX_APARELHO.search(p))),
            "marcas_no_prompt": "|".join(marcas_em(p)),
            "marcas_na_resposta": "|".join(marcas_em(resp)),
            "n_marcas_declarado": num(r.get("mentioned_brands_count")),
            "n_fontes": num(r.get("sources_count")),
            "relevancia": num(r.get("relevance_score")),
            "tam_resposta": len(resp),
        }
prom = []
for v in pares.values():
    v["seeds"] = "|".join(sorted(v.pop("seeds")))
    prom.append(v)
with open(OUT/"prompts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(prom[0].keys())); w.writeheader(); w.writerows(prom)

# ---------------------------------------------------------------- qualidade
br  = [l for l in linhas if l["pais"] == "br"]
cat = [l for l in br if l["eh_categoria"]]
vol = sum(l["volume"] for l in cat)
sem = sum(l["volume"] for l in cat if not l["eh_branded"])
seeds_marca = sorted({s for p in prom for s in p["seeds"].split("|")})
com = collections.Counter()
for p in prom:
    for m in p["marcas_na_resposta"].split("|"):
        if m: com[m] += 1

with open(OUT/"qualidade_ai.md", "w", encoding="utf-8") as f:
    f.write(f"""# Qualidade — base de demanda mediada por IA

Gerado por `20-normalizado/normalizar_ai.py`. Dois datasets: `topicos.csv` e `prompts.csv`.

## Tópicos

- **{len(linhas)}** tópicos únicos em **{len(por_arquivo)}** exports · **{len(br)}** Brasil · {len(linhas)-len(br)} Estados Unidos
- **{len(cat)}** tópicos mencionam aparelho e formam a base de categoria — {100*(len(br)-len(cat))/len(br):.0f}% do
  recorte Brasil é vazamento de clustering e fica fora de todo agregado
- Volume da categoria no Brasil: **{vol:,}** · prompts declarados: **{sum(l['prompts'] for l in cat):,}**
- Sem marca nenhuma no nome: **{sem:,}** ({100*sem/vol:.1f}% do volume da categoria)

**Teto de 1.000 linhas por export.** Todo arquivo para em 1.000 tópicos. O universo é
censurado por seed: os números acima descrevem *demanda mapeada*, não demanda total. Cada seed
novo alarga o mapa, e nenhum percentual daqui deve ser lido como participação sobre o universo.

**Os seeds de tópico não carregam nome de marca.** São todos termos de categoria
({", ".join(sorted({l['seed'] for l in linhas}))}). Marca que aparece no nome de um tópico foi
descoberta organicamente — por isso a leitura de cobertura por nome de tópico **não tem viés de
seed** e é a medida primária deste material.

## Prompts

- **{len(prom)}** pares prompt × provedor únicos, de {len({p['prompt'] for p in prom})} prompts distintos
- Provedores: {", ".join(sorted({p['provedor'] for p in prom}))}
- Seeds: {", ".join(seeds_marca)}

**Estes têm viés de seed e a contagem de marca sobre eles é enviesada.** Quatro dos seeds são
nomes de marca — {", ".join(s for s in seeds_marca if s != "geladeira")} — e nenhum é Consul,
Samsung ou Haier. Marca com seed próprio aparece mais por construção. Serve para **exemplo de
prompt e leitura de conteúdo**, nunca para ranking de cobertura.

Marcas encontradas no texto das respostas, para registro do viés:
{chr(10).join(f"- {m}: {c} de {len(prom)} respostas ({100*c/len(prom):.1f}%)" for m, c in com.most_common(8))}

## Outras ressalvas

- `mentioned_brands_count` traz a **contagem**, não os nomes. As marcas aqui vêm de busca de
  string no texto da resposta — aproximação declarada, não campo da ferramenta.
- `sources_count` vem zero em ~20% das linhas porque o Google AI Mode não reporta fontes.
  Ausência de dado, não ausência de fonte.
- Os {len(linhas)-len(br)} tópicos dos Estados Unidos ficam fora de todos os agregados do Brasil.
- Tópicos duplicados entre exports são atribuídos ao primeiro arquivo que os traz.
""")

print(f"topicos.csv  {len(linhas)} linhas ({len(br)} br, {len(cat)} de categoria)")
print(f"prompts.csv  {len(prom)} pares")
print(f"volume categoria br {vol:,} · sem marca {100*sem/vol:.1f}%")
