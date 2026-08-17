"""
Territorios anunciados e vagos — pre-leitura pelo corpus de IA.
Reproduz 2026-08-17_youdare_analise_territorio-anunciado-e-vago.md

Taxonomia derivada do proprio dado, em ordem de prioridade: a primeira familia
que casar vence. Cobertura ~50% — declarada no documento, nao mascarada.

Uso: python3 territorio_analise.py <dir_00-raw/ai-search>
"""
import csv, re, sys, collections
from pathlib import Path
csv.field_size_limit(10**7)

RAW = Path(sys.argv[1] if len(sys.argv) > 1 else "../00-raw/ai-search")
TOPICOS = ["eletrolux", "geladeira", "hisense", "midea"]

TAXONOMIA = [
    ("FORA DE CATEGORIA",      r"\b(himss|hbento|sa[uú]de|health|quatenus|quomodo|rationem|suggestis|facultates|insight|login|conferenc|exhibitor)\b"),
    ("assistencia / reparo",   r"\b(assist[eê]ncia|conserto|consertar|reparo|reparar|t[ée]cnic|autorizada|chamado|substituir|trocar a|troca de)\b"),
    ("defeito / problema",     r"\b(n[aã]o (gela|liga|funciona|centrifuga|seca|esquenta)|erro|defeito|problema|barulho|vazando|vazamento|parou de|entupid)\b"),
    ("peca / consumivel",      r"\b(pe[çc]a|filtro|correia|resist[eê]ncia|refil|l[aâ]mpada|g[aá]s refrigerante|reposi[çc]|acess[oó]rio)\b"),
    ("instalacao",             r"\b(instala[çc]|instalar|montar|montagem|encaixe|medidas do v[aã]o)\b"),
    ("garantia",               r"\b(garantia|cobertura|extens[aã]o de garantia)\b"),
    ("uso / como fazer",       r"\b(como (usar|limpar|lavar|programar|configurar|ligar|regular|ajustar|higienizar|secar|descongelar|desodorizar)|passo a passo|tutorial|manual)\b"),
    ("manutencao / cuidado",   r"\b(manuten[çc]|cuidad|conserva[çr]|limpeza|higieniz|durabilidade|vida [uú]til|prolongar)\b"),
    ("descarte / sustentab",   r"\b(descart|recicl|sustentab|coleta consciente|meio ambiente)\b"),
    ("receita / preparo",      r"\b(receita|assar|cozinhar|preparar|air.?fryer.*fazer)\b"),
    ("consumo / eficiencia",   r"\b(consumo|consome|gasta|kwh|energia|econ[oô]mic|efici[eê]nc|selo|procel|inmetro|conta de luz)\b"),
    ("conectividade / smart",  r"\b(smart|wi.?fi|conect|aplicativo|intelig[eê]nt|automa[çc])\b"),
    ("aquisicao / comparacao", r"\b(melhor|melhores|compar|vale a pena|custo.?benef|diferen[çc]a entre|\bvs\b|versus|recomend|escolher|barat|pre[çc]o|quanto custa|onde comprar|comprar|oferta|promo|venda|vender)\b"),
    ("especificacao produto",  r"\b(frost free|inverter|lava e seca|lava.?seca|essential care|essencial care|side by side|\d+\s?(kg|litros|l\b|btus?|polegadas)|duplex|invertida|coifa|cooktop|micro.?ondas|aspirador|lava.?lou[çc]as|freezer|fog[aã]o|forno)\b"),
    ("marca / navegacao",      r"^(electrolux|eletrolux|midea|hisense|haier|brastemp|consul|samsung)[\s\w]{0,25}$"),
]

VIDA_COM_O_PRODUTO = {
    "assistencia / reparo", "defeito / problema", "peca / consumivel", "instalacao",
    "garantia", "uso / como fazer", "manutencao / cuidado", "descarte / sustentab",
    "receita / preparo",
}
AQUISICAO = {"aquisicao / comparacao", "especificacao produto", "marca / navegacao"}

def classificar(texto):
    t = (texto or "").lower()
    for nome, padrao in TAXONOMIA:
        if re.search(padrao, t):
            return nome
    return "nao classificado"

def carregar_prompts():
    saida = []
    for topico in TOPICOS:
        with open(RAW / f"2026-08-17_ai-prompts_topico-{topico}.csv", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r.get("prompt"):
                    saida.append((topico, r["prompt"]))
    return saida

def carregar_perguntas_nao_branded():
    with open(RAW / "2026-08-14_semrush_ai-answers_non-branded-brasil.csv", encoding="utf-8") as fh:
        return sorted({r["Question"] for r in csv.DictReader(fh) if r.get("Question")})

def relatorio(textos, titulo):
    contagem = collections.Counter(classificar(t) for t in textos)
    fora = contagem.pop("FORA DE CATEGORIA", 0)
    base = len(textos) - fora
    print(f"\n## {titulo}   n={len(textos)}   fora de categoria: {fora} ({100*fora/len(textos):.1f}%)")
    for familia, n in contagem.most_common():
        marca = " ←vida com o produto" if familia in VIDA_COM_O_PRODUTO else ""
        print(f"   {familia:26} {n:>5} | {100*n/base:5.1f}%{marca}")
    vida = sum(contagem[f] for f in VIDA_COM_O_PRODUTO)
    aquis = sum(contagem[f] for f in AQUISICAO)
    nc = contagem["nao classificado"]
    print(f"   {'-'*52}")
    print(f"   {'VIDA COM O PRODUTO':26} {vida:>5} | {100*vida/base:5.1f}%")
    print(f"   {'AQUISICAO (total)':26} {aquis:>5} | {100*aquis/base:5.1f}%")
    print(f"   {'cobertura da taxonomia':26} {base-nc:>5} | {100*(base-nc)/base:5.1f}%")

prompts = carregar_prompts()
relatorio([p for _, p in prompts], "4.000 prompts de IA — todos")
for topico in ["geladeira", "eletrolux"]:
    relatorio([p for t, p in prompts if t == topico], f"topico '{topico}'")
relatorio(carregar_perguntas_nao_branded(), "150 perguntas nao-branded (AI answers)")

# vocabulario real das familias de vida com o produto — insumo do seed list do Tier 1
print("\n\n## vocabulario observado — familias de vida com o produto")
corpus = [p for _, p in prompts] + carregar_perguntas_nao_branded()
for familia in sorted(VIDA_COM_O_PRODUTO):
    exemplos = [p for p in corpus if classificar(p) == familia]
    if not exemplos:
        print(f"\n### {familia}: NENHUMA pergunta no corpus")
        continue
    print(f"\n### {familia}  ({len(exemplos)} perguntas)")
    vistos = []
    for p in exemplos:
        if p not in vistos:
            vistos.append(p)
        if len(vistos) == 5:
            break
    for p in vistos:
        print(f"   - {p[:110]}")
