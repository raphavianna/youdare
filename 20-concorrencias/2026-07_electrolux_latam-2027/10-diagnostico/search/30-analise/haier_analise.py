"""
Leitura de busca da Haier no Brasil — reproduz os numeros de
2026-08-17_youdare_analise_haier-entrada-brasil.md

Premissa declarada: o campo Trend do SEMrush e o indice mensal normalizado pelo
pico, com 12 pontos. Logo vol_i = Volume * T_i / media(T). Confianca media (R3).

Uso:  python3 haier_analise.py <dir_00-raw/busca-convencional>
"""
import csv, re, sys, statistics as st, warnings, collections
from pathlib import Path
import openpyxl
warnings.filterwarnings("ignore")

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "../00-raw/busca-convencional")

FR = r"\b(lave|linge|refrigerateur|congelateur|frigo|cave a vin|lave vaisselle|t[ée]l[ée]viseur|hublot|sechant|silencieux|noir|gris|americain|multiporte|encastrable|ventile|lumiere)\b"
EN = r"\b(washing machine|fridge|refrigerator|refrigerators|fridges|dishwasher|air conditioner|air conditioning|appliances|smart home|group|corp|corporation|electronics|logo|inch|led|company|europe|china|ceo|biomedical|freezer|airco|hong)\b"
PT_GUARD = r"geladeira|adega|ar condicionado|ar-condicionado|eletrodom|marca|assist|é bom|controle remoto|port[áa]til|btus?"

FAMILIAS = {
    "marca pura / curiosidade": r"^haier$|haier brasil|marca haier|haier eletrodom|haier electronics|haier logo|haier company|haier elegance",
    "ar condicionado":          r"ar[- ]condicionado|btus?|\bar portatil\b|controle remoto",
    "tv":                       r"\btv\b|television|televis|inch|55c11",
    "adega":                    r"adega",
    "geladeira / MDA":          r"geladeira|refrigera(?!teur)|lava|lavadora|airfryer|air fryer",
    "confianca / avaliacao":    r"é bom|e bom|vale a pena|confi[áa]vel|durabilidade|review|avalia",
    "servico / pos-compra":     r"assist|servic|manual|garantia|pe[çc]a|conserto|t[ée]cnic",
    "comunicacao / patrocinio": r"eliana|liverpool|roland garros|patroc",
}

def volume(v):
    try:    return int(float(str(v).replace(",", "")))
    except: return 0

def trend(s):
    try:
        v = [float(x) for x in str(s).split(",")]
        return v if len(v) == 12 else None
    except: return None

def serie_mensal(r):
    """Reconstroi a serie mensal absoluta a partir de Volume (media 12m) e Trend."""
    t, v = trend(r.get("Trend")), volume(r.get("Volume"))
    if not t or st.mean(t) == 0:
        return [v] * 12
    m = st.mean(t)
    return [v * x / m for x in t]

def eh_pt(kw):
    k = kw.lower()
    if re.search(FR, k) or re.search(r"servicio tecnico|aire acondicionado", k):
        return False
    if re.search(EN, k) and not re.search(PT_GUARD, k):
        return False
    return True

def ler_csv(p):
    with open(p, encoding="utf-8-sig") as fh:
        return [r for r in csv.DictReader(fh) if r.get("Keyword")]

def ler_xlsx(p, aba="Keywords"):
    wb = openpyxl.load_workbook(p, data_only=True)
    linhas = [r for r in wb[aba].iter_rows(values_only=True) if r and r[0]]
    hdr = list(linhas[0])
    wb.close()
    return [dict(zip(hdr, r)) for r in linhas[1:]]

def sparkline(t):
    return "".join("▁▂▃▄▅▆▇█"[min(7, int(x * 7.99))] for x in t) if t else ""

haier = ler_csv(RAW / "2026-08-17_semrush_keywords_haier.csv")
elux  = ler_xlsx(RAW / "2026-08-17_semrush_keywords_electrolux-branded.xlsx")
pt    = [r for r in haier if eh_pt(r["Keyword"])]

# 1. idioma
print("## idioma da query (base br)")
por_idioma = collections.Counter()
for r in haier:
    por_idioma["PT" if eh_pt(r["Keyword"]) else "estrangeira"] += volume(r["Volume"])
total = sum(por_idioma.values())
for k, v in por_idioma.items():
    print(f"   {k:12} vol {v:>7,} | {100*v/total:5.1f}%")

# 2. serie mensal e proporcao (ponto 8 = primeiro mes pos-marco/26)
sh = [sum(x) for x in zip(*[serie_mensal(r) for r in pt])]
se = [sum(x) for x in zip(*[serie_mensal(r) for r in elux])]
print("\n## serie mensal reconstruida — Haier PT-BR")
print("   " + "  ".join(f"{x:,.0f}" for x in sh))
print(f"\n{'medida':22} {'Haier':>10} {'Electrolux':>12} {'proporcao':>10}")
for nome, fn in [("media 12 meses", lambda s: st.mean(s)),
                 ("media pos-marco/26", lambda s: st.mean(s[7:])),
                 ("ultimo mes", lambda s: s[-1])]:
    h, e = fn(sh), fn(se)
    print(f"{nome:22} {h:>10,.0f} {e:>12,.0f} {100*h/e:>9.2f}%")

# 3. composicao
print("\n## composicao do volume corrente (PT-BR)")
def corrente(r): return serie_mensal(r)[-1]
tot = sum(corrente(r) for r in pt)
for nome, padrao in FAMILIAS.items():
    rx = re.compile(padrao, re.I)
    m = [r for r in pt if rx.search(r["Keyword"].lower())]
    v = sum(corrente(r) for r in m)
    print(f"   {nome:26} {len(m):>3} kw | {v:>7,.0f} | {100*v/tot:5.1f}%")

# 4. forma da serie — separa alta sustentada de pico isolado
print("\n## forma da serie (PT-BR, volume medio >= 40)")
for r in sorted(pt, key=lambda r: -volume(r["Volume"])):
    t = trend(r["Trend"])
    if not t or volume(r["Volume"]) < 40:
        continue
    sustentada = t[-1] >= 0.9 and t[-2] >= 0.5 and st.mean(t[9:]) > st.mean(t[:7])
    print(f"   {r['Keyword'][:38]:38} {volume(r['Volume']):>6,} {sparkline(t)}"
          f"  {'ALTA SUSTENTADA' if sustentada else ''}")

# 5. teste de comunicacao
print("\n## termos de comunicacao citados no briefing")
for termo in ["eliana", "liverpool", "roland garros", "patroc"]:
    m = [r["Keyword"] for r in haier if termo in r["Keyword"].lower()]
    print(f"   {termo:15} {m if m else '— nenhuma'}")
