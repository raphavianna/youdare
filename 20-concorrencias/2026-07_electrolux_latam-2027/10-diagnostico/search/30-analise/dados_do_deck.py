"""
Consolida todos os numeros do material executivo num unico JSON.
Toda cifra do deck sai daqui — nada e digitado a mao no HTML.

Uso: python3 dados_do_deck.py  ->  30-analise/dados_do_deck.json
"""
import csv, json, re, glob, os, statistics as st, collections
from pathlib import Path
import openpyxl, warnings
warnings.filterwarnings("ignore"); csv.field_size_limit(10**7)

B = Path(__file__).resolve().parent.parent
NORM, RAW = B/"20-normalizado", B/"00-raw"

def num(x):
    try: return float(str(x or 0).replace(",",""))
    except: return 0.0

def serie(r):
    try: t = json.loads(r.get("trend") or "null")
    except: return None
    if not t or len(t)!=12 or st.mean(t)==0: return None
    v, m = num(r["volume_medio_12m"]), st.mean(t)
    return [v*x/m for x in t]

# ---------- keywords: players + territorio sem dono ----------
kws = list(csv.DictReader(open(NORM/"keywords.csv", encoding="utf-8")))
lista = {r["keyword"]: r for r in csv.DictReader(open(B/"50-listas"/"lista-cauda-nao-branded.csv", encoding="utf-8"))}
cauda = []
for r in csv.DictReader(open(RAW/"busca-convencional"/"2026-08-17_semrush_keywords_cauda-nao-branded.csv", encoding="utf-8-sig")):
    if num(r.get("Volume")) <= 0: continue
    k = r["Keyword"].strip().lower(); meta = lista.get(k, {})
    if meta.get("familia") == "controle branded": continue
    tr = ""
    if r.get("Trend"):
        try: tr = json.dumps([float(x) for x in str(r["Trend"]).split(",")])
        except: pass
    cauda.append({"keyword": k, "marca_seed": "sem_dono", "volume_medio_12m": str(int(num(r["Volume"]))),
                  "familia": meta.get("familia","?"), "categoria": meta.get("categoria","sem categoria"),
                  "intent": r.get("Intent",""), "trend": tr,
                  "tem_ai_overview": str(int("AI Overview" in (r.get("SERP Features") or "")))})
todos = kws + cauda

DESCOBERTA = {"marca e navegacao"}
ESCOLHA    = {"especificacao produto", "aquisicao e comparacao"}
POSSE      = {"assistencia e reparo","defeito","peca e consumivel","instalacao","garantia","manual e uso",
              "manutencao e cuidado","descarte e sustentab","receita e preparo","assistencia","peca",
              "manutencao","consumo","receita","descarte","consumo e eficiencia","sinonimo"}

PLAYERS = [("electrolux","Electrolux"),("brastemp","Brastemp"),("consul","Consul"),
           ("samsung","Samsung"),("midea","Midea"),("hisense","Hisense"),("haier","Haier")]

base = [sum(x) for x in zip(*[s for r in kws if r["marca_seed"]=="generico" for s in [serie(r)] if s])]

out = {"players": {}, "categoria_heads": {}, "sem_dono": {}, "ai": {}, "meta": {}}

