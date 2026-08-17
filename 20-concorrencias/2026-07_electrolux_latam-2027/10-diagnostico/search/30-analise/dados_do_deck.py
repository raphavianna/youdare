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
    # exemplos deste recorte, por familia — para que o chip de um slide de marca
    # nunca mostre consulta de outra marca
    ef = collections.defaultdict(list)
    for r in rows: ef[r["familia"]].append([r["keyword"], round(num(r["volume_medio_12m"]))])
    d["exemplos_familia"] = {f: sorted(v, key=lambda i: -i[1])[:3] for f, v in ef.items()}
    # as consultas reais que mais pesam em cada estagio, para nao falar de estagio no abstrato
    d["top_estagio"] = {}
    for est, fams in (("descoberta",DESCOBERTA),("escolha",ESCOLHA),("posse",POSSE)):
        sel = sorted([r for r in rows if r["familia"] in fams], key=lambda r: -num(r["volume_medio_12m"]))[:4]
        d["top_estagio"][est] = [[r["keyword"], round(num(r["volume_medio_12m"])), r["familia"]] for r in sel]
    if S and base:
        rel = [S[i]/base[i] for i in range(12)]
        d["serie_relativa"] = [round(x, 5) for x in rel]
        d["inclinacao_bruta"] = round(st.mean(S[7:])/st.mean(S[:7]), 2)
        d["inclinacao_vs_categoria"] = round(st.mean(rel[7:])/st.mean(rel[:7]), 2)
    return d

for seed, nome in PLAYERS:
    g = [r for r in kws if r["marca_seed"] == seed]
    p = perfil(g, seed); p["nome"] = nome
    # inclinacao por familia, calculada — nao digitada
    porfam = collections.defaultdict(list)
    for r in g:
        sr = serie(r)
        if sr: porfam[r["familia"]].append(sr)
    incl = {}
    for f, ss in porfam.items():
        S = [sum(x) for x in zip(*ss)]
        if st.mean(S[:7]) > 0:
            incl[f] = {"inclinacao": round(st.mean(S[7:])/st.mean(S[:7]), 2), "volume": round(sum(S)/12)}
    p["familias_inclinacao"] = incl
    # demanda que chega pelo NOME de uma submarca (atributo transversal)
    sub = [r for r in g if r.get("submarca") == "1"]
    p["submarca"] = {"volume": round(sum(num(r["volume_medio_12m"]) for r in sub)),
                     "kw": len(sub),
                     "itens": sorted([[r["keyword"], round(num(r["volume_medio_12m"])), r["familia"]] for r in sub],
                                     key=lambda x: -x[1])}
    out["players"][seed] = p
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

# ---------- a jornada em 4 estagios (estagio 0 = demanda sem marca nenhuma) ----------
def vol(rows): return sum(num(r["volume_medio_12m"]) for r in rows)
heads   = [r for r in kws if r["marca_seed"] == "generico"]
branded = [r for r in kws if r["marca_seed"] != "generico"]
j4 = {"heads": round(vol(heads)), "cauda": round(vol(cauda))}
j4["sem_marca"]  = j4["heads"] + j4["cauda"]
j4["descoberta"] = round(vol([r for r in branded if r["familia"] in DESCOBERTA]))
j4["escolha"]    = round(vol([r for r in branded if r["familia"] in ESCOLHA]))
j4["posse"]      = round(vol([r for r in branded if r["familia"] in POSSE]))
j4["nao_class"]  = round(vol(branded)) - j4["descoberta"] - j4["escolha"] - j4["posse"]
j4["total"]      = j4["sem_marca"] + round(vol(branded))
out["jornada4"] = j4

# ---------- exemplos reais de consulta, por familia, para os chips do deck ----------
def exemplos(rows, k=8):
    d = collections.defaultdict(list)
    for r in rows: d[r["familia"]].append([r["keyword"], round(num(r["volume_medio_12m"]))])
    return {f: sorted(v, key=lambda i: -i[1])[:k] for f, v in d.items()}
out["exemplos"] = exemplos(branded)                      # vocabulario das consultas COM marca
out["exemplos_sem_marca"] = exemplos(cauda)              # vocabulario da cauda SEM marca
out["exemplos_sem_marca"]["heads"] = sorted(
    [[r["keyword"], round(num(r["volume_medio_12m"]))] for r in heads], key=lambda i: -i[1])[:8]

