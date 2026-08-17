"""
Normalizacao dos exports de search — Electrolux Brasil.

Unifica os oito arquivos de keyword (schemas divergentes: xlsx com 36 colunas,
csv com 18), reconstroi a serie mensal, marca idioma, familia e categoria de
produto, e gera os datasets canonicos usados por toda a analise downstream.

Tambem normaliza o corpus de IA: prompts por topico e as respostas nao-branded,
estas ultimas convertidas de formato largo (uma coluna por marca) para longo.

Saidas em 20-normalizado/:
  keywords.csv        — 8 arquivos unificados, uma linha por keyword por fonte
  ai_prompts.csv      — 4.000 prompts + 150 perguntas nao-branded
  ai_respostas.csv    — formato longo: pergunta x provedor x marca
  qualidade.md        — relatorio de limpeza

Uso: python3 normalizar.py
"""
import csv, re, json, statistics as st, collections, warnings
from pathlib import Path
import openpyxl
warnings.filterwarnings("ignore")
csv.field_size_limit(10**7)

BASE = Path(__file__).resolve().parent
RAW_KW = BASE.parent / "00-raw" / "busca-convencional"
RAW_AI = BASE.parent / "00-raw" / "ai-search"

ARQUIVOS_KW = {
    "electrolux": ("2026-08-17_semrush_keywords_electrolux-branded.xlsx", "xlsx"),
    "generico":   ("2026-08-17_semrush_keywords_genericas-categoria.xlsx", "xlsx"),
    "brastemp":   ("2026-08-17_semrush_keywords_brastemp.csv", "csv"),
    "consul":     ("2026-08-17_semrush_keywords_consul.csv", "csv"),
    "hisense":    ("2026-08-17_semrush_keywords_hisense.csv", "csv"),
    "midea":      ("2026-08-17_semrush_keywords_midea.csv", "csv"),
    "samsung":    ("2026-08-17_semrush_keywords_samsung.csv", "csv"),
    "haier":      ("2026-08-17_semrush_keywords_haier.csv", "csv"),
}

# ---------------------------------------------------------------- idioma
RX_FR = re.compile(r"\b(lave|linge|refrigerateur|congelateur|frigo|cave a vin|lave vaisselle|t[ée]l[ée]viseur|hublot|sechant|silencieux|noir|gris|americain|multiporte|encastrable|ventile|lumiere|seche)\b", re.I)
RX_ES = re.compile(r"\b(servicio tecnico|aire acondicionado|nevera|lavadora de ropa|precio)\b", re.I)
RX_EN = re.compile(r"\b(washing machine|fridge|refrigerator|refrigerators|fridges|dishwasher|air conditioner|air conditioning|appliances|smart home|group|corp|corporation|electronics|logo|inch|led|company|europe|china|ceo|biomedical|freezer chest|airco|hong|price|review|manual pdf download)\b", re.I)
RX_PT_GUARD = re.compile(r"geladeira|adega|ar condicionado|ar-condicionado|eletrodom|marca|assist|é bom|controle remoto|port[áa]til|btus?|lavadora|lava e seca|fog[aã]o|micro.?ondas|aspirador", re.I)

def idioma(kw):
    k = kw.lower()
    if RX_FR.search(k): return "fr"
    if RX_ES.search(k): return "es"
    if RX_EN.search(k) and not RX_PT_GUARD.search(k): return "en"
    return "pt"