def perfil(rows, chave):
    V = sum(num(r["volume_medio_12m"]) for r in rows)
    fam = collections.Counter()
    for r in rows: fam[r["familia"]] += num(r["volume_medio_12m"])
    cat = collections.Counter()
    for r in rows: cat[r.get("categoria","sem categoria")] += num(r["volume_medio_12m"])
    intent = collections.Counter()
    for r in rows: intent[(r.get("intent") or "-").split(",")[0].strip()] += num(r["volume_medio_12m"])
    aio = sum(num(r["volume_medio_12m"]) for r in rows if r.get("tem_ai_overview")=="1")
    ss = [s for r in rows for s in [serie(r)] if s]
    S = [sum(x) for x in zip(*ss)] if ss else None
    top = sorted(rows, key=lambda r: -num(r["volume_medio_12m"]))[:6]
    d = {"chave": chave, "kw": len(rows), "volume": round(V),
         "descoberta": round(100*sum(fam[f] for f in DESCOBERTA)/V, 1),
         "escolha":    round(100*sum(fam[f] for f in ESCOLHA)/V, 1),
         "posse":      round(100*sum(fam[f] for f in POSSE)/V, 1),
         "nao_class":  round(100*fam.get("nao classificado",0)/V, 1),
         "ai_overview": round(100*aio/V),
         "intent": [[k, round(100*v/V)] for k,v in intent.most_common(3)],
         "familias": {k: round(100*v/V,1) for k,v in fam.most_common() if 100*v/V >= 0.4},
         "categorias": {k: round(100*v/V,1) for k,v in cat.most_common() if 100*v/V >= 0.5},
         "top_keywords": [[r["keyword"], round(num(r["volume_medio_12m"]))] for r in top],
         "serie": [round(x) for x in S] if S else None}
    if S and base:
        rel = [S[i]/base[i] for i in range(12)]
        d["serie_relativa"] = [round(x, 5) for x in rel]
        d["inclinacao_bruta"] = round(st.mean(S[7:])/st.mean(S[:7]), 2)
        d["inclinacao_vs_categoria"] = round(st.mean(rel[7:])/st.mean(rel[:7]), 2)
    return d

for seed, nome in PLAYERS:
    g = [r for r in kws if r["marca_seed"] == seed]
    p = perfil(g, seed); p["nome"] = nome; out["players"][seed] = p
out["categoria_heads"] = perfil([r for r in kws if r["marca_seed"]=="generico"], "generico")
out["categoria_heads"]["nome"] = "Categoria (heads sem marca)"
out["sem_dono"] = perfil(cauda, "sem_dono"); out["sem_dono"]["nome"] = "Território sem dono"

# familias x AI Overview (todas as fontes)
fam_aio = collections.defaultdict(lambda: [0.0, 0.0])
for r in todos:
    v = num(r["volume_medio_12m"]); fam_aio[r["familia"]][0] += v
    if r.get("tem_ai_overview") == "1": fam_aio[r["familia"]][1] += v
out["familias_ai_overview"] = {f: {"volume": round(V), "aio": round(100*A/V)}
                               for f,(V,A) in fam_aio.items() if V >= 3000}
tp = sum(V for f,(V,A) in fam_aio.items() if f in POSSE); ap = sum(A for f,(V,A) in fam_aio.items() if f in POSSE)
to = sum(V for f,(V,A) in fam_aio.items() if f not in POSSE); ao = sum(A for f,(V,A) in fam_aio.items() if f not in POSSE)
out["ai_overview_agregado"] = {"posse": {"volume": round(tp), "aio": round(100*ap/tp)},
                               "demais": {"volume": round(to), "aio": round(100*ao/to)},
                               "electrolux": out["players"]["electrolux"]["ai_overview"]}

# ---------- IA: respostas ----------
R = list(csv.DictReader(open(NORM/"ai_respostas.csv", encoding="utf-8")))
MARCAS = ["Electrolux","Consul","Brastemp","Midea","Samsung"]
PROV = ["All AI Platforms","ChatGPT","Gemini","Google AI Mode","Perplexity"]
def f(x):
    try: return float(str(x).replace("%","").replace(",","."))
    except: return None
cob = {}
for m in MARCAS:
    linha = {}
    for p in PROV:
        sub = [r for r in R if r["marca"]==m and r["provedor"]==p]
        linha[p] = round(100*sum(1 for r in sub if r["citada"]=="1")/len(sub)) if sub else 0
    pos = [v for r in R if r["marca"]==m and r["provedor"]!="All AI Platforms" and (v:=f(r["posicao"])) is not None]
    sen = [v for r in R if r["marca"]==m and r["provedor"]!="All AI Platforms" and (v:=f(r["sentimento"])) is not None]
    cob[m] = {"cobertura": linha, "posicao": round(st.mean(pos),1) if pos else None,
              "sentimento": round(st.mean(sen),1) if sen else None, "n_citacoes": len(pos)}
out["ai"]["marcas"] = cob
famcob = collections.defaultdict(lambda: collections.defaultdict(lambda: [0,0]))
for r in R:
    if r["provedor"] != "All AI Platforms": continue
    famcob[r["familia"]][r["marca"]][0] += (1 if r["citada"]=="1" else 0)
    famcob[r["familia"]][r["marca"]][1] += 1