# ---------- frentes nomeadas: os 40 termos de controle branded da lista ----------
fr = []
for r in csv.DictReader(open(RAW/"busca-convencional"/"2026-08-17_semrush_keywords_cauda-nao-branded.csv", encoding="utf-8-sig")):
    k = r["Keyword"].strip().lower()
    if lista.get(k, {}).get("familia") == "controle branded":
        fr.append([k, round(num(r.get("Volume")))])
out["frentes"] = sorted(fr, key=lambda i: -i[1])

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
# ================================================================ PANORAMA DE IA
# Base propria, normalizada por 20-normalizado/normalizar_ai.py. Nao se soma com a
# base de busca: mede outra coisa, com outra unidade.
TOP = list(csv.DictReader(open(NORM/"topicos.csv", encoding="utf-8")))
PRO = list(csv.DictReader(open(NORM/"prompts.csv", encoding="utf-8")))
def i(x):
    try: return int(float(x or 0))
    except: return 0

CATBR = [r for r in TOP if r["pais"] == "br" and r["eh_categoria"] == "1"]
VT = sum(i(r["volume"]) for r in CATBR)
pan = {"universo": {
    "topicos_exportados": len(TOP), "topicos_br": sum(1 for r in TOP if r["pais"] == "br"),
    "topicos_us": sum(1 for r in TOP if r["pais"] == "us"), "topicos_categoria": len(CATBR),
    "volume": VT, "prompts_declarados": sum(i(r["prompts"]) for r in CATBR),
    "seeds": sorted({r["seed"] for r in TOP}), "teto_por_export": 1000,
    "prompts_lidos": len(PRO), "prompts_distintos": len({r["prompt"] for r in PRO}),
    "provedores": sorted({r["provedor"] for r in PRO})}}

# --- eixo 1: cobertura pelo NOME do topico (sem vies de seed) ---------------
NUC = ["electrolux","brastemp","consul","samsung","midea","hisense","haier"]
NOMES = {"electrolux":"Electrolux","brastemp":"Brastemp","consul":"Consul","samsung":"Samsung",
         "midea":"Midea","hisense":"Hisense","haier":"Haier"}
def bloco(rows):
    v = sum(i(r["volume"]) for r in rows)
    return {"topicos": len(rows), "volume": v, "pct": round(100*v/VT, 2),
            "exemplos": [[r["topico"], i(r["volume"]), r["estagio"]]
                         for r in sorted(rows, key=lambda r: -i(r["volume"]))[:5]]}
EST_LISTA = ["exploracao de categoria", "descoberta", "escolha", "posse"]
VOL_EST = {e: sum(i(r["volume"]) for r in CATBR if r["estagio"] == e) for e in EST_LISTA}

def por_estagio(rows):
    """cobertura da marca dentro de cada estagio, sempre sobre o total daquele estagio"""
    d = {}
    for e in EST_LISTA:
        v = sum(i(r["volume"]) for r in rows if r["estagio"] == e)
        d[e] = {"volume": v, "pct": round(100*v/VOL_EST[e], 2) if VOL_EST[e] else 0}
    return d

pan["cobertura_nome"] = {m: dict(bloco([r for r in CATBR if m in r["marcas_nucleo"].split("|")]),
                                 nome=NOMES[m],
                                 por_estagio=por_estagio([r for r in CATBR if m in r["marcas_nucleo"].split("|")]))
                         for m in NUC}
pan["cobertura_nome"]["outras_marcas"] = dict(
    bloco([r for r in CATBR if r["eh_branded"] == "1" and not r["marcas_nucleo"]]), nome="Outras marcas")
pan["sem_marca"] = dict(bloco([r for r in CATBR if r["eh_branded"] == "0"]), nome="Sem marca nenhuma")

# --- eixo 2: jornada, e quanto de cada estagio esta sem marca --------------
EST = ["exploracao de categoria", "descoberta", "escolha", "posse"]
pan["estagios"] = {}
for e in EST:
    s = [r for r in CATBR if r["estagio"] == e]
    v = sum(i(r["volume"]) for r in s)
    sm = [r for r in s if r["eh_branded"] == "0"]
    fam = collections.Counter()
    for r in s: fam[r["familia"]] += i(r["volume"])
    pan["estagios"][e] = {
        "topicos": len(s), "volume": v, "pct": round(100*v/VT, 1),
        "prompts": sum(i(r["prompts"]) for r in s),
        "sem_marca_pct": round(100*sum(i(r["volume"]) for r in sm)/v, 1),
        "familias": [[f, c, round(100*c/v, 1)] for f, c in fam.most_common(6)],
        "exemplos": [[r["topico"], i(r["volume"]), r["familia"]]
                     for r in sorted(s, key=lambda r: -i(r["volume"]))[:6]],
        "exemplos_sem_marca": [[r["topico"], i(r["volume"]), r["familia"]]
                               for r in sorted(sm, key=lambda r: -i(r["volume"]))[:6]]}

