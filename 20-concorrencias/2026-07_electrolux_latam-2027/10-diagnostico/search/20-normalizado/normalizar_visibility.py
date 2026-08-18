"""
Extrai os relatorios de AI Visibility (PDF) para CSV auditavel.

Cada relatorio e um "Desempenho da marca" da Semrush sobre UM dominio, numa
plataforma. Traz share of voice, mencoes e sentimento — medidas que nenhuma
outra fonte do pacote tem.

REGRA DE LEITURA QUE VEM ANTES DO NUMERO
Cada relatorio monta o proprio universo de perguntas, em torno do dominio
analisado. Por isso o mesmo player aparece com valores diferentes em relatorios
diferentes: a Electrolux tem 12,4% de SOV no relatorio dela, 16,5% no da Consul
e 11,2% no da Midea. **Nao se compara SOV entre relatorios.** A comparacao
valida e sempre entre players DENTRO do mesmo relatorio.

Os numeros sao lidos do texto do PDF por regex, nao digitados. Rodar de novo
reproduz o mesmo CSV; se o PDF mudar de layout, o script quebra em vez de mentir.

Uso: python3 normalizar_visibility.py  ->  20-normalizado/ai_visibility.csv
"""
import re, csv, subprocess, glob, os
from pathlib import Path

B = Path(__file__).resolve().parent.parent
RAW, OUT = B/"00-raw"/"ai-search"/"ai-visibility", B/"20-normalizado"

# como as marcas aparecem no relatorio -> chave do material
NOMES = {"electrolux (brazil official online store)": "electrolux", "electrolux": "electrolux",
         "consul": "consul", "brastemp": "brastemp", "midea": "midea", "samsung": "samsung",
         "hisense": "hisense", "haier": "haier", "lg": "lg", "panasonic": "panasonic",
         "philco": "philco", "other": "outras"}

def texto(pdf):
    r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(f"pdftotext falhou em {pdf}")
    return r.stdout

def pct(x): return float(x.replace(".", "").replace(",", "."))

def bloco(t, titulo, ate):
    i = t.index(titulo); return t[i:t.index(ate, i)]

linhas = []
for fp in sorted(glob.glob(str(RAW/"*.pdf"))):
    base = os.path.basename(fp)
    # 2026-08-18_ai-visibility_<dominio>_<plataforma>.pdf
    m = re.match(r"(\d{4}-\d{2}-\d{2})_ai-visibility_([^_]+)_(.+)\.pdf", base)
    if not m: raise RuntimeError(f"nome fora do padrao: {base}")
    data, dominio, plat = m.groups()
    plataforma = {"chatgpt": "ChatGPT", "google-ai-mode": "Google AI Mode"}[plat]
    t = texto(fp)

    sov = {}
    for nome, v in re.findall(r"^\s*([A-Za-z][A-Za-z ()À-ÿ]+?)\s{2,}(\d{1,2},\d)%\s*$",
                              bloco(t, "Distribuição de Share of Voz", "Gerado em"), re.M):
        k = NOMES.get(nome.strip().lower())
        if k: sov[k] = pct(v)

    sb = bloco(t, "Sentimento geral", "Distribuição de Share of Voz")
    fav = re.search(r"Favorable\s{2,}(\d{1,3})%", sb)
    favoravel = int(fav.group(1)) if fav else None

    men = {}
    for nome, v, n in re.findall(
            r"^\s*([A-Za-z][A-Za-z ()À-ÿ]+?)\s{2,}(\d{1,2},?\d?)%\s{2,}(\d+)\s*$", t, re.M):
        k = NOMES.get(nome.strip().lower())
        if k and k not in men: men[k] = (pct(v), int(n))

    # o dominio analisado, como chave de marca — para saber de quem e o sentimento
    dono = {"loja-electrolux": "electrolux", "consul": "consul", "midea": "midea"}.get(dominio, dominio)
    for marca, v in sorted(sov.items(), key=lambda i: -i[1]):
        mm = men.get(marca, (None, None))
        linhas.append({
            "relatorio": f"{dominio} · {plataforma}", "data": data,
            "dominio_analisado": dominio, "plataforma": plataforma,
            "marca": marca, "eh_o_dono_do_relatorio": int(marca == dono),
            "share_of_voice": v, "mencoes_pct": mm[0], "mencoes_n": mm[1],
            "sentimento_favoravel_do_dono": favoravel if marca == dono else ""})

with open(OUT/"ai_visibility.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)

print(f"ai_visibility.csv — {len(linhas)} linhas · "
      f"{len({l['relatorio'] for l in linhas})} relatórios\n")
for rel in sorted({l["relatorio"] for l in linhas}):
    sub = [l for l in linhas if l["relatorio"] == rel]
    fav = next((l["sentimento_favoravel_do_dono"] for l in sub if l["eh_o_dono_do_relatorio"]), "")
    print(f"{rel}   (favorável do dono: {fav}%)")
    for l in sub:
        marca = l["marca"] + (" ←" if l["eh_o_dono_do_relatorio"] else "")
        print(f"   {marca:14} SOV {l['share_of_voice']:>5}%")
    print()
print("Lembrete: SOV NAO se compara entre relatorios. So entre players do mesmo relatorio.")
