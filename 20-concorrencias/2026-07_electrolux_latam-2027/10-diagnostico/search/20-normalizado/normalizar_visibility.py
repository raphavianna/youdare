"""
Extrai os relatorios de AI Visibility (PDF) para CSV auditavel.

Fonte: dois PDFs de "Desempenho da marca" sobre loja.electrolux.com.br, um por
plataforma (ChatGPT e Google AI Mode). Trazem uma medida que nenhuma outra fonte
do pacote tem: **share of voice em resposta de IA**, por marca, com sentimento.

Os numeros sao lidos do texto do PDF por regex, nao digitados. Rodar de novo
reproduz o mesmo CSV; se o PDF mudar, o script quebra em vez de mentir.

Uso: python3 normalizar_visibility.py  ->  20-normalizado/ai_visibility.csv
"""
import re, csv, subprocess
from pathlib import Path

B = Path(__file__).resolve().parent.parent
RAW, OUT = B/"00-raw"/"ai-search", B/"20-normalizado"

PDFS = [("ChatGPT",        "2026-08-17_semrush_ai-visibility_desempenho-marca-chatgpt.pdf"),
        ("Google AI Mode", "2026-08-17_semrush_ai-visibility_desempenho-marca-google-ai-mode.pdf")]

# como as marcas aparecem no relatorio -> chave do material
NOMES = {"electrolux (brazil official online store)": "electrolux", "consul": "consul",
         "brastemp": "brastemp", "midea": "midea", "samsung": "samsung", "other": "outras"}

def texto(pdf):
    r = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True)
    if r.returncode != 0: raise RuntimeError(f"pdftotext falhou em {pdf}")
    return r.stdout

def pct(x): return float(x.replace(".", "").replace(",", "."))

def bloco(t, titulo, ate):
    """recorta o trecho entre um titulo de secao e o proximo marcador"""
    i = t.index(titulo)
    j = t.index(ate, i)
    return t[i:j]

linhas = []
for plataforma, arq in PDFS:
    t = texto(RAW/arq)

    # --- share of voice: "Marca    14,7%"
    sov = {}
    for nome, v in re.findall(r"^\s*([A-Za-z][A-Za-z ()À-ÿ]+?)\s{2,}(\d{1,2},\d)%\s*$",
                              bloco(t, "Distribuição de Share of Voz", "Gerado em"), re.M):
        k = NOMES.get(nome.strip().lower())
        if k: sov[k] = pct(v)

    # --- sentimento geral: "Favorable   41%"
    sb = bloco(t, "Sentimento geral", "Distribuição de Share of Voz")
    fav = re.search(r"Favorable\s{2,}(\d{1,3})%", sb)
    favoravel = int(fav.group(1)) if fav else None

    # --- mencoes: "Marca    24,7%    37" (a tabela quebra em duas paginas)
    men = {}
    for nome, v, n in re.findall(
            r"^\s*([A-Za-z][A-Za-z ()À-ÿ]+?)\s{2,}(\d{1,2},?\d?)%\s{2,}(\d+)\s*$", t, re.M):
        k = NOMES.get(nome.strip().lower())
        if k and k not in men: men[k] = (pct(v), int(n))

    for marca in ["electrolux", "consul", "brastemp", "midea", "samsung", "outras"]:
        if marca not in sov: continue
        m = men.get(marca, (None, None))
        linhas.append({"plataforma": plataforma, "marca": marca,
                       "share_of_voice": sov[marca],
                       "mencoes_pct": m[0], "mencoes_n": m[1],
                       "sentimento_favoravel_marca": favoravel if marca == "electrolux" else ""})

with open(OUT/"ai_visibility.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0].keys())); w.writeheader(); w.writerows(linhas)

print(f"ai_visibility.csv — {len(linhas)} linhas, {len(PDFS)} plataformas\n")
for p, _ in PDFS:
    sub = [l for l in linhas if l["plataforma"] == p]
    print(f"{p}:")
    for l in sub:
        mp = f'{l["mencoes_pct"]}% ({l["mencoes_n"]})' if l["mencoes_pct"] is not None else "—"
        print(f"   {l['marca']:11} SOV {l['share_of_voice']:>5}%   menções {mp}")
    print()