# intent agregado, ponderado por volume — a leitura da propria ferramenta
ints = collections.Counter()
for r in CATBR:
    for k in ("informational","commercial","transactional","navigational","task"):
        ints[k] += i(r["volume"]) * float(r.get(f"int_{k}") or 0)
TI = sum(ints.values()) or 1
pan["intents"] = {k: round(100*v/TI, 1) for k, v in ints.most_common()}

# --- eixo 3: familias de necessidade, transversais aos estagios -------------
fam = collections.defaultdict(lambda: {"volume": 0, "topicos": 0, "sem_marca": 0, "ex": []})
for r in CATBR:
    d = fam[r["familia"]]; v = i(r["volume"])
    d["volume"] += v; d["topicos"] += 1
    if r["eh_branded"] == "0": d["sem_marca"] += v
    d["ex"].append([r["topico"], v])
pan["familias"] = {f: {"volume": d["volume"], "topicos": d["topicos"],
                       "pct": round(100*d["volume"]/VT, 1),
                       "sem_marca_pct": round(100*d["sem_marca"]/d["volume"], 1),
                       "exemplos": sorted(d["ex"], key=lambda x: -x[1])[:4]}
                   for f, d in fam.items()}

# --- eixo 4: ocupacao real por dominio (visibility x volume) ---------------
# presenca = a marca aparece no topico. ocupacao = presenca ponderada pela
# visibilidade que ela tem la dentro. As duas medem coisas diferentes e a
# distancia entre elas e o diagnostico.
CATIX = {r["topico"]: r for r in CATBR}
pan["ocupacao"] = {}
for fp in sorted(glob.glob(str(RAW/"ai-search"/"brand-topics"/"*.csv"))):
    dom = re.sub(r"^.*_ai-brand-topics_|\.csv$", "", os.path.basename(fp))
    bt = list(csv.DictReader(open(fp, encoding="utf-8-sig")))
    ov = [(r, CATIX[r["name"].strip()]) for r in bt if r["name"].strip() in CATIX]
    pres = sum(i(c["volume"]) for _, c in ov)
    ocup = sum(i(c["volume"]) * i(b["visibility"])/100 for b, c in ov)
    nomes = {r["name"].strip() for r in bt}
    porest = {}
    for e in EST:
        s = [r for r in CATBR if r["estagio"] == e]
        tv = sum(i(r["volume"]) for r in s) or 1
        pv = sum(i(r["volume"]) for r in s if r["topico"] in nomes)
        ov_e = sum(i(r["volume"]) * i(dict((x["name"].strip(), x) for x in bt)[r["topico"]]["visibility"])/100
                   for r in s if r["topico"] in nomes)
        porest[e] = {"presenca": round(100*pv/tv, 1), "ocupacao": round(100*ov_e/tv, 1),
                     "descoberto": round(100*(tv-pv)/tv, 1)}
    pan["ocupacao"][dom] = {
        "dominio": dom.replace("-com-br", ".com.br").replace("-", "."),
        "linhas": len(bt), "topicos_no_universo": len(ov),
        "fora_do_universo": sum(1 for r in bt if r["name"].strip() not in CATIX),
        "presenca_pct": round(100*pres/VT, 1), "ocupacao_pct": round(100*ocup/VT, 1),
        "visibility_mediana": round(st.median([i(b["visibility"]) for b, _ in ov])) if ov else None,
        "por_estagio": porest,
        "maiores": [[c["topico"], i(c["volume"]), i(b["visibility"]), i(b["mentions"]), c["estagio"]]
                    for b, c in sorted(ov, key=lambda x: -i(x[1]["volume"])*i(x[0]["visibility"]))[:6]]}

# --- eixo 5: os prompts, com o vies de seed declarado ----------------------
mres = collections.Counter()
for r in PRO:
    for m in r["marcas_na_resposta"].split("|"):
        if m: mres[m] += 1