# ------------------------------------------------------------- taxonomia
TAXONOMIA = [
    ("fora de categoria",      r"\b(himss|hbento|sa[uú]de|health|quatenus|quomodo|rationem|suggestis|facultates|insight|login|conferenc|exhibitor)\b"),
    ("assistencia e reparo",   r"\b(assist[eê]ncia|conserto|consertar|reparo|reparar|t[ée]cnic|autorizada|chamado|substituir|trocar a|troca de)\b"),
    ("defeito",                r"\b(n[aã]o (gela|liga|funciona|centrifuga|seca|esquenta)|erro |defeito|barulho|vazando|vazamento|parou de|entupid)\b"),
    ("peca e consumivel",      r"\b(pe[çc]a|filtro|correia|resist[eê]ncia|refil|l[aâ]mpada|g[aá]s refrigerante|reposi[çc]|acess[oó]rio)\b"),
    ("instalacao",             r"\b(instala[çc]|instalar|montar|montagem|medidas do v[aã]o)\b"),
    ("garantia",               r"\b(garantia|cobertura|extens[aã]o de garantia)\b"),
    ("manual e uso",           r"\b(manual|como (usar|limpar|lavar|programar|configurar|ligar|regular|ajustar|higienizar|secar|descongelar|desodorizar)|passo a passo|tutorial)\b"),
    ("manutencao e cuidado",   r"\b(manuten[çc]|cuidad|conserva[çr]|limpeza|higieniz|durabilidade|vida [uú]til|prolongar)\b"),
    ("descarte e sustentab",   r"\b(descart|recicl|sustentab|coleta consciente|log[ií]stica reversa)\b"),
    ("receita e preparo",      r"\b(receita|assar|cozinhar|air.?fryer.*fazer)\b"),
    ("consumo e eficiencia",   r"\b(consumo|consome|gasta|kwh|energia|econ[oô]mic|efici[eê]nc|selo|procel|inmetro|conta de luz)\b"),
    ("conectividade e smart",  r"\b(smart|wi.?fi|conect|aplicativo|intelig[eê]nt|automa[çc])\b"),
    ("frente nomeada",         r"\b(shopclub|shop club|outlet|afiliad|coleta consciente)\b|\b(cuida|projeta|instala)\s+(electrolux|eletrolux)\b|electrolux\s+(pro|cuida|projeta|instala)\b"),
    ("aquisicao e comparacao", r"\b(melhor|melhores|compar|vale a pena|custo.?benef|diferen[çc]a entre|\bvs\b|versus|recomend|escolher|barat|pre[çc]o|quanto custa|onde comprar|comprar|oferta|promo[çc]|desconto|venda|vender)\b"),
    ("especificacao produto",  r"\b(frost free|inverter|lava e seca|lava.?seca|essential care|essencial care|side by side|\d+\s?(kg|litros|btus?|polegadas)|duplex|invertida|top load|front load)\b"),
    ("marca e navegacao",      r"^(electrolux|eletrolux|midea|hisense|haier|brastemp|consul|samsung)([\s\w]{0,25})?$"),
]
FAMILIAS_VIDA = {"assistencia e reparo","defeito","peca e consumivel","instalacao","garantia",
                 "manual e uso","manutencao e cuidado","descarte e sustentab","receita e preparo"}

def familia(texto):
    t = (texto or "").lower()
    for nome, padrao in TAXONOMIA:
        if re.search(padrao, t):
            return nome
    return "nao classificado"

CATEGORIAS = [
    ("geladeira",    r"geladeira|refrigerador|frost free|side by side|duplex|invertida"),
    ("lavanderia",   r"lavadora|m[aá]quina de lavar|lava e seca|lava.?seca|secadora|tanquinho|lava roupa"),
    ("ar condicionado", r"ar.?condicionado|split|btus?|climatiza"),
    ("coccao",       r"fog[aã]o|forno|cooktop|micro.?ondas|coifa|air.?fryer|fritadeira"),
    ("lava loucas",  r"lava.?lou[çc]as"),
    ("aspirador",    r"aspirador|vertical stick|robo aspirador"),
    ("purificador",  r"purificador|bebedouro|filtro de [aá]gua"),
    ("adega",        r"adega|cave a vin|wine"),
    ("freezer",      r"freezer|congelador|congelateur"),
    ("tv e outros",  r"\btv\b|televis|t[ée]l[ée]vis|som|[aá]udio"),
]
def categoria(texto):
    t = (texto or "").lower()
    for nome, padrao in CATEGORIAS:
        if re.search(padrao, t):
            return nome
    return "sem categoria"

# ------------------------------------------------------------- utilidades
def num(v):
    try: return float(str(v).replace(",", "").strip())
    except: return 0.0

def parse_trend(s):
    try:
        v = [float(x) for x in str(s).split(",")]
        return v if len(v) == 12 else None
    except: return None

def volume_corrente(volume, trend):
    """vol_i = Volume * T_i / media(T). Premissa declarada, confianca media."""
    if not trend or st.mean(trend) == 0: return volume
    return volume * trend[-1] / st.mean(trend)