out["ai"]["cobertura_por_familia"] = {
    fm: {"n": famcob[fm]["Electrolux"][1], **{m: round(100*famcob[fm][m][0]/famcob[fm][m][1]) for m in MARCAS}}
    for fm in famcob if famcob[fm]["Electrolux"][1] >= 3}

# ---------- IA: trafego de LLM ----------
wb = openpyxl.load_workbook(RAW/"ai-search"/"2026-08-17_similarweb_ai-referrals_electrolux-vs-concorrentes.xlsx", data_only=True)
ws = wb["AI_Referrals"]; rr = [r for r in ws.iter_rows(values_only=True) if r and r[0]]
doms = list(rr[0])[2:]; ref = collections.defaultdict(lambda: collections.defaultdict(float))
for r in rr[1:]:
    mes = r[0].strftime("%Y-%m") if hasattr(r[0],"strftime") else str(r[0])
    for i,d in enumerate(doms):
        if isinstance(r[2+i], (int,float)): ref[d][mes] += r[2+i]
wb.close()
meses = sorted({m for d in ref for m in ref[d]})
out["ai"]["referrals"] = {"meses": meses, "series": {d: [round(ref[d].get(m,0)) for m in meses] for d in doms}}

# ---------- IA: topicos ----------
APAR = r"geladeira|refrigerad|freezer|lava.?lou[çc]a|m[aá]quina de lavar|lavadora|lava e seca|secadora|fog[aã]o|cooktop|forno|micro.?ondas|air.?fryer|fritadeira|ar.?condicionado|climatizador|coifa|depurador|adega|purificador|aspirador|eletrodom"
FAMT = [("uso e receita", r"receita|preparo|como usar|modo de"), ("limpeza e manutencao", r"limpeza|limpar|manuten|cuidado|higieniz"),
        ("comparacao e modelo", r"melhor|compar|\bvs\b|modelo|escolher|qual"), ("peca e filtro", r"pe[çc]a|filtro|componente"),
        ("consumo e energia", r"consumo|energia|kwh|economia|pot[êe]ncia"), ("instalacao", r"instala"),
        ("defeito e problema", r"defeito|problema|n[aã]o (gela|liga|seca)|erro"), ("assistencia e conserto", r"conserto|assist|reparo|t[ée]cnic"),
        ("preco e compra", r"pre[çc]o|comprar|oferta|promo|barat|custo")]
uni = {}
for fp in sorted(glob.glob(str(RAW/"ai-search"/"topicos"/"*_br.csv"))):
    for r in csv.DictReader(open(fp, encoding="utf-8")):
        nm = (r.get("name") or "").strip()
        try: v = int(float(r.get("volume") or 0))
        except: v = 0
        if nm and nm not in uni: uni[nm] = v
apar = {k:v for k,v in uni.items() if re.search(APAR, k, re.I)}
T = sum(apar.values()); usados = set()
tops = {}
for nome, pat in FAMT:
    rx = re.compile(pat, re.I); m = {k:v for k,v in apar.items() if rx.search(k) and k not in usados}
    usados |= set(m)
    tops[nome] = {"n": len(m), "volume": sum(m.values()), "pct": round(100*sum(m.values())/T, 1),
                  "maiores": sorted(m.items(), key=lambda i:-i[1])[:4]}
out["ai"]["topicos"] = {"total_topicos": len(apar), "volume_total": T, "familias": tops,
                        "vazamento_pct": round(100*(len(uni)-len(apar))/len(uni))}
out["meta"] = {"kw_total": len(kws), "kw_cauda": len(cauda), "perguntas_ia": 150,
               "prompts_ia": 4000, "meses_referrals": len(meses)}

json.dump(out, open(B/"30-analise"/"dados_do_deck.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK — {len(json.dumps(out))} bytes")
print("players:", list(out["players"]))
print("electrolux:", {k:v for k,v in out["players"]["electrolux"].items() if k in ("volume","descoberta","escolha","posse","inclinacao_vs_categoria","ai_overview")})
print("sem_dono:", {k:v for k,v in out["sem_dono"].items() if k in ("volume","posse","ai_overview")})
print("topicos:", {k:v["pct"] for k,v in out["ai"]["topicos"]["familias"].items()})