N = len(PRO)
SEEDS = sorted({s for r in PRO for s in r["seeds"].split("|")})
pan["prompts"] = {
    "n": N, "distintos": len({r["prompt"] for r in PRO}), "seeds": SEEDS,
    "seeds_de_marca": [s for s in SEEDS if s not in ("geladeira",)],
    "sem_seed": [m for m in NUC if m not in [s.replace("eletrolux","electrolux") for s in SEEDS]],
    "por_provedor": {p: sum(1 for r in PRO if r["provedor"] == p) for p in sorted({r["provedor"] for r in PRO})},
    "mencao_na_resposta": [[m, c, round(100*c/N, 1)] for m, c in mres.most_common(10)],
    "marcas_por_resposta": round(st.mean([i(r["n_marcas_declarado"]) for r in PRO]), 1),
    "fontes_por_resposta": round(st.mean([i(r["n_fontes"]) for r in PRO]), 1),
    "sem_fonte_pct": round(100*sum(1 for r in PRO if i(r["n_fontes"]) == 0)/N),
    "familias": [[f, c] for f, c in collections.Counter(r["familia"] for r in PRO).most_common(8)]}
# Em que necessidades a IA responde nomeando um fabricante — e em quais ela responde
# sem nenhum. Calculado SO sobre o seed nao-branded: e o unico recorte em que a
# pergunta nao carrega marca, logo o unico em que a resposta nomear uma marca e
# decisao do modelo e nao eco do prompt.
def taxa_marca(rows):
    d = {}
    for f in {r["familia"] for r in rows}:
        s = [r for r in rows if r["familia"] == f]
        if len(s) < 20: continue
        c = sum(1 for r in s if any(m in NUC for m in r["marcas_na_resposta"].split("|") if m))
        d[f] = {"n": len(s), "com_marca": round(100*c/len(s), 1), "sem_marca": round(100*(len(s)-c)/len(s), 1)}
    return d
CATP = [r for r in PRO if r["eh_categoria"] == "1"]
LIMPO = [r for r in CATP if r["seeds"] == "geladeira"]
pan["prompts"]["marca_por_familia"] = taxa_marca(LIMPO)
pan["prompts"]["marca_por_familia_contaminado"] = taxa_marca(CATP)
pan["prompts"]["n_limpo"] = len(LIMPO)
c = sum(1 for r in LIMPO if any(m in NUC for m in r["marcas_na_resposta"].split("|") if m))
pan["prompts"]["taxa_marca_geral"] = round(100*c/len(LIMPO), 1)
pan["prompts"]["exemplos_limpos"] = {}
for f in pan["prompts"]["marca_por_familia"]:
    vistos, sel = set(), []
    for r in sorted([r for r in LIMPO if r["familia"] == f], key=lambda r: -i(r["relevancia"])):
        if r["prompt"] in vistos: continue     # o mesmo prompt vem uma vez por provedor
        vistos.add(r["prompt"]); sel.append(r)
        if len(sel) == 3: break
    pan["prompts"]["exemplos_limpos"][f] = [
        [r["prompt"][:150], r["provedor"],
         "|".join(m for m in r["marcas_na_resposta"].split("|") if m in NUC)] for r in sel]
pan["prompts"]["exemplos"] = {}
for f in ("assistencia e conserto","defeito e problema","manutencao e limpeza","peca e filtro",
          "instalacao","uso e receita","comparacao e modelo","preco e compra","produto e categoria"):
    sel = sorted([r for r in PRO if r["familia"] == f and r["eh_categoria"] == "1"],
                 key=lambda r: -i(r["relevancia"]))[:4]
    if sel: pan["prompts"]["exemplos"][f] = [[r["prompt"][:190], r["provedor"],
                                              r["marcas_na_resposta"]] for r in sel]
out["panorama"] = pan

out["meta"] = {"kw_total": len(kws), "kw_cauda": len(cauda), "perguntas_ia": 150,
               "prompts_ia": 4000, "meses_referrals": len(meses)}

json.dump(out, open(B/"30-analise"/"dados_do_deck.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK — {len(json.dumps(out))} bytes")
print("players:", list(out["players"]))
print("electrolux:", {k:v for k,v in out["players"]["electrolux"].items() if k in ("volume","descoberta","escolha","posse","inclinacao_vs_categoria","ai_overview")})
print("sem_dono:", {k:v for k,v in out["sem_dono"].items() if k in ("volume","posse","ai_overview")})
print("topicos:", {k:v["pct"] for k,v in out["ai"]["topicos"]["familias"].items()})