def ler_csv(caminho):
    with open(caminho, encoding="utf-8-sig") as fh:
        return [r for r in csv.DictReader(fh) if (r.get("Keyword") or "").strip()]

def ler_xlsx(caminho, aba="Keywords"):
    wb = openpyxl.load_workbook(caminho, data_only=True)
    linhas = [r for r in wb[aba].iter_rows(values_only=True) if r and r[0]]
    cabecalho = list(linhas[0]); wb.close()
    return [dict(zip(cabecalho, r)) for r in linhas[1:] if str(r[1] or "").strip()]

# ------------------------------------------------------------- keywords
registros, log = [], collections.Counter()
for marca, (arquivo, tipo) in ARQUIVOS_KW.items():
    linhas = ler_xlsx(RAW_KW / arquivo) if tipo == "xlsx" else ler_csv(RAW_KW / arquivo)
    log[f"lidas:{marca}"] = len(linhas)
    for r in linhas:
        kw = str(r.get("Keyword", "")).strip()
        if not kw: continue
        trend = parse_trend(r.get("Trend"))
        vol = num(r.get("Volume"))
        serp = str(r.get("SERP Features") or "")
        registros.append({
            "fonte_arquivo": arquivo,
            "marca_seed": marca,
            "keyword": kw.lower(),
            "idioma": idioma(kw),
            "familia": familia(kw),
            "categoria": categoria(kw),
            "volume_medio_12m": int(vol),
            "volume_corrente_est": round(volume_corrente(vol, trend), 1),
            "kd": num(r.get("Keyword Difficulty")),
            "cpc_usd": num(r.get("CPC (USD)")),
            "densidade_competitiva": num(r.get("Competitive Density")),
            "intent": str(r.get("Intent") or "").strip(),
            "tem_ai_overview": int("AI Overview" in serp),
            "serp_features": serp,
            "click_potential": num(r.get("Click potential")),
            "trend": json.dumps(trend) if trend else "",
        })

# deduplicacao: mesma keyword em mais de um arquivo fica com o de maior volume
por_kw = collections.defaultdict(list)
for r in registros: por_kw[r["keyword"]].append(r)
dedup = []
for kw, grupo in por_kw.items():
    principal = max(grupo, key=lambda r: r["volume_medio_12m"])
    principal = dict(principal)
    principal["n_fontes"] = len(grupo)
    principal["fontes"] = "|".join(sorted({g["marca_seed"] for g in grupo}))
    dedup.append(principal)
log["keywords_brutas"] = len(registros)
log["keywords_unicas"] = len(dedup)
log["removidas_dedup"] = len(registros) - len(dedup)
log["idioma_estrangeiro"] = sum(1 for r in dedup if r["idioma"] != "pt")
log["fora_de_categoria"] = sum(1 for r in dedup if r["familia"] == "fora de categoria")

limpo = [r for r in dedup if r["idioma"] == "pt" and r["familia"] != "fora de categoria"]
log["keywords_limpas"] = len(limpo)

campos = list(limpo[0].keys())
with open(BASE / "keywords.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=campos); w.writeheader(); w.writerows(sorted(limpo, key=lambda r: -r["volume_medio_12m"]))

# ------------------------------------------------------------- prompts de IA
prompts = []
for topico in ["eletrolux", "geladeira", "hisense", "midea"]:
    for r in csv.DictReader(open(RAW_AI / f"2026-08-17_ai-prompts_topico-{topico}.csv", encoding="utf-8")):
        p = (r.get("prompt") or "").strip()
        if not p: continue
        prompts.append({
            "fonte": f"prompts_topico_{topico}", "topico": topico, "texto": p,
            "llm": r.get("llm", ""), "familia": familia(p), "categoria": categoria(p),
            "marcas_mencionadas": r.get("mentioned_brands_count", ""),
            "n_fontes_citadas": r.get("sources_count", ""),
            "relevancia": r.get("relevance_score", ""),
        })
log["prompts_brutos"] = len(prompts)
log["prompts_fora_categoria"] = sum(1 for p in prompts if p["familia"] == "fora de categoria")

perguntas_nb = sorted({r["Question"] for r in csv.DictReader(open(RAW_AI / "2026-08-14_semrush_ai-answers_non-branded-brasil.csv", encoding="utf-8")) if (r.get("Question") or "").strip()})
for q in perguntas_nb:
    prompts.append({"fonte": "ai_answers_nao_branded", "topico": "nao-branded", "texto": q,
                    "llm": "", "familia": familia(q), "categoria": categoria(q),
                    "marcas_mencionadas": "", "n_fontes_citadas": "", "relevancia": ""})
log["perguntas_nao_branded"] = len(perguntas_nb)

prompts_limpos = [p for p in prompts if p["familia"] != "fora de categoria"]
log["prompts_limpos"] = len(prompts_limpos)
with open(BASE / "ai_prompts.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(prompts_limpos[0].keys())); w.writeheader(); w.writerows(prompts_limpos)

# --------------------------------------------- respostas de IA: largo -> longo
linhas_nb = list(csv.DictReader(open(RAW_AI / "2026-08-14_semrush_ai-answers_non-branded-brasil.csv", encoding="utf-8")))
MARCAS = ["Electrolux (brazil official online store)", "Consul", "Brastemp", "Midea", "Samsung"]
longo = []
for r in linhas_nb:
    if not (r.get("Question") or "").strip(): continue
    for marca in MARCAS:
        pos = (r.get(f"{marca} (position)") or "").strip()
        sen = (r.get(f"{marca} (sentiment score)") or "").strip()
        longo.append({
            "pergunta": r["Question"], "provedor": r.get("Provider", ""),
            "marca": "Electrolux" if marca.startswith("Electrolux") else marca,
            "posicao": "" if pos in ("-", "") else pos,
            "posicao_diff": (r.get(f"{marca} (position diff)") or "").replace("-", "") if (r.get(f"{marca} (position diff)") or "").strip() != "-" else "",
            "sentimento": "" if sen in ("-", "") else sen,
            "citada": int(pos not in ("-", "")),
            "familia": familia(r["Question"]), "categoria": categoria(r["Question"]),
        })
log["ai_respostas_linhas_longo"] = len(longo)
with open(BASE / "ai_respostas.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(longo[0].keys())); w.writeheader(); w.writerows(longo)

# ------------------------------------------------------------- relatorio
with open(BASE / "qualidade.md", "w", encoding="utf-8") as fh:
    fh.write("# Relatório de limpeza — gerado por `normalizar.py`\n\n")
    fh.write("| Etapa | n |\n|---|---:|\n")
    for k, v in log.items():
        fh.write(f"| {k.replace('_',' ')} | {v:,} |\n")
    fh.write("\n## Regras aplicadas\n\n")
    fh.write("1. **Deduplicação por keyword.** Mesma keyword em mais de um arquivo fica com o registro de maior volume; a origem completa é preservada na coluna `fontes`.\n")
    fh.write("2. **Filtro de idioma.** Queries em francês, inglês e espanhol capturadas na base `br` são removidas do dataset limpo. A classificação é heurística por vocabulário e conservadora.\n")
    fh.write("3. **Filtro de categoria.** Prompts sobre saúde, conferências e conteúdo em latim presentes nos arquivos `prompts_by_topic` são removidos.\n")
    fh.write("4. **Reconstrução de volume corrente.** `vol_i = Volume × T_i / média(T)`, sob a premissa de que `Trend` é o índice mensal normalizado pelo pico. Premissa declarada, confiança média.\n")
    fh.write("5. **Respostas de IA convertidas de formato largo para longo** — uma linha por pergunta × provedor × marca.\n")
    fh.write("\n## Limites conhecidos\n\n")
    fh.write("- As colunas `Competitors` / `Competitor on TOP 10` e `Content references` estão **vazias em todos os oito arquivos**. Não é possível saber quem ocupa o top 10 de cada keyword.\n")
    fh.write("- A linha `Provider = All AI Platforms` é agregado dos demais provedores e não deve ser somada com eles.\n")
    fh.write("- A cobertura da taxonomia é parcial; `nao classificado` é uma categoria legítima e aparece no dataset.\n")

print(open(BASE / "qualidade.md", encoding="utf-8").read())
