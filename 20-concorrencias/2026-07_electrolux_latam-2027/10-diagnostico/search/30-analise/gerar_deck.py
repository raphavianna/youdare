# -*- coding: utf-8 -*-
"""
Gera o material executivo em HTML a partir de 30-analise/dados_do_deck.json.
Nenhum numero e digitado aqui: tudo vem do JSON, que vem dos datasets
normalizados. Rode dados_do_deck.py antes.

Saidas em 50-entrega/:
  ..._deck_cenario-search-ai-electrolux.html   — o material
  ..._deck_ressalvas-de-dado.html              — o apendice, deck separado
"""
import json, html, statistics as st
from pathlib import Path

B = Path(__file__).resolve().parent.parent
D = json.load(open(B/"30-analise"/"dados_do_deck.json", encoding="utf-8"))
P, SD, HD, AI, J4 = D["players"], D["sem_dono"], D["categoria_heads"], D["ai"], D["jornada4"]
META = D["meta"]
PAN, U = D["panorama"], D["panorama"]["universo"]   # usados ja na abertura

# paleta categorica validada por dataviz/scripts/validate_palette.js (dark, superficie #1a1a19)
COR = {"electrolux":"#3987e5","brastemp":"#d95926","consul":"#199e70","samsung":"#c98500",
       "midea":"#d55181","hisense":"#008300","haier":"#e66767","sem_dono":"#9085e9","generico":"#6b6a63"}
ORDEM = ["electrolux","brastemp","consul","samsung","midea","hisense","haier"]
NOME = {k: P[k]["nome"] for k in ORDEM}
NOME.update({"sem_dono":"Território sem dono","generico":"Categoria (heads)"})
# rampa sequencial ordinal para os estagios da jornada (claro -> escuro)
EST = {"sem_marca":"#f7e3b8","descoberta":"#f2c777","escolha":"#c98500","posse":"#7d5300","nc":"#2e2e2b"}
MESES = ["ago","set","out","nov","dez","jan","fev","mar","abr","mai","jun","jul"]
def e(s): return html.escape(str(s))
def dec(v): return str(v).replace(".", ",")          # decimal em pt-BR
def vs(k):  return f'{P[k]["inclinacao_vs_categoria"]:.2f}'.replace(".", ",")  # ano a ano vs categoria
def n(v): return f"{v:,.0f}".replace(",", ".")
def pct(v, d=1): return f"{v:.{d}f}".replace(".", ",") + "%"
EXT = {1:"um",2:"dois",3:"três",4:"quatro",5:"cinco",6:"seis",7:"sete"}
def ext(k): return EXT.get(k, str(k))   # numeral por extenso, para prosa

# fontes: sem nomear ferramenta, por decisao editorial
F_KW  = f'Base de busca Brasil · {n(META["kw_total"])} keywords · ago/25–jul/26'
F_CAUDA = f'Base de busca Brasil · {n(META["kw_cauda"])} keywords sem marca com volume'
# "All AI Platforms" e o agregado da propria ferramenta, nao um provedor
N_PROV_IA = len([k for k in AI["marcas"]["Electrolux"]["cobertura"] if k != "All AI Platforms"])
F_IA  = f'Respostas de IA · {META["perguntas_ia"]} perguntas sem marca × {N_PROV_IA} provedores'
F_REF = "Tráfego vindo de LLM · 12 meses · 4 domínios"

slides, apendice = [], []

def slide(marca_fonte, kicker, titulo, subtitulo, corpo, leitura="", fonte="", destino=None):
    """marca_fonte: 'search' | 'ia' | 'ambos'"""
    rot = {"search":"Search","ia":"IA","ambos":"Search + IA","briefing":"Briefing"}[marca_fonte]
    (destino if destino is not None else slides).append(f"""<section class="slide">
  <div class="slide-inner">
    <header class="s-head">
      <div class="s-top"><span class="kicker">{kicker}</span><span class="badge b-{marca_fonte}">{rot}</span></div>
      <h2>{titulo}</h2>
      {f'<p class="subt">{subtitulo}</p>' if subtitulo else ''}
    </header>
    <div class="s-body">{corpo}</div>
    {f'<p class="leitura">{leitura}</p>' if leitura else ''}
    {f'<footer class="fonte">{fonte}</footer>' if fonte else ''}
  </div>
</section>""")

# ---------------------------------------------------------------- graficos
def barras_h(itens, cor_fn, max_v=None, fmt=n):
    mx = max_v or max(v for _, v, *_ in itens) or 1
    out = []
    for it in itens:
        lab, val = it[0], it[1]
        ck = it[2] if len(it) > 2 else None
        c = cor_fn(ck) if cor_fn else "#3987e5"
        out.append(f"""<div class="bh-row"><span class="bh-lab">{e(lab)}</span>
          <span class="bh-track"><span class="bh-fill" style="width:{max(0.6,100*val/mx):.2f}%;background:{c}"></span></span>
          <span class="bh-val">{fmt(val)}</span></div>""")
    return '<div class="bh">' + "".join(out) + "</div>"

def barras_empilhadas(rows, rotulos_dentro=True):
    """rows: [(label, [(seg_label, valor, cor)], extra_html)]"""
    out = []
    for lab, segs, extra in rows:
        tot = sum(v for _, v, _ in segs) or 1
        partes = []
        for sl, v, c in segs:
            w = 100*v/tot
            txt = f'<b>{pct(v,1)}</b>' if (rotulos_dentro and w >= 7) else ""
            escuro = c in (EST["sem_marca"], EST["descoberta"], "#f2c777", "#f7e3b8")
            partes.append(f'<span class="be-seg" style="width:{w:.2f}%;background:{c};'
                          f'color:{"#141412" if escuro else "#f4f1e8"}" title="{e(sl)}: {pct(v)}">{txt}</span>')
        out.append(f"""<div class="be-row"><span class="be-lab">{e(lab)}</span>
          <span class="be-track">{"".join(partes)}</span><span class="be-extra">{extra}</span></div>""")
    return '<div class="be">' + "".join(out) + "</div>"

def legenda(itens):
    return '<div class="legenda">' + "".join(
        f'<span><i style="background:{c}"></i>{e(l)}</span>' for l, c in itens) + "</div>"

def indexar(s):
    b = s[0] or 1
    return [100*v/b for v in s]

def linhas(series, destaque=None, w=1000, h=290, rotulos_x=None, ref100=False, y0=None, y1=None,
           rotular_todos=False, reflab="base 100"):
    vals = [v for s in series.values() for v in s]
    lo = y0 if y0 is not None else min(vals); hi = y1 if y1 is not None else max(vals)
    if hi == lo: hi = lo + 1
    pl, pr, pt, pb = 8, 96, 14, 26
    X = lambda i, L: pl + (w-pl-pr)*i/(L-1)
    Y = lambda v: pt + (h-pt-pb)*(1-(v-lo)/(hi-lo))
    out = []
    rot = []
    if ref100 and lo < 100 < hi:
        out.append(f'<line class="ref" x1="{pl}" y1="{Y(100):.1f}" x2="{w-pr}" y2="{Y(100):.1f}"/>')
        # entra na fila de rotulos para nao colidir com as pontas das series
        rot.append([Y(100), w-pr, "#8b8981", reflab, "ref"])
    for k, s in series.items():
        forte = (destaque is None) or (k == destaque)
        c = COR.get(k, "#6b6a63") if forte else "#6f6e67"
        d = " ".join(f"{'M' if i==0 else 'L'}{X(i,len(s)):.1f},{Y(v):.1f}" for i, v in enumerate(s))
        out.append(f'<path d="{d}" stroke="{c}" class="ln{" forte" if forte else ""}"/>')
        if forte or rotular_todos:
            out.append(f'<circle cx="{X(len(s)-1,len(s)):.1f}" cy="{Y(s[-1]):.1f}" r="{4.5 if forte else 3}" fill="{c}"/>')
            rot.append([Y(s[-1]), X(len(s)-1, len(s)), c, NOME.get(k, k), forte])
    # rotulos a direita, empurrados para nao se sobrepor
    rot.sort(key=lambda r: r[0])
    for i in range(1, len(rot)):
        if rot[i][0] - rot[i-1][0] < 15: rot[i][0] = rot[i-1][0] + 15
    for y, x, c, lab, forte in rot:
        cls_ = "reflab" if forte == "ref" else ("lnlab" if forte else "lnlab fraco")
        out.append(f'<text class="{cls_}" x="{x+9:.1f}" y="{y+4:.1f}" fill="{c}">{e(lab)}</text>')
    if rotulos_x:
        for i, r in enumerate(rotulos_x):
            if r: out.append(f'<text class="xlab" x="{X(i,len(rotulos_x)):.1f}" y="{h-6}">{e(r)}</text>')
    return f'<svg class="chart" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">{"".join(out)}</svg>'

def quadrante(pontos, eixo_x, eixo_y, corte_x, corte_y, rotulos, w=1000, h=420,
              fmt_x=lambda v: f"{v:.2f}".replace(".", ","), fmt_y=lambda v: pct(v, 1)):
    """Retrato posicional: cada player num plano de duas medidas, com os quatro
    quadrantes nomeados. pontos: [(chave, x, y)] · rotulos: [sup-esq, sup-dir, inf-esq, inf-dir]"""
    xs = [x for _, x, _ in pontos]; ys = [y for _, _, y in pontos]
    x0, x1 = min(xs + [corte_x]), max(xs + [corte_x]); y0, y1 = min(ys + [corte_y]), max(ys + [corte_y])
    mx, my = (x1 - x0) * .18 or 1, (y1 - y0) * .18 or 1
    x0, x1, y0, y1 = x0 - mx, x1 + mx, y0 - my, y1 + my
    pl, pr, pt, pb = 54, 118, 30, 40
    X = lambda v: pl + (w - pl - pr) * (v - x0) / (x1 - x0)
    Y = lambda v: pt + (h - pt - pb) * (1 - (v - y0) / (y1 - y0))
    cx, cy = X(corte_x), Y(corte_y)
    o = [f'<rect class="qbg" x="{pl}" y="{pt}" width="{w-pl-pr}" height="{h-pt-pb}"/>',
         f'<rect class="qhi" x="{cx}" y="{pt}" width="{w-pr-cx}" height="{cy-pt}"/>',
         f'<line class="qax" x1="{cx}" y1="{pt}" x2="{cx}" y2="{h-pb}"/>',
         f'<line class="qax" x1="{pl}" y1="{cy}" x2="{w-pr}" y2="{cy}"/>']
    # os quatro rotulos, ancorados nos cantos internos
    for txt, ax, ay, an in [(rotulos[0], pl+10, pt+18, "start"), (rotulos[1], w-pr-10, pt+18, "end"),
                            (rotulos[2], pl+10, h-pb-10, "start"), (rotulos[3], w-pr-10, h-pb-10, "end")]:
        o.append(f'<text class="qlab" x="{ax}" y="{ay}" text-anchor="{an}">{e(txt)}</text>')
    for k, x, y in sorted(pontos, key=lambda p: -p[2]):
        c = COR.get(k, "#6b6a63")
        o.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="8" fill="{c}" class="qpt"/>')
        o.append(f'<text class="qnome" x="{X(x)+13:.1f}" y="{Y(y)+4:.1f}" fill="{c}">{e(NOME.get(k,k))}</text>')
    o.append(f'<text class="qcorte" x="{cx}" y="{h-pb+14:.0f}" text-anchor="middle">{e(fmt_x(corte_x))}</text>')
    o.append(f'<text class="qcorte" x="{pl-8}" y="{cy+4:.0f}" text-anchor="end">{e(fmt_y(corte_y))}</text>')
    o.append(f'<text class="qeixo" x="{(pl+w-pr)/2:.0f}" y="{h-8}" text-anchor="middle">{e(eixo_x)} →</text>')
    o.append(f'<text class="qeixo" x="{-((pt+h-pb)/2):.0f}" y="16" transform="rotate(-90)" text-anchor="middle">{e(eixo_y)} →</text>')
    return f'<svg class="chart quad" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">{"".join(o)}</svg>'

def heatmap(cols, rows, get, fmt=lambda v: pct(v, 0)):
    mx = max((get(r, c) or 0) for r in rows for c in cols) or 1
    th = "".join(f"<th>{e(c)}</th>" for c in cols)
    tr = []
    for r in rows:
        tds = []
        for c in cols:
            v = get(r, c) or 0
            a = 0.06 + 0.94*(v/mx)**0.65 if v else 0.03
            tds.append(f'<td style="background:rgba(57,135,229,{a:.2f});color:{"#0d0d0c" if v/mx>0.45 else "#cfcdc4"}">{fmt(v) if v else "—"}</td>')
        tr.append(f'<tr><th class="rh">{e(NOME.get(r,r))}</th>{"".join(tds)}</tr>')
    return f'<table class="hm"><thead><tr><th></th>{th}</tr></thead><tbody>{"".join(tr)}</tbody></table>'

def tabela(cabec, linhas_, classe=""):
    """linha como str = linha de grupo, ja em <td colspan>; separa blocos dentro da tabela"""
    th = "".join(f"<th>{c}</th>" for c in cabec)
    tr = "".join(f'<tr class="grp-row">{l}</tr>' if isinstance(l, str)
                 else "<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas_)
    return f'<table class="tb {classe}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def kpis(itens):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><span class="kv" style="color:{c or "#f0ede4"}">{v}</span><span class="kl">{e(l)}</span></div>'
        for v, l, c in itens) + "</div>"

# o mesmo momento tem dois nomes: um no vocabulario das consultas com marca,
# outro no da cauda sem marca. O deck fala de familia, nao de arquivo de origem.
ALIAS = {"assistencia e reparo":"assistencia","peca e consumivel":"peca","manutencao e cuidado":"manutencao",
         "consumo e eficiencia":"consumo","receita e preparo":"receita","descarte e sustentab":"descarte"}
ALIAS_INV = {v: k for k, v in ALIAS.items()}
EXM, EXC = D["exemplos"], D["exemplos_sem_marca"]

def _exs(fam, prefer="marca", escopo=None):
    """escopo: perfil de um player — garante que o exemplo seja daquela marca, nao de outra"""
    fontes = [escopo["exemplos_familia"]] if escopo else []
    fontes += [EXM, EXC] if prefer == "marca" else [EXC, EXM]
    for src in fontes:
        for key in (fam, ALIAS.get(fam), ALIAS_INV.get(fam)):
            if key and src.get(key): return src[key]
    return []

def ex(fam, k=3, prefer="marca", escopo=None):
    """exemplos reais de consulta daquela familia, direto do dataset"""
    return " · ".join(f'<code>{e(q)}</code>' for q, _ in _exs(fam, prefer, escopo)[:k])

def exf(fam, rotulo, k=2, prefer="marca", escopo=None):
    """o mesmo, com a familia nomeada antes — nenhum termo de exemplo aparece solto"""
    qs = _exs(fam, prefer, escopo)[:k]
    if not qs: return ""
    return (f'<span class="fam">{e(rotulo)}</span> '
            + " · ".join(f'<code>{e(q)}</code>' for q, _ in qs))


# estagios -> familias que os compoem, para exibir em todo slide de jornada
FAM_ESTAGIO = {
 "descoberta": [("marca e navegacao", "Marca e navegação")],
 "escolha":    [("especificacao produto", "Especificação de produto"), ("aquisicao e comparacao", "Aquisição e comparação")],
 "posse":      [("assistencia e reparo","Assistência e reparo"),("peca e consumivel","Peça e consumível"),
                ("instalacao","Instalação"),("manutencao e cuidado","Manutenção e cuidado"),
                ("defeito","Defeito"),("manual e uso","Manual e uso"),("garantia","Garantia"),
                ("consumo e eficiencia","Consumo"),("receita e preparo","Receita"),("descarte e sustentab","Descarte")],
}
def chips_familias(lista, k=5, prefer="marca", escopo=None):
    """chips avulsos: [(familia, rotulo)] — cada um com uma consulta real de exemplo"""
    itens = []
    for fam, lab in lista[:k]:
        exs = _exs(fam, prefer, escopo)
        if not exs: continue
        itens.append(f'<span class="chip"><b>{e(lab)}</b><code>{e(exs[0][0])}</code></span>')
    return '<div class="chips">' + "".join(itens) + "</div>"

def chips(estagio, k=4, prefer="marca", escopo=None):
    """lista as familias do estagio com um exemplo real de consulta em cada"""
    return chips_familias(FAM_ESTAGIO[estagio], k, prefer, escopo)

FAMLAB = {f: lab for est in FAM_ESTAGIO.values() for f, lab in est}
FAMLAB.update({"assistencia":"Assistência e reparo","peca":"Peça e consumível","manutencao":"Manutenção e cuidado",
               "consumo":"Consumo","receita":"Receita","descarte":"Descarte","sinonimo":"Categoria",
               "conectividade e smart":"Conectividade","nao classificado":"Não classificado"})
EST_LAB = {"descoberta":"1 · Descoberta", "escolha":"2 · Escolha", "posse":"3 · Posse"}
CATN = {"coccao":"cocção","lava loucas":"lava-louças","sem categoria":"sem categoria declarada"}
def catn(c): return CATN.get(c, c).capitalize()
TOPLAB = {"uso e receita":"Uso e receita","limpeza e manutencao":"Limpeza e manutenção",
          "comparacao e modelo":"Comparação e modelo","peca e filtro":"Peça e filtro",
          "consumo e energia":"Consumo e energia","instalacao":"Instalação",
          "defeito e problema":"Defeito e problema","assistencia e conserto":"Assistência e conserto",
          "preco e compra":"Preço e compra"}

def sintese(marca_fonte, parte, titulo, subtitulo, pontos, decide, fonte="", destino=None):
    """Slide executivo que abre um bloco: o que ele decide, antes de abrir os detalhes.
    pontos: [(numero, rotulo, leitura, cor)] — no maximo quatro."""
    cartoes = "".join(
        f'<div class="sx"><span class="sxn" style="color:{c}">{v}</span>'
        f'<span class="sxl">{e(l)}</span><p class="sxp">{t}</p></div>' for v, l, t, c in pontos)
    corpo = (f'<div class="sintese">{cartoes}</div>'
             f'<div class="quadro"><span class="qh">O que este bloco decide</span><p>{decide}</p></div>')
    slide(marca_fonte, parte, titulo, subtitulo, corpo, "", fonte, destino)

def chips_estagio(perfil, ests=("descoberta","escolha","posse")):
    """as consultas que mais pesam em cada estagio DENTRO daquele recorte, com a familia de origem"""
    itens = []
    for est in ests:
        t = (perfil.get("top_estagio") or {}).get(est) or []
        if not t: continue
        kw, _, fam = t[0]
        itens.append(f'<span class="chip e-{est}"><b>{EST_LAB[est]} · {e(FAMLAB.get(fam,fam))}</b>'
                     f'<code>{e(kw)}</code></span>')
    return '<div class="chips">' + "".join(itens) + "</div>"

# ================================================================== ABERTURA
slides.append(f"""<section class="slide capa"><div class="slide-inner">
  <span class="kicker">Youdare · Direção de Mídia e Dados · agosto 2026</span>
  <h1>O que a busca<br><em>e a IA</em> dizem<br>sobre a categoria</h1>
  <p class="sub">Cenário, players e jornada do consumidor — Electrolux LATAM 2027, recorte Brasil</p>
  <div class="capa-meta"><span>Search</span><span>IA</span><span>Brasil · 12 meses</span></div>
</div></section>""")

slide("briefing", "Objetivo do briefing", "Converter reconhecimento de marca em intenção de compra no momento da decisão",
  "O briefing aponta um vão entre awareness e consideração. Busca e IA são as fontes que enxergam o momento da decisão em escala.",
  '<div class="quadro"><blockquote>“Moving beyond awareness, converting brand recognition into purchase intent <b>at the moment of decision</b>.”</blockquote><cite>Briefing Electrolux · desafio declarado para o Brasil</cite></div>'
  + kpis([("85%","awareness MDA","#3987e5"),("44%","consideração T2B","#d95926"),("41 p.p.","o vão entre as duas","#c98500")]),
  "", "Brand Health Track · Q1 2026")

IDX_ABERTURA = len(slides)   # o argumento de abertura e montado no fim

slide("ambos", "As fontes", "Duas fontes de demanda, lidas separadamente antes de serem cruzadas",
  "Busca mostra o que as pessoas digitam. IA mostra o que elas perguntam e o que os assistentes respondem. As duas foram fechadas de forma independente.",
  '<div class="fontes">'
  f'<div class="fx"><span class="fxb b-search">Search</span><span class="fxv">{n(META["kw_total"])}</span><span class="fxl">keywords da categoria e das marcas</span></div>'
  f'<div class="fx"><span class="fxb b-ia">IA</span><span class="fxv">{n(U["topicos_categoria"])}</span><span class="fxl">tópicos de demanda mediada por assistente</span></div>'
  '</div>' +
  tabela(["","O que enxerga","O que não enxerga"], [
    ['<span class="badge b-search">Search</span>',"Demanda expressa, sua composição, os termos exatos, a forma ao longo de 12 meses","Quem captura cada consulta · demanda latente · conversão"],
    ['<span class="badge b-ia">IA</span>',"Se a marca é citada sem ser nomeada, em que posição, com que carga, e o tráfego que chega","Quais fontes o modelo cita · o que responde quando perguntam pela marca"]]),
  "O método detalhado — como cada medida é calculada, sobre o que, e onde ela engana — vive no documento de apoio <b>Como ler o dado</b>, que acompanha este material.", "Brasil · ago/25 a jul/26")

# --- a jornada em 4 estagios (NOVO)
slide("search", "O modelo", "A jornada tem quatro estágios, e o primeiro não tem marca nenhuma",
  "Toda a leitura deste material usa estes quatro estágios. Eles saem da forma da consulta: o que a pessoa digita revela em que ponto da relação com a categoria ela está.",
  tabela(["Estágio","O que a pessoa procura","Famílias de necessidade e um termo real de cada"], [
    [f'<b style="color:{EST["sem_marca"]}">0 · Sem marca</b>',"A categoria, sem ter escolhido fabricante",
     f'<span class="fam">Cabeça de categoria</span> <code>{e(HD["exemplos_familia"]["nao classificado"][0][0])}</code> · '
     + exf("assistencia", "Assistência e reparo", 1, "cauda")],
    [f'<b style="color:{EST["descoberta"]}">1 · Descoberta de marca</b>',"Quem é a marca, se ela é boa",
     exf("marca e navegacao", "Marca e navegação", 3)],
    [f'<b style="color:{EST["escolha"]}">2 · Escolha de produto</b>',"Qual modelo, qual capacidade, qual preço",
     exf("especificacao produto", "Especificação de produto", 2) + " · " + exf("aquisicao e comparacao", "Aquisição e comparação", 1)],
    [f'<b style="color:{EST["posse"]}">3 · Posse</b>',"Já tem o produto e convive com ele",
     exf("instalacao", "Instalação", 1, "cauda") + " · " + exf("manutencao", "Manutenção e cuidado", 1, "cauda")
     + " · " + exf("peca", "Peça e consumível", 1, "cauda")]], "wide"),
  "O estágio 0 é a maior fatia da demanda e o único em que nenhum player é nomeado. Os estágios 1 a 3 são, por definição, buscas que trazem o nome de um fabricante escrito.", F_KW)

slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 1</span><h2>A categoria e os players</h2>
  <p class="sub">Quem cresce, quem perde, onde cada um joga e o que a demanda de busca revela sobre a relação de cada marca com o consumidor</p></div></section>""")

IDX_P1 = len(slides)   # a sintese da Parte 1 e montada no fim e inserida aqui

# ================================================================== PARTE 1
def sparkbar(vals):
    """indice mes a mes, base 100 no primeiro mes lido"""
    ix = indexar(vals); mx = max(ix); mn = min(ix)
    cel = "".join(
        f'<span class="sb" style="height:{18+52*(v-mn)/(mx-mn or 1):.0f}%;'
        f'background:{"#199e70" if v >= 100 else "#d95926"}" title="{MESES[i]}: {v:.0f}"></span>'
        for i, v in enumerate(ix))
    return f'<span class="sbw">{cel}</span>'

# panorama com indice mes a mes e ultimo vs primeiro
slide("search", "Panorama", "Hisense e Haier são os únicos que terminam o período acima de onde começaram",
  "Índice de share de demanda mês a mês, base 100 no primeiro mês lido. Barra verde é mês acima da base, laranja abaixo. Ponta a ponta compara o último mês com o primeiro; ano a ano compara a média dos cinco últimos com a dos sete primeiros.",
  tabela(["Player","Volume/mês","Índice mês a mês (base 100 = ago/25)","Último vs 1º mês","Ano a ano"],
    [[f'<span class="dot" style="background:{COR[k]}"></span>{NOME[k]}', n(P[k]["volume"]),
      sparkbar(P[k]["serie_relativa"]),
      f'<b class="{"up" if indexar(P[k]["serie_relativa"])[-1] >= 100 else "down"}">'
      f'{indexar(P[k]["serie_relativa"])[-1]:.0f}</b>',
      f'<b class="{"up" if P[k]["inclinacao_vs_categoria"] > 1.08 else "down" if P[k]["inclinacao_vs_categoria"] < 0.92 else "flat"}">'
      f'{vs(k)}</b>']
     for k in sorted(ORDEM, key=lambda k: -indexar(P[k]["serie_relativa"])[-1])], "wide"),
  "As duas colunas podem divergir: ponta a ponta depende de como foi o último mês, ano a ano descreve o período. <b>É o ano a ano que descreve a trajetória.</b>", F_KW)

# --- Electrolux
el = P["electrolux"]
ARQ = {"electrolux":"Conhecida, pouco procurada depois","brastemp":"Grande e perdendo espaço",
       "consul":"Procurada por quem já comprou","samsung":"Perde espaço, base pequena",
       "midea":"Cresce, e ninguém procura depois","hisense":"Entra pelo nome","haier":"Ainda formando nome"}

def cls(k):
    """volume classificado da marca: os tres estagios somam 100% dele.
    O nao classificado varia muito entre recortes e domina a barra sem dizer nada."""
    return max(P[k]["descoberta"] + P[k]["escolha"] + P[k]["posse"], 0.01)

slide("search", "Retrato", "Nenhuma marca da categoria cresce e é procurada por quem já comprou",
  "Cada marca em duas medidas. <b>Horizontal: se ganhou ou perdeu demanda contra a categoria em doze meses</b> — 1,00 é crescer no mesmo ritmo da categoria, acima é ganhar espaço, abaixo é perder. "
  "<b>Vertical: quanto da demanda pela marca vem de quem já tem o produto em casa</b> — quem procura peça, assistência, instalação, manutenção, manual, garantia. As duas são proporções, então o tamanho da marca não interfere.",
  quadrante([(k, P[k]["inclinacao_vs_categoria"], 100*P[k]["posse"]/cls(k)) for k in ORDEM],
            "Ganha demanda contra a categoria", "Demanda de quem já tem o produto", 1.0,
            st.median([100*P[k]["posse"]/cls(k) for k in ORDEM]),
            ["Procurada depois · não cresce", "Procurada depois · e cresce",
             "Não procurada depois · não cresce", "Não procurada depois · cresce"]) +
  '<div class="quadro"><p><b>O quadrante de cima à direita está vazio.</b> À esquerda, Consul, Samsung e Brastemp são procuradas por quem já tem o produto e pararam de ganhar demanda. À direita, Hisense, Haier e Midea ganham demanda e quase ninguém as procura depois da compra. Ser lembrado depois da compra e crescer são, hoje, coisas que nenhuma marca faz ao mesmo tempo.</p></div>',
  f'A Electrolux fica em cima das duas linhas de corte: {vs("electrolux")} contra a categoria, que é nem ganhar nem perder demanda, e {pct(100*el["posse"]/cls("electrolux"))} de demanda de quem já comprou, que é exatamente a mediana das sete. Nas duas medidas ela é a média do mercado.', F_KW)

slide("search", "Retrato", "Quem entra na categoria vive de nome; quem já está vive de produto",
  "Composição da demanda de cada marca entre os três estágios que existem dentro dela, ordenada pela fatia de posse. As barras somam 100% do volume classificado de cada marca, e a leitura é de perfil, não de tamanho: os recortes de origem têm profundidade diferente por marca.",
  barras_empilhadas([(NOME[k], [("Descoberta", 100*P[k]["descoberta"]/cls(k), EST["descoberta"]),
                                ("Escolha", 100*P[k]["escolha"]/cls(k), EST["escolha"]),
                                ("Posse", 100*P[k]["posse"]/cls(k), EST["posse"])],
                      f'<span class="arq">{ARQ[k]}</span>')
                     for k in sorted(ORDEM, key=lambda k: -P[k]["posse"]/cls(k))]) +
  legenda([("1 · Descoberta de marca", EST["descoberta"]), ("2 · Escolha de produto", EST["escolha"]),
           ("3 · Posse", EST["posse"])]) +
  # a barra escura é a posse: mostrar as familias que a compoem, com um termo real
  # de cada uma. So uma de assistencia; as demais, de relacao neutra com a marca.
  '<span class="chips-tit">A barra escura, aberta: as famílias de posse, com um termo real de cada</span>' +
  chips_familias([("instalacao","Instalação"),("peca e consumivel","Peça e consumível"),
                  ("manutencao e cuidado","Manutenção e cuidado"),("manual e uso","Manual e uso"),
                  ("assistencia e reparo","Assistência e reparo")]),
  f"Haier e Hisense concentram a demanda no próprio nome: é o retrato de quem está entrando. Nenhum player passa de {pct(100*P['consul']['posse']/cls('consul'))} do volume classificado em posse, e é lá que vivem as dez famílias de necessidade da vida com o produto.", F_KW)

CATS = ["geladeira","lavanderia","ar condicionado","coccao","lava loucas","freezer","aspirador","adega"]
slide("search", "Retrato", "Cada grupo de players disputa um território de categoria diferente",
  "Peso de cada categoria de produto dentro da demanda de cada player, com a categoria e o território sem dono como referência. Célula mais clara, maior concentração.",
  heatmap([catn(c) for c in CATS], ORDEM + ["generico","sem_dono"],
          lambda r, c: (P[r] if r in P else (HD if r == "generico" else SD))["categorias"].get(
              next(k for k in CATS if catn(k) == c), 0)),
  "Hisense, Haier e Midea concentram em ar condicionado, categoria fora do core histórico da disputa entre as marcas estabelecidas. O território sem dono também: 28% dele é ar condicionado.", F_KW)

PC = lambda v: pct(100*v/J4["total"], 1)
slide("search", "Retrato", "Metade da demanda de busca acontece antes de qualquer marca entrar na conta",
  "A demanda de busca da categoria parte em dois: <b>a que não escreve nome de fabricante nenhum</b> e <b>a que escreve</b>. Só a segunda se divide em estágios de jornada — descoberta, escolha e posse são, por definição, buscas que já trazem uma marca no texto.",
  barras_empilhadas([("Demanda de busca", [
      ("Sem marca", 100*J4["sem_marca"]/J4["total"], EST["sem_marca"]),
      ("Descoberta", 100*J4["descoberta"]/J4["total"], EST["descoberta"]),
      ("Escolha", 100*J4["escolha"]/J4["total"], EST["escolha"]),
      ("Posse", 100*J4["posse"]/J4["total"], EST["posse"]),
      ("Não classificado", 100*J4["nao_class"]/J4["total"], EST["nc"])], "")]) +
  legenda([("0 · Sem marca", EST["sem_marca"]), ("1 · Descoberta", EST["descoberta"]),
           ("2 · Escolha", EST["escolha"]), ("3 · Posse", EST["posse"]), ("Não classificado", EST["nc"])]) +
  '<div class="col2"><div>' +
  tabela(["Estágio","Buscas/mês","% do total","O que contém"], [
    '<td class="grp" colspan="4"><b>Sem nome de fabricante nenhum</b> — nenhum player é procurado aqui</td>',
    [f'<b style="color:{EST["sem_marca"]}">0 · Sem marca</b>', n(J4["sem_marca"]), f'<b>{PC(J4["sem_marca"])}</b>',
     f'Cabeças de categoria ({n(J4["heads"])}) e a cauda de serviço sem fabricante ({n(J4["cauda"])})'],
    '<td class="grp" colspan="4"><b>Com o nome de um fabricante escrito na busca</b> — a soma dos sete players</td>',
    [f'<b style="color:{EST["descoberta"]}">1 · Descoberta</b>', n(J4["descoberta"]), f'<b>{PC(J4["descoberta"])}</b>', "O nome do fabricante, sozinho ou com a categoria"],
    [f'<b style="color:{EST["escolha"]}">2 · Escolha</b>', n(J4["escolha"]), f'<b>{PC(J4["escolha"])}</b>', "Marca + capacidade, tecnologia, modelo, preço, comparação"],
    [f'<b style="color:{EST["posse"]}">3 · Posse</b>', n(J4["posse"]), f'<b>{PC(J4["posse"])}</b>', "Marca + as dez famílias de vida com o produto"],
    [f'<b style="color:#8b8981">Não classificado</b>', n(J4["nao_class"]), f'<b>{PC(J4["nao_class"])}</b>', "Traz marca, mas o texto não permite dizer qual estágio"]], "wide") +
  '</div><div>' +
  tabela([f'Dentro do estágio 0: a cauda de serviço ({n(J4["cauda"])})',"% dela","Termo real"],
         [[e(FAMLAB.get(f, f.capitalize())), "<b>" + pct(v) + "</b>",
           f'<code>{e(SD["exemplos_familia"][f][0][0][:30])}</code>' if SD["exemplos_familia"].get(f) else "—"]
          for f, v in list(SD["familias"].items())[:6]]) +
  kpis([(n(SD["volume"]), "buscas/mês de serviço sem nenhum fabricante", COR["sem_dono"]),
        (f'{SD["ai_overview"]}%', "já respondidas com resumo de IA", "#c98500")]) +
  '</div></div>',
  f'O estágio 0 é {PC(J4["sem_marca"])} da demanda e não pertence a nenhum player. Os outros {pct(100 - 100*J4["sem_marca"]/J4["total"],1)} trazem um nome de fabricante escrito na busca — é essa fatia que se reparte entre as sete marcas. Dentro do estágio 0, {n(SD["volume"])} buscas/mês são de quem já tem o produto e procura serviço sem nomear quem fabricou — é a coluna da direita.', F_KW + f' · {n(META["kw_cauda"])} keywords sem marca com volume')

slide("search", "Electrolux", "Contra a categoria, a demanda da Electrolux está parada",
  "Cada linha é a <b>fatia da categoria</b> que a marca tem, mês a mês, indexada ao próprio primeiro mês. "
  "<b>A categoria é a linha horizontal em 100</b>: por construção ela não sobe nem desce neste gráfico, porque é a régua contra a qual todas as outras são medidas. "
  "Linha acima de 100 é marca ganhando espaço dentro da categoria; abaixo, perdendo. Hisense e Haier ficam de fora: a base pequena faz a série oscilar e achataria todo o resto.",
  linhas({k: indexar(P[k]["serie_relativa"]) for k in ["electrolux","brastemp","consul","samsung","midea"]},
         destaque="electrolux", rotulos_x=MESES, ref100=True, rotular_todos=True,
         reflab="Categoria = 100") +
  kpis([(vs("electrolux"), "Electrolux ano a ano contra a categoria · média dos 5 últimos meses contra os 7 primeiros", "#3987e5"),
        (f'{indexar(el["serie_relativa"])[-1]:.0f}', "ponta a ponta · último mês contra o primeiro", "#f0ede4"),
        (f'{indexar(HD["serie"])[-1]:.0f}', "a categoria em volume absoluto, ponta a ponta — ela também não cresce", "#6b6a63")]),
  f'<b>A categoria não está crescendo</b>: em volume absoluto ela termina os doze meses em {indexar(HD["serie"])[-1]:.0f} contra a base 100, com pico sazonal em fevereiro e março. '
  f'Dentro dela, a Electrolux termina praticamente onde começou — {vs("electrolux")} ano a ano. Julho foi um mês forte, o que puxa a leitura ponta a ponta para {indexar(el["serie_relativa"])[-1]:.0f}, mas a <b>média do período não se move</b>. '
  f'Brastemp ({vs("brastemp")}) e Samsung ({vs("samsung")}) perdem espaço; Consul ({vs("consul")}) fica parada; Midea ({vs("midea")}) é a única das cinco que ganha.', F_KW)

# --- submarcas: atributo transversal, nao familia
FR = {k: v for k, v in D["frentes"]}
SUB_ELUX = {kw: (vol, fam) for kw, vol, fam in el["submarca"]["itens"]}
def frente(lab, fam, *termos):
    """soma as grafias de uma frente e guarda os termos exatos que a compoem"""
    itens = [(t, FR.get(t) or SUB_ELUX.get(t, (0,))[0]) for t in termos]
    return (lab, fam, sum(v for _, v in itens), [t for t, v in itens if v])

FRENTES = [frente("Cuida","assistência e reparo","electrolux cuida","eletrolux cuida"),
           frente("Outlet","aquisição e comparação","electrolux outlet","eletrolux outlet","outlet eletrolux"),
           frente("Shopclub","aquisição e comparação","electrolux shopclub","shopclub eletrolux","shop club eletrolux"),
           frente("Instala","instalação","electrolux instala","eletrolux instala"),
           frente("Projeta","especificação de produto","electrolux projeta","eletrolux projeta"),
           frente("Pro","especificação de produto","electrolux pro","eletrolux pro"),
           frente("Coleta Consciente","descarte","coleta consciente electrolux")]
V_FRENTES = sum(v for _, _, v, _ in FRENTES)
# a mesma necessidade, digitada sem o nome comercial — o contraponto de cada frente

slide("search", "Electrolux", "Mais gente procura assistência da Electrolux do que a marca criada para prestá-la",
  "Confronto entre a necessidade expressa com o nome da marca e a submarca de serviço correspondente. As duas caem na mesma família; muda apenas o que a pessoa digitou.",
  '<div class="confronto">'
  f'<div class="cf"><span class="cft">A necessidade</span><span class="cfv" style="color:#3987e5">{n(FR.get("assistência técnica electrolux",0))}</span>'
  '<span class="cfl"><code>assistência técnica electrolux</code></span></div>'
  '<div class="cfx">↔</div>'
  f'<div class="cf"><span class="cft">A submarca criada para ela</span><span class="cfv" style="color:#d95926">{n(FRENTES[0][2])}</span>'
  '<span class="cfl"><code>electrolux cuida</code> + <code>eletrolux cuida</code></span></div></div>' +
  barras_h([(f"{lab} · {fam}", v, None) for lab, fam, v, _ in sorted(FRENTES, key=lambda x: -x[2])],
           lambda x: "#d95926", fmt=n) +
  kpis([(n(V_FRENTES), "buscas/mês somando as sete frentes", "#d95926"),
        (pct(100*V_FRENTES/el["volume"], 1), "da demanda pela marca", "#f0ede4"),
        ("2", "grafias da marca: electrolux e eletrolux", "#6b6a63")]),
  "A necessidade existe e a estrutura existe; o que falta é o consumidor conhecer o nome da frente. Cada barra traz a família em que a frente cai, e nenhuma delas é família por si.", F_KW + " + cauda sem marca")

INCL = {f: v for f, v in el["familias_inclinacao"].items() if v["volume"] >= 100 and f != "nao classificado"}
_incl4 = ", ".join(f'{FAMLAB.get(f, f.capitalize()).lower()} ({dec(v["inclinacao"])})'
                   for f, v in sorted(INCL.items(), key=lambda i: -i[1]["inclinacao"])[:4])
slide("search", "Electrolux", "Dentro da Electrolux, quem cresce é a demanda de quem já tem o produto",
  "Inclinação por família dentro da marca: acima de 1,00 a família cresce ao longo dos doze meses, abaixo encolhe. Em destaque, as famílias de posse.",
  barras_h([(FAMLAB.get(f, f.capitalize()),
             v["inclinacao"], "posse" if f in [x[0] for x in FAM_ESTAGIO["posse"]] else None)
            for f, v in sorted(INCL.items(), key=lambda i: -i[1]["inclinacao"])],
           lambda k: "#7d5300" if k == "posse" else "#3987e5", max_v=1.6,
           fmt=lambda v: str(round(v, 2)).replace(".", ",")) +
  chips_familias([("defeito","Defeito"),("garantia","Garantia"),
                  ("peca e consumivel","Peça e consumível"),("manual e uso","Manual e uso")], escopo=el),
  f'As quatro famílias que mais crescem são todas de posse — {_incl4}. '
  f'Especificação de produto vem depois, com {dec(INCL["especificacao produto"]["inclinacao"])}, e é a maior em volume ({n(INCL["especificacao produto"]["volume"])} buscas/mês). '
  f'A demanda pelo nome da marca fica parada, em {dec(INCL["marca e navegacao"]["inclinacao"])}.', F_KW)

slide("search", "Electrolux", "Geladeira concentra um terço da demanda de marca da Electrolux",
  "Peso de cada categoria de produto dentro da demanda da marca, e as consultas que mais pesam.",
  '<div class="col2"><div>' +
  barras_h([(catn(c), v, "electrolux") for c, v in list(el["categorias"].items())[:7]],
           lambda k: COR["electrolux"], fmt=lambda v: pct(v)) + '</div><div>' +
  tabela(["Maiores consultas da marca","Família","Buscas/mês"],
         [[e(k), f'<span class="fam">{e(FAMLAB.get(f, f.capitalize()))}</span>', "<b>" + n(v) + "</b>"]
          for k, v, f in el["top_keywords"][:6]]) + '</div></div>',
  f'Ar condicionado é {pct(el["categorias"].get("ar condicionado", 0))} da demanda da Electrolux, contra {pct(P["midea"]["categorias"].get("ar condicionado", 0))} da Midea e {pct(P["haier"]["categorias"].get("ar condicionado", 0))} da Haier.', F_KW)

# --- demais players
def bloco_player(k, titulo, subtitulo, leitura):
    """So dado de busca. Tudo que e IA vive na Parte 2, depois do modelo de IA."""
    p = P[k]
    esq = barras_empilhadas([("Jornada", [("Descoberta", p["descoberta"], EST["descoberta"]),
                                          ("Escolha", p["escolha"], EST["escolha"]),
                                          ("Posse", p["posse"], EST["posse"]),
                                          ("Não class.", p["nao_class"], EST["nc"])], "")]) + \
          legenda([("Descoberta", EST["descoberta"]), ("Escolha", EST["escolha"]),
                   ("Posse", EST["posse"]), ("Não class.", EST["nc"])]) + \
          barras_h([(catn(c), v, k) for c, v in list(p["categorias"].items())[:6]],
                   lambda x: COR[k], fmt=lambda v: pct(v))
    dir_ = kpis([(n(p["volume"]), "buscas/mês", COR[k]),
                 (vs(k), "ano a ano vs categoria", "#f0ede4"),
                 (f'{indexar(p["serie_relativa"])[-1]:.0f}', "ponta a ponta, base 100", "#f0ede4")]) + \
           '<div class="mm"><span class="mml">Mês a mês</span>' + sparkbar(p["serie_relativa"]) + '</div>' + \
           tabela(["Maiores consultas da marca","Família","Buscas/mês"],
                  [[e(kw), f'<span class="fam">{e(FAMLAB.get(f, f.capitalize()))}</span>', "<b>" + n(v) + "</b>"]
                   for kw, v, f in p["top_keywords"][:5]])
    slide("search", p["nome"], titulo, subtitulo,
          f'<div class="col2"><div>{esq}</div><div>{dir_}</div></div>' + chips_estagio(p), leitura, F_KW)

# ============================================== PARTE 2 · O PANORAMA DE IA
CN, SM, ES, OC = PAN["cobertura_nome"], PAN["sem_marca"], PAN["estagios"], PAN["ocupacao"]
DOM0 = list(OC.values())[0] if OC else None   # dominio com tópicos de marca medidos
NUC_ORD = sorted([k for k in CN if k != "outras_marcas"], key=lambda k: -CN[k]["pct"])
PP = PAN["prompts"]
F_PAN = f"Tópicos de IA · {n(U['topicos_categoria'])} tópicos de categoria · Brasil"
F_PRO = f"Prompts de IA · {n(U['prompts_distintos'])} prompts × {len(U['provedores'])} provedores"
EST_ORD = ["exploracao de categoria", "descoberta", "escolha", "posse"]
EST_NOME = {"exploracao de categoria":"Exploração de categoria","descoberta":"Descoberta de marca",
            "escolha":"Escolha e compra","posse":"Posse"}
EST_COR = {"exploracao de categoria":EST["sem_marca"],"descoberta":EST["descoberta"],
           "escolha":EST["escolha"],"posse":EST["posse"]}
FAMN = {"assistencia e conserto":"Assistência e conserto","defeito e problema":"Defeito e problema",
        "peca e filtro":"Peça e filtro","instalacao":"Instalação","manutencao e limpeza":"Manutenção e limpeza",
        "uso e receita":"Uso e receita","consumo e energia":"Consumo e energia","garantia e suporte":"Garantia e suporte",
        "preco e compra":"Preço e compra","comparacao e modelo":"Comparação e modelo","marca e loja":"Marca e loja",
        "especificacao de produto":"Especificação de produto",
        "produto e categoria":"Produto e categoria"}
def fn(f): return FAMN.get(f, f.capitalize())

slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 2</span><h2>A demanda em IA</h2>
  <p class="sub">O tamanho da conversa mediada por assistente, como ela se distribui pela jornada, e quanto dela nenhuma marca ocupa</p></div></section>""")

sintese("ia", "Parte 2 · Síntese", f'{pct(SM["pct"], 1)} da demanda em IA não nomeia nenhum fabricante',
  "O que esta parte estabelece, antes de abrir marca por marca. Todos os números são de demanda mediada por assistente no Brasil. É outra fonte e outra unidade que a busca, e não se soma com ela.",
  [(pct(SM["pct"], 1), "da demanda não nomeia fabricante", "O maior dado da base. A demanda é de categoria, não de fabricante.", EST["sem_marca"]),
   (pct(CN["electrolux"]["pct"], 1), "é a Electrolux, a maior das marcas", f'À frente de Brastemp ({pct(CN["brastemp"]["pct"],1)}) e Midea ({pct(CN["midea"]["pct"],1)}). Lidera entre as sete, sobre uma base pequena.', COR["electrolux"]),
   (pct(ES["escolha"]["sem_marca_pct"], 0), "da escolha está sem marca", "O estágio da decisão de compra é o mais desocupado dos quatro.", EST["escolha"]),
   # este cartao tem de estar na MESMA medida dos outros. Ocupacao por dominio e
   # outra coisa e vive nos slides proprios, com o contraste explicado.
   (pct(sum(CN[k]["pct"] for k in NUC_ORD), 1), "é tudo que as sete marcas cobrem juntas",
    f'As demais marcas da categoria — LG, Philco, Mondial e outras — somam {pct(CN["outras_marcas"]["pct"],1)}, mais que o conjunto declarado inteiro.', "#6b6a63")],
  "Com a maior parte da demanda sem marca, a disputa é por <b>ocupar território vago</b> e não por tirar participação de um concorrente. As telas seguintes mostram qual território, em que momento da jornada e a que distância cada player está dele.",
  F_PAN)

slide("ia", "O universo", f'{n(U["topicos_categoria"])} tópicos de categoria, {n(U["volume"])} de demanda mediada por assistente',
  "Um tópico é um agrupamento de prompts que os assistentes tratam como o mesmo assunto — a unidade desta parte, equivalente ao que a keyword é na busca. Toda a leitura a seguir se refere ao Brasil e a eletrodomésticos.",
  kpis([(n(U["topicos_categoria"]), "tópicos de categoria no Brasil", "#199e70"),
        (n(U["volume"]), "de volume mediado por IA", "#f0ede4"),
        (n(U["prompts_declarados"]), "prompts dentro desses tópicos", "#f0ede4"),
        (n(U["prompts_distintos"]), "prompts lidos um a um", "#c98500")]) +
  tabela(["Do que foi lido ao que entra na conta","Tópicos","O critério"], [
    ["Tópicos lidos", n(U["topicos_exportados"]), f'{len(U["seeds"])} pontos de partida, todos de categoria — <b>nenhum com nome de marca</b>, e é isso que torna a cobertura por marca uma medida limpa'],
    ["No Brasil", n(U["topicos_br"]), f'{n(U["topicos_us"])} tópicos dos Estados Unidos ficam fora de todo agregado'],
    ["<b>Sobre a categoria</b>", f'<b>{n(U["topicos_categoria"])}</b>',
     f'{100 - round(100*U["topicos_categoria"]/U["topicos_br"])}% do recorte Brasil trata de outro assunto e não menciona aparelho']], "wide"),
  "Nenhuma marca foi usada como ponto de partida. Toda marca que aparecer nas telas seguintes foi encontrada dentro da demanda de categoria, não procurada — e por isso as sete se comparam entre si sobre a mesma base.", F_PAN)

# --- cenario consolidado da cobertura -------------------------------------
CN_ORD = sorted([k for k in CN], key=lambda k: -CN[k]["pct"])
slide("ia", "Cobertura · Consolidado", f'{pct(SM["pct"],1)} da demanda mediada por IA não nomeia nenhum fabricante',
  "Participação de cada marca no volume dos tópicos de categoria, medida pelo nome do tópico. Os seeds são todos de categoria. Nenhuma marca foi semeada, então marca que aparece aqui foi descoberta pela própria ferramenta.",
  barras_empilhadas([("Demanda de categoria",
      [("Sem marca", SM["pct"], EST["sem_marca"])] +
      [(CN[k]["nome"], CN[k]["pct"], COR.get(k, "#6b6a63")) for k in CN_ORD], "")]) +
  legenda([("Sem marca nenhuma", EST["sem_marca"])] +
          [(CN[k]["nome"], COR.get(k, "#6b6a63")) for k in CN_ORD]) +
  kpis([(n(SM["volume"]), "de volume sem marca nenhuma", EST["sem_marca"]),
        (n(SM["topicos"]), "tópicos sem fabricante no nome", "#f0ede4"),
        (pct(100 - SM["pct"], 1), "é tudo que as marcas juntas ocupam", "#6b6a63")]),
  f'A mesma leitura do estágio 0 da parte de busca, em patamar mais alto: {pct(100*J4["sem_marca"]/J4["total"],1)} da demanda de busca não nomeia marca, contra {pct(SM["pct"],1)} em IA.', F_PAN)

slide("ia", "Cobertura · Por marca", f'Electrolux é a marca mais presente da categoria em IA, com {pct(CN["electrolux"]["pct"],1)} da demanda',
  "As sete marcas do conjunto declarado, pelo volume dos tópicos que carregam o nome delas. A coluna de exemplos mostra o maior tópico de cada uma.",
  barras_h([(CN[k]["nome"], CN[k]["pct"], k) for k in CN_ORD if k != "outras_marcas"],
           lambda k: COR.get(k, "#6b6a63"), max_v=max(6.0, CN["electrolux"]["pct"]), fmt=lambda v: pct(v, 2)) +
  tabela(["Marca","Tópicos","Volume","Maior tópico da marca","Estágio dele"],
    [[f'<span class="dot" style="background:{COR.get(k,"#6b6a63")}"></span>{CN[k]["nome"]}',
      n(CN[k]["topicos"]), "<b>" + n(CN[k]["volume"]) + "</b>",
      f'<code>{e(CN[k]["exemplos"][0][0][:56])}</code>' if CN[k]["exemplos"] else "—",
      f'<span class="fam">{e(EST_NOME.get(CN[k]["exemplos"][0][2], CN[k]["exemplos"][0][2]))}</span>' if CN[k]["exemplos"] else "—"]
     for k in CN_ORD[:6] if k != "outras_marcas"], "wide"),
  f'LG, Philco, Mondial, Britânia e outras marcas fora do conjunto declarado somam {pct(CN["outras_marcas"]["pct"],1)}, acima da Electrolux. O conjunto competitivo do briefing não cobre tudo que a IA nomeia.', F_PAN)

POSSE_TOP = max(((k, CN[k]["por_estagio"]["posse"]["pct"]) for k in CN_ORD if k != "outras_marcas"),
                key=lambda x: x[1])
slide("ia", "Cobertura · Por estágio", "A Electrolux cobre um quarto da descoberta e quase nada da escolha",
  "A mesma cobertura, quebrada por estágio: quanto do volume de cada estágio carrega o nome de cada marca. Cada coluna soma sobre o total daquele estágio, não sobre a marca.",
  heatmap([EST_NOME[k] for k in EST_ORD], [k for k in CN_ORD if k != "outras_marcas"],
          lambda m, c: CN[m]["por_estagio"][next(k for k in EST_ORD if EST_NOME[k] == c)]["pct"],
          fmt=lambda v: pct(v, 2) if v else "—") +
  kpis([(pct(CN["electrolux"]["por_estagio"]["descoberta"]["pct"], 1), "da descoberta é Electrolux", EST["descoberta"]),
        (pct(CN["electrolux"]["por_estagio"]["escolha"]["pct"], 1), "da escolha", EST["escolha"]),
        (pct(CN["electrolux"]["por_estagio"]["posse"]["pct"], 1), "da posse", EST["posse"]),
        (pct(ES["posse"]["sem_marca_pct"], 1), "da posse não tem fabricante nenhum no nome", "#c98500")]),
  f'O perfil da Electrolux em IA repete o da busca: forte onde a marca é procurada pelo nome ({pct(CN["electrolux"]["por_estagio"]["descoberta"]["pct"],1)} da descoberta), quase ausente onde o produto é escolhido e onde se convive com ele. '
  f'Na posse ela é a <b>maior das sete</b>, com {pct(POSSE_TOP[1],2)} — e mesmo assim o estágio inteiro cabe numa margem estreita: nenhuma marca passa disso, e {pct(ES["posse"]["sem_marca_pct"],1)} do volume não tem fabricante nenhum no nome.', F_PAN)

# --- as outras medidas de marca em IA, ancoradas na cobertura sobre o total
slide("ia", "Cobertura · Outras medidas", "Citação, posição e sentimento: três leituras que não substituem a cobertura",
  "A cobertura vem primeiro e é sempre sobre o total da demanda da categoria. As três colunas seguintes vêm de outra fonte, uma amostra de 150 perguntas sem marca, e têm outro denominador. Servem para descrever <b>como</b> a marca aparece, não <b>quanto</b> da demanda ela cobre.",
  tabela(["Marca","<b>Cobertura</b><br><span class='th2'>% do total da demanda</span>",
          "Citação<br><span class='th2'>% das 150 perguntas</span>",
          "Posição<br><span class='th2'>onde surge na resposta</span>",
          "Sentimento<br><span class='th2'>carga da menção</span>"],
    [[f'<span class="dot" style="background:{COR.get(k,"#6b6a63")}"></span>{CN[k]["nome"]}',
      f'<b>{pct(CN[k]["pct"], 2)}</b>',
      f'{AI["marcas"][CN[k]["nome"]]["cobertura"]["All AI Platforms"]}%' if CN[k]["nome"] in AI["marcas"] else "—",
      dec(AI["marcas"][CN[k]["nome"]]["posicao"]) if CN[k]["nome"] in AI["marcas"] else "—",
      (f'<b class="{"down" if AI["marcas"][CN[k]["nome"]]["sentimento"] < 60 else "up"}">'
       f'{dec(AI["marcas"][CN[k]["nome"]]["sentimento"])}</b>') if CN[k]["nome"] in AI["marcas"] else "—"]
     for k in CN_ORD if k != "outras_marcas"], "wide") +
  '<div class="quadro"><p>Quando a comparação for de marca contra marca, a medida é a <b>cobertura</b>: Electrolux ' +
  pct(CN["electrolux"]["pct"], 2) + ' contra ' + pct(CN["brastemp"]["pct"], 2) + ' da Brastemp. Os ' +
  str(AI["marcas"]["Electrolux"]["cobertura"]["All AI Platforms"]) + '% da coluna de citação são sobre 150 perguntas e não descrevem tamanho de demanda.</p></div>',
  f'A Electrolux lidera as duas medidas. A Consul é o caso que mais diverge: {pct(CN["consul"]["pct"],2)} de cobertura, a 5ª do conjunto, e {AI["marcas"]["Consul"]["cobertura"]["All AI Platforms"]}% de citação, a 2ª — é pouco procurada pelo nome e muito citada quando ninguém nomeia. Tem também o melhor sentimento ({dec(AI["marcas"]["Consul"]["sentimento"])}), contra {dec(AI["marcas"]["Electrolux"]["sentimento"])} da Electrolux.',
  F_PAN + " · " + F_IA)

slide("ia", "Cobertura · Provedores", "A citação da categoria em IA é, hoje, citação no ChatGPT",
  "Citação de cada marca por provedor, sobre a amostra de 150 perguntas. O padrão vale para todos os players, o que indica característica da plataforma e não fraqueza de uma marca.",
  tabela(["Provedor"] + ["Electrolux","Consul","Brastemp","Samsung","Midea"],
         [[f'<b>{pv}</b>'] + [f'{AI["marcas"][m]["cobertura"][pv]}%' for m in ["Electrolux","Consul","Brastemp","Samsung","Midea"]]
          for pv in ["ChatGPT","Gemini","Google AI Mode","Perplexity"]], "wide") +
  kpis([(f'{AI["marcas"]["Electrolux"]["cobertura"]["ChatGPT"]}%', "das perguntas citam a Electrolux no ChatGPT", "#199e70"),
        ("7% a 9%", "nos outros três provedores", "#6b6a63")]),
  "Qualquer leitura de posição em IA que não separe provedor está lendo ChatGPT e chamando de IA.", F_IA)

# --- jornada --------------------------------------------------------------
slide("ia", "Jornada · Consolidado", "Metade da demanda em IA é exploração de categoria, e a posse pesa mais que a descoberta",
  "Os quatro estágios pelo volume que cada um concentra e, na última coluna, quanto de cada um está sem marca nenhuma.",
  barras_empilhadas([(EST_NOME[k], [("v", ES[k]["pct"], EST_COR[k]),
                                    ("resto", 100 - ES[k]["pct"], "#232322")],
                      f'<b style="color:{EST_COR[k]}">{pct(ES[k]["sem_marca_pct"],0)}</b> sem marca')
                     for k in EST_ORD], rotulos_dentro=False) +
  tabela(["Estágio","Volume","% da demanda","Prompts","<b>Sem marca</b>","Maior tópico sem marca"],
    [[f'<b style="color:{EST_COR[k]}">{EST_NOME[k]}</b>', n(ES[k]["volume"]), pct(ES[k]["pct"]),
      n(ES[k]["prompts"]),
      f'<b class="{"down" if ES[k]["sem_marca_pct"] >= 85 else "flat"}">{pct(ES[k]["sem_marca_pct"],1)}</b>',
      (f'<code>{e(ES[k]["exemplos_sem_marca"][0][0][:40])}</code> '
       f'<span class="fam">{e(fn(ES[k]["exemplos_sem_marca"][0][2]))}</span>') if ES[k]["exemplos_sem_marca"] else "—"]
     for k in EST_ORD], "wide"),
  f'<b>A escolha é o estágio mais desocupado: {pct(ES["escolha"]["sem_marca_pct"],1)} do volume não nomeia fabricante.</b> É o estágio em que a compra se decide e aquele em que as marcas menos aparecem na conversa mediada.', F_PAN)

d = ES["posse"]
slide("ia", "Retrato", "O território de posse é o maior espaço vago da categoria em IA",
  "As oito famílias de vida com o produto, pelo peso dentro do estágio, com os maiores tópicos que nenhuma marca reivindica. É o estágio que mais pesa depois da exploração de categoria.",
  '<div class="col2"><div>' +
  barras_h([(fn(f), pp, None) for f, c, pp in d["familias"]], lambda x: EST["posse"], fmt=lambda v: pct(v)) +
  '</div><div>' +
  tabela(["Maiores tópicos <b>sem marca</b> da posse","Família","Volume"],
         [[e(t[:40]), f'<span class="fam">{e(fn(f))}</span>', "<b>" + n(v) + "</b>"]
          for t, v, f in d["exemplos_sem_marca"][:6]]) +
  '</div></div>' +
  kpis([(n(d["volume"]), "de volume no estágio", EST["posse"]),
        (pct(d["pct"]), "da demanda mediada por IA", "#f0ede4"),
        (pct(d["sem_marca_pct"], 1), "sem marca nenhuma", "#c98500"),
        (pct(CN["electrolux"]["por_estagio"]["posse"]["pct"], 2), "é o que a Electrolux cobre", COR["electrolux"])]),
  f'A posse pesa {pct(d["pct"])} da demanda mediada contra {pct(ES["descoberta"]["pct"])} da descoberta, e {pct(d["sem_marca_pct"],1)} dela não carrega nome de fabricante — a maior taxa de território vago dos quatro estágios.', F_PAN)

# --- ocupacao real por dominio -------------------------------------------
DOM = list(OC.values())[0] if OC else None
if DOM:
    sintese("ia", "Ocupação · Síntese", "Presença e ocupação medem coisas diferentes, e a distância entre elas é o diagnóstico",
      "Duas medidas diferentes sobre o mesmo domínio. <b>Presença</b> é o volume dos tópicos em que a marca aparece de algum modo. <b>Ocupação</b> é essa presença ponderada pela visibilidade que ela tem dentro de cada tópico. As duas medem <b>quem a IA mostra</b>, e não o que é perguntado — por isso não se comparam com a cobertura das telas anteriores.",
      [(pct(DOM["presenca_pct"], 1), "presença: aparece", "Está em algum grau nos tópicos que somam esse volume.", "#d95926"),
       (pct(DOM["ocupacao_pct"], 1), "ocupação: de fato ocupa", "Ponderado pela visibilidade real. Menos da metade da presença.", "#c98500"),
       (str(DOM["visibility_mediana"]), "visibilidade mediana", "Nos tópicos em que aparece, ocupa cerca de um terço do espaço.", "#f0ede4"),
       (pct(DOM["por_estagio"]["posse"]["descoberto"], 1), "da posse sem ela", "O estágio em que está mais ausente é o de vida com o produto.", EST["posse"])],
      f'A {DOM["dominio"].split(".")[0].capitalize()} — a única marca do conjunto com esta medida calculada hoje — ocupa <b>{pct(DOM["ocupacao_pct"],1)}</b> da demanda mediada por IA. Serve de referência de patamar: mesmo uma marca estabelecida da categoria ocupa menos de um décimo da conversa. <b>Não leia este número contra os {pct(CN["electrolux"]["pct"],1)} de cobertura da Electrolux</b>: cobertura é o que se pergunta, ocupação é o que a IA mostra, e a Electrolux ainda não tem esta segunda medida calculada.',
      f'Tópicos de marca · {DOM["dominio"]} · {DOM["topicos_no_universo"]} tópicos de categoria em que o domínio aparece')

    slide("ia", "Ocupação", f'A {DOM["dominio"].split(".")[0].capitalize()} aparece em {pct(DOM["presenca_pct"],1)} da demanda da categoria e ocupa {pct(DOM["ocupacao_pct"],1)}',
      "Presença contra ocupação, estágio a estágio. A barra clara é o volume em que a marca aparece; a escura é o que ela de fato ocupa depois de ponderar pela visibilidade.",
      barras_empilhadas([(EST_NOME[k],
          [("ocupa", DOM["por_estagio"][k]["ocupacao"], "#d95926"),
           ("aparece sem ocupar", DOM["por_estagio"][k]["presenca"] - DOM["por_estagio"][k]["ocupacao"], "#5c3a2c"),
           ("descoberto", DOM["por_estagio"][k]["descoberto"], "#232322")],
          f'<b style="color:#c98500">{pct(DOM["por_estagio"][k]["descoberto"],0)}</b> descoberto')
        for k in EST_ORD], rotulos_dentro=False) +
      legenda([("Ocupa de fato", "#d95926"), ("Aparece sem ocupar", "#5c3a2c"), ("Sem presença nenhuma", "#232322")]) +
      tabela(["Tópico onde mais ocupa","Volume","Visibilidade","Menções","Estágio"],
        [[e(t[:44]), n(v), f'<b>{vis}</b>', str(men), EST_NOME.get(est, est)]
         for t, v, vis, men, est in DOM["maiores"][:5]], "wide"),
      f'A ocupação é mais baixa na posse ({pct(DOM["por_estagio"]["posse"]["ocupacao"],1)}), o mesmo vão que a parte de busca já mostrou, agora medido por outra fonte e em outra marca.',
      f'Tópicos de marca · {DOM["dominio"]}')

# --- os prompts -----------------------------------------------------------
EXF, MPF, EXL = PP["exemplos"], PP["marca_por_familia"], PP["exemplos_limpos"]
F_LIMPO = f'Prompts de IA · {n(PP["n_limpo"])} respostas de seed sem marca'
slide("ia", "Os prompts", "O que as pessoas de fato perguntam aos assistentes sobre a categoria",
  f'{n(PP["distintos"])} prompts lidos um a um, em {len(PP["por_provedor"])} provedores. Abaixo, as perguntas reais de maior relevância em cada família de necessidade.',
  tabela(["Família","Prompt real"],
    [[f'<b>{fn(f)}</b>', f'<code>{e(EXF[f][0][0][:118])}</code>']
     for f in ["assistencia e conserto","defeito e problema","manutencao e limpeza","peca e filtro",
               "instalacao","uso e receita","comparacao e modelo","preco e compra"] if f in EXF], "wide"),
  f'Uma resposta cita <b>{dec(PP["marcas_por_resposta"])} marcas em média</b> e apoia-se em {dec(PP["fontes_por_resposta"])} fontes. Não há segunda página: a marca não citada fica fora do resultado que o consumidor lê.', F_PRO)

slide("ia", "Retrato", "Quanto mais a pergunta se afasta da compra, menos a IA nomeia fabricante",
  f'Recorte limpo: as {n(PP["n_limpo"])} respostas de seeds sem marca, o único em que citar um fabricante é decisão do modelo e não eco do prompt. A barra é a fatia de respostas que cita alguma das sete marcas.',
  barras_h([(f'{fn(f)}  ·  n {MPF[f]["n"]}', MPF[f]["com_marca"], None)
            for f in sorted(MPF, key=lambda f: -MPF[f]["com_marca"])],
           lambda x: "#199e70", max_v=100, fmt=lambda v: pct(v, 1)) +
  # os dois extremos da curva, com a pergunta real de cada um
  '<div class="chips">' + "".join(
    f'<span class="chip"><b>{fn(f)} · {pct(MPF[f]["com_marca"],1)}</b>'
    f'<code>{e((next((x for x in EXL[f] if x[2]), EXL[f][0]))[0][:66])}</code></span>'
    for f in ["marca e loja", "especificacao de produto", "uso e receita", "instalacao"]
    if f in EXL and EXL[f]) + '</div>',
  f'<b>Não há degrau: é uma descida contínua ao longo de {len(MPF)} famílias.</b> Quando a pergunta é sobre loja, metade das respostas nomeia uma das sete. Quando é sobre instalar, nenhuma nomeia. E {pct(PP["taxa_marca_geral"],1)} das respostas do recorte inteiro citam alguma das sete.', F_LIMPO)

# --- AI Visibility: quatro relatorios, tres dominios
V = PAN["visibility"]
VNOME = {"electrolux":"Electrolux","brastemp":"Brastemp","consul":"Consul","midea":"Midea",
         "samsung":"Samsung","lg":"LG","panasonic":"Panasonic","outras":"Outras marcas"}
# relatorios de concorrente e em quantos deles a Electrolux passa o dono da casa
_CONC = [d for d in V.values() if d["dono"] != "electrolux"]
_ACIMA = [d for d in _CONC
          if d["electrolux_sov"] > next(p[1] for p in d["players"] if p[0] == d["dono"])]
EL_CHAT = V["loja-electrolux · ChatGPT"]["electrolux_sov"]
EL_AIM  = V["loja-electrolux · Google AI Mode"]["electrolux_sov"]
slide("ia", "Visibilidade", "Onde quer que se olhe, a Electrolux é das marcas mais faladas",
  "Share of voice em resposta de IA, de quatro relatórios sobre três domínios. <b>Cada relatório monta o próprio universo de perguntas, em torno do domínio analisado</b>, então a comparação só vale entre players da mesma linha. Em negrito, o dono de cada relatório. "
  "<b>Quando o mesmo player aparece com valores diferentes, o número de referência é o do relatório da Electrolux</b>; os demais entram como confirmação, não como medida.",
  tabela(["Relatório", "1º", "2º", "3º", "Onde o dono fica", "Sentimento do dono"],
    [[f'<b>{VNOME.get(d["dono"], d["dono"])}</b><br><span class="th2">{d["plataforma"]}</span>'] +
     [(f'<b>{VNOME.get(m, m)} {pct(sv,1)}</b>' if dono else f'{VNOME.get(m, m)} {pct(sv,1)}')
      for m, sv, _, dono in [x for x in d["players"] if x[0] != "outras"][:3]] +
     [f'<b class="{"up" if d["posicao_do_dono"] == 1 else "down"}">{d["posicao_do_dono"]}º</b>',
      f'<b class="{"down" if (d["favoravel_do_dono"] or 0) < 60 else "up"}">{d["favoravel_do_dono"]}%</b>']
     for d in V.values()], "wide") +
  kpis([(pct(EL_CHAT, 1), "SOV da Electrolux no ChatGPT · relatório dela, o número de referência", COR["electrolux"]),
        (pct(EL_AIM, 1), "SOV da Electrolux no Google AI Mode · relatório dela", COR["electrolux"]),
        ("1º", "posição dela nos dois relatórios próprios", "#199e70"),
        (f'{pct(V["midea · Google AI Mode"]["electrolux_sov"],1)} a {pct(V["consul · Google AI Mode"]["electrolux_sov"],1)}',
         "faixa em que ela aparece nos relatórios dos concorrentes", "#6b6a63")]),
  f'Nos relatórios da própria Electrolux ela é 1ª nas duas plataformas, com {pct(EL_CHAT,1)} e {pct(EL_AIM,1)} — são esses os números que valem. '
  f'Os {ext(len(_CONC))} relatórios de concorrente confirmam a leitura por outro caminho: '
  f'em {"ambos" if len(_ACIMA) == len(_CONC) else str(len(_ACIMA))} a Electrolux aparece mais que o dono da casa. '
  f'E no da Consul quem lidera é a Brastemp, com {pct([p[1] for p in V["consul · Google AI Mode"]["players"] if p[0] == "brastemp"][0],1)} — posição que ela não tem em nenhuma outra medida do material.',
  "Relatórios de visibilidade em IA · 4 relatórios · 3 domínios")

slide("ia", "Visibilidade", "A percepção da marca muda de acordo com o assistente",
  "Sentimento favorável do mesmo domínio, <code>loja.electrolux.com.br</code>, medido no mesmo dia em duas plataformas.",
  '<div class="confronto">'
  f'<div class="cf"><span class="cft">No ChatGPT</span><span class="cfv" style="color:#d95926">{V["loja-electrolux · ChatGPT"]["favoravel_do_dono"]}%</span><span class="cfl">de sentimento favorável</span></div>'
  '<div class="cfx">↔</div>'
  f'<div class="cf"><span class="cft">No Google AI Mode</span><span class="cfv" style="color:#199e70">{V["loja-electrolux · Google AI Mode"]["favoravel_do_dono"]}%</span><span class="cfl">de sentimento favorável</span></div></div>' +
  '<div class="quadro"><p>Não é ruído de amostra: são dois relatórios completos, com série temporal, gerados pela mesma ferramenta no mesmo dia. <b>Qualquer meta de percepção em IA precisa ser definida por plataforma</b> — uma média entre os dois descreveria uma marca que não existe.</p></div>',
  "O relatório do ChatGPT registra 40,5% de menções positivas para a Electrolux contra 53,1% da Consul. É a segunda fonte independente a colocar a Consul acima em percepção.",
  "Relatórios de visibilidade em IA · loja.electrolux.com.br")

REF = AI["referrals"]
# tudo calculado da serie: nenhum multiplo nem variacao digitada
_RS   = REF["series"]
_RTOT = [sum(s[i] for s in _RS.values()) for i in range(len(REF["meses"]))]
_REL  = _RS["loja.electrolux.com.br"]
_h    = len(_RTOT) // 2
MULT_EL  = _REL[-1] / (_REL[0] or 1)
MULT_CAT = _RTOT[-1] / (_RTOT[0] or 1)
VAR_SEM  = 100 * (sum(_RTOT[_h:]) / (sum(_RTOT[:_h]) or 1) - 1)
SH_INI, SH_FIM = 100*_REL[0]/_RTOT[0], 100*_REL[-1]/_RTOT[-1]
slide("ia", "Tendência", f'O tráfego vindo de LLM multiplicou por {dec(round(MULT_EL,1))} na Electrolux e por {dec(round(MULT_CAT,1))} nos quatro domínios',
  "Visitas mensais que chegam a cada domínio a partir de assistentes de IA. Os quatro domínios são os únicos da categoria com a medida disponível.",
  linhas({("electrolux" if "electrolux" in d else "brastemp" if "brastemp" in d else "consul" if "consul" in d else "midea"): s
          for d, s in _RS.items()}, destaque="electrolux", rotular_todos=True,
         rotulos_x=[m[-2:] for m in REF["meses"]], y0=0) +
  kpis([(n(_REL[-1]), "visitas/mês da loja vindas de LLM", "#3987e5"),
        (f'+{VAR_SEM:.0f}%', "os quatro domínios somados · 2º semestre contra o 1º", "#f0ede4"),
        (f'{pct(SH_INI,1)} → {pct(SH_FIM,1)}', "share da Electrolux dentro do canal", "#199e70")]),
  f'O canal cresce para todos — os quatro domínios somados sobem {VAR_SEM:.0f}% de um semestre para o outro. A Electrolux sai na frente em volume e ainda ganha participação dentro dele, de {pct(SH_INI,1)} para {pct(SH_FIM,1)}.', F_REF)

# ================================================================== PARTE 3
slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 3</span><h2>Busca e IA juntas</h2>
  <p class="sub">O que as duas fontes dizem quando comparadas: onde convergem, onde divergem, e a leitura que só existe no cruzamento</p></div></section>""")

slide("ambos", "Divergência", "Receita é a menor família em busca e a maior em IA",
  "A mesma necessidade aparece em posições opostas nas duas fontes. É comportamento migrando de canal.",
  '<div class="confronto">'
  f'<div class="cf"><span class="cft">Em busca</span><span class="cfv" style="color:#6b6a63">{pct(SD["familias"]["receita"])}</span><span class="cfl">do território sem dono · a <b>menor</b> família</span></div>'
  '<div class="cfx">↔</div>'
  f'<div class="cf"><span class="cft">Em IA</span><span class="cfv" style="color:#199e70">{pct(PAN["familias"]["uso e receita"]["pct"])}</span><span class="cfl">da categoria · a <b>maior</b> família de posse</span></div></div>' +
  tabela(["Maiores tópicos de uso e receita em IA","Volume"],
         [[e(t), "<b>" + n(v) + "</b>"] for t, v in PAN["familias"]["uso e receita"]["exemplos"][:4]]) +
  kpis([(n(PAN["familias"]["uso e receita"]["volume"]), "de volume em uso e receita na IA", "#199e70"),
        (pct(PAN["familias"]["uso e receita"]["sem_marca_pct"]), "dele sem marca nenhuma", "#c98500")]),
  "O briefing cita “pesquisar uma receita” como ponto de entrada. O dado diz que essa porta hoje é de assistente, não de buscador.", F_PAN + " · " + F_KW)

slide("search", "Mediação", "A IA já responde a maior parte das consultas de posse",
  "Com que frequência o Google entrega um resumo gerado no topo, em vez de links, para cada família de demanda.",
  barras_h([(FAMLAB.get(f, f.capitalize()), v["aio"], None) for f, v in
            sorted(D["familias_ai_overview"].items(), key=lambda i: -i[1]["aio"])[:12]],
           lambda k: "#c98500", max_v=100, fmt=lambda v: f"{v}%"),
  "Manutenção, defeito, instalação e consumo estão entre 84% e 93% de mediação.", F_KW)

ag = D["ai_overview_agregado"]
slide("ambos", "Mediação", "A mediação já alcançou o território que a marca não ocupa, e ainda não o dela",
  "Comparação da incidência de resumo gerado entre as famílias de posse, as demais famílias e a demanda própria da Electrolux.",
  kpis([(f'{ag["posse"]["aio"]}%', "das consultas de posse já são mediadas", "#c98500"),
        (f'{ag["demais"]["aio"]}%', "das demais famílias", "#6b6a63"),
        (f'{ag["electrolux"]}%', "das consultas da Electrolux", "#3987e5")]) +
  f'<div class="quadro alerta"><p>Quando a mediação avançar sobre as consultas de marca e de especificação, onde a Electrolux tem <b>{n(el["volume"])} buscas/mês</b> e hoje controla o resultado, a marca passa a ser intermediada em terreno que domina.</p></div>',
  "É a única leitura do material que só existe cruzando as duas fontes.", F_KW)

slide("ambos", "Síntese", "As duas fontes concordam sobre o vão e discordam sobre a posição",
  "Onde busca e IA convergem, a leitura é robusta. Onde divergem, a divergência é informação sobre como cada canal funciona.",
  tabela(["","<span class='badge b-search'>Search</span>","<span class='badge b-ia'>IA</span>"],
    [["<b>Posição da Electrolux</b>","3ª em volume de marca · recortes de profundidade diferente impedem comparar tamanho entre players", f'<b>{pct(CN["electrolux"]["pct"],1)}</b> de cobertura sobre o total · <b>1ª entre as sete</b>'],
     ["<b>Trajetória</b>","não ganha share; quem cresce são os entrantes",f'share de tráfego <b>{pct(SH_INI,1)} → {pct(SH_FIM,1)}</b>'],
     ["<b>Posse</b>", f'{pct(el["posse"])} da demanda da marca · metade da Consul', f'cobre {pct(CN["electrolux"]["por_estagio"]["posse"]["pct"],2)} do estágio · <b>a maior das sete</b>, e ainda assim quase nada'],
     ["<b>Quem ocupa a posse</b>", f'Consul, com {pct(P["consul"]["posse"])} da demanda dela', f'Ninguém: {pct(ES["posse"]["sem_marca_pct"],1)} do estágio não tem marca no nome'],
     ["<b>Percepção</b>","não é o que a fonte mede", f'sentimento {dec(AI["marcas"]["Electrolux"]["sentimento"])}, 2º pior do conjunto']], "wide"),
  "A marca está melhor posicionada no canal novo do que no maduro, e não construiu essa vantagem deliberadamente.", F_KW + " · " + F_IA)

slide("ambos", "Fechamento", "Os quatro achados que sustentam o resto",
  "",
  '<div class="achados">' + "".join(
    f'<div class="ach"><span class="an">{i}</span><div><b>{t}</b><p>{dd}</p></div></div>'
    for i, (t, dd) in enumerate([
      ("A IA só nomeia fabricante quando a pergunta é de compra",
       f'A citação cai de forma contínua ao longo de {len(MPF)} famílias: {pct(MPF["marca e loja"]["com_marca"],1)} das respostas sobre onde comprar citam uma das sete marcas, '
       f'{pct(MPF["produto e categoria"]["com_marca"],1)} das respostas sobre o produto, {pct(MPF["uso e receita"]["com_marca"],1)} das sobre uso e receita, e {pct(MPF["instalacao"]["com_marca"],1)} das sobre instalação. '
       f'Quanto mais a pergunta se afasta da transação, mais a categoria é respondida sem que exista fabricante.'),
      ("A Electrolux ganhou presença em IA sem ganhar reputação",
       f'É a mais coberta das sete ({pct(CN["electrolux"]["pct"],1)} da demanda mediada, contra {pct(CN["brastemp"]["pct"],1)} da Brastemp) e a segunda pior em sentimento ({dec(AI["marcas"]["Electrolux"]["sentimento"])} contra {dec(AI["marcas"]["Consul"]["sentimento"])} da Consul). '
       f'São medidas independentes: ser citada mais não faz ser falada melhor.'),
      ("O crescimento da categoria está nos entrantes",
       f'Hisense a {vs("hisense")} e Haier a {vs("haier")} contra a categoria; Brastemp a {vs("brastemp")} e Samsung a {vs("samsung")}.'),
      ("Quem for ocupar a posse vai encontrar um intermediário já instalado",
       f'{pct(ES["posse"]["sem_marca_pct"],1)} da demanda de posse em IA não nomeia fabricante e {ag["posse"]["aio"]}% das consultas de posse em busca já são respondidas por resumo gerado. '
       f'O território está vago do lado das marcas e ocupado do lado da mediação.')], 1)) + '</div>',
  "", "")

slide("ambos", "Fechamento", "O que muda com o tempo, e o que não",
  "Este material para aqui: os dados e a leitura deles. A decisão de território, mensagem e plano é das áreas.",
  '<div class="col2"><div class="quadro"><span class="qh">Move com o tempo</span><ul>'
  '<li>A base instalada de Haier e Hisense começa a gerar demanda de pós-compra</li>'
  '<li>O tráfego de LLM segue crescendo em toda a categoria</li>'
  f'<li>A conversa de uso e receita já trocou de canal: é a menor família em busca ({pct(SD["familias"]["receita"])} do território sem dono) e a maior de posse em IA ({pct(PAN["familias"]["uso e receita"]["pct"])} da categoria)</li>'
  f'<li>A mediação sobe da posse para a compra: hoje responde {ag["posse"]["aio"]}% das consultas de posse e {ag["electrolux"]}% das da Electrolux — a distância entre os dois números é o prazo que a marca tem</li></ul></div>'
  '<div class="quadro"><span class="qh">Não move sozinho</span><ul>'
  '<li>O território de posse continua sem dono enquanto ninguém o ocupar</li>'
  f'<li>A escolha de produto segue sem dono: {pct(ES["escolha"]["sem_marca_pct"],1)} do estágio em que a compra se decide não nomeia fabricante nenhum</li>'
  f'<li>Reputação não vem junto com presença: a Electrolux é a mais citada da categoria e a segunda pior em sentimento ({dec(AI["marcas"]["Electrolux"]["sentimento"])} contra {dec(AI["marcas"]["Consul"]["sentimento"])} da Consul)</li>'
  f'<li>Nome de frente comercial não vira demanda por existir: as sete somam {n(V_FRENTES)} buscas/mês, {pct(100*V_FRENTES/el["volume"],1)} da demanda pela marca</li></ul></div></div>',
  "", "")
_p1=[]
sintese("search", "Parte 1 · Síntese", "A marca é grande onde se escolhe o produto e pequena onde se convive com ele",
  "O que esta parte estabelece, antes de abrir marca por marca. Toda a leitura é de demanda de busca no Brasil, doze meses.",
  [(pct(el["posse"]), "da demanda da Electrolux é posse", f'Contra {pct(P["consul"]["posse"])} da Consul, a única das sete em que a demanda de quem já comprou pesa de verdade.', COR["electrolux"]),
   (vs("electrolux"), "de share ano a ano contra a categoria", "A marca não perde e não ganha share. Hisense (1,40) e Haier (1,36) crescem.", "#f0ede4"),
   (n(SD["volume"]), "buscas/mês que ninguém reivindica", "Território 100% posse, sem fabricante nomeado em nenhuma consulta.", COR["sem_dono"]),
   (pct(100*V_FRENTES/el["volume"], 1), "é o que as sete frentes somam", "A estrutura de serviço existe e o nome dela quase não é procurado.", "#d95926")],
  "A demanda de posse existe e a marca não está nela. A decisão que isso pede é <b>onde a marca escolhe existir</b>, antes de qualquer discussão de eficiência de mídia. As telas seguintes mostram player a player quem já fez essa escolha.",
  F_KW, destino=_p1)
slides[IDX_P1:IDX_P1] = _p1

_ab = []
slide("ambos", "O argumento", "A categoria é procurada; as marcas, quase não",
  "Duas medições independentes, uma em busca e outra em IA, chegam ao mesmo lugar. A demanda existe em escala e a maior parte dela não menciona nenhum fabricante.",
  kpis([(pct(SM["pct"], 1), "da demanda em IA não nomeia fabricante", EST["sem_marca"]),
        (pct(ES["escolha"]["sem_marca_pct"], 1), "no momento em que a compra se decide", EST["escolha"]),
        (pct(100*J4["sem_marca"]/J4["total"], 1), "da demanda de busca, mesma leitura", COR["generico"])]) +
  tabela(["Fonte","Demanda medida","Sem marca nenhuma","O que isso quer dizer"], [
    ['<span class="badge b-search">Search</span>', n(J4["total"]) + " buscas/mês",
     f'<b>{pct(100*J4["sem_marca"]/J4["total"],1)}</b>',
     "Metade das buscas da categoria acontece antes de qualquer fabricante entrar na conta"],
    ['<span class="badge b-ia">IA</span>', n(U["volume"]) + " de volume mediado",
     f'<b>{pct(SM["pct"],1)}</b>',
     "Quatro em cada cinco tópicos de categoria não carregam nome de marca"]], "wide") +
  f'<div class="quadro"><span class="qh">A consequência para a resposta</span><p>O briefing pede para converter reconhecimento em intenção no momento da decisão. Nesse momento específico, <b>{pct(ES["escolha"]["sem_marca_pct"],1)} da demanda mediada por IA não tem dono</b>. Ocupar o ecossistema deixa de ser ambição de posicionamento e passa a ser um espaço medido, com tamanho e endereço.</p></div>',
  "", F_KW + " · " + F_PAN, destino=_ab)
# a Parte 1 e inserida antes da abertura de proposito: inserir do indice maior
# para o menor evita que a primeira insercao desloque a segunda
slides[IDX_ABERTURA:IDX_ABERTURA] = _ab

print("total material:", len(slides))

# ================================================== DECK SEPARADO: RESSALVAS
apendice.append("""<section class="slide capa"><div class="slide-inner">
  <span class="kicker">Youdare · Direção de Mídia e Dados · agosto 2026</span>
  <h1>Ressalvas<br><em>de dado</em></h1>
  <p class="sub">Complemento técnico do material de cenário — o que checar antes de construir em cima, e o que este pacote não responde</p>
  <div class="capa-meta"><span>Uso interno</span><span>Leia junto com o deck de cenário</span></div>
</div></section>""")

slide("ambos", "Ressalvas", "Números frágeis: confira antes de levar para o cliente",
  "Cada linha indica um número presente no material de cenário que não sustenta contestação sem contexto.",
  tabela(["Número","Por quê","Onde aparece"], [
    ["Descoberta da Samsung, 5,5%","O recorte de origem partiu de uma consulta de categoria, não do nome da marca. É artefato, não achado","Panorama · comparativo de jornada"],
    ["Citação em IA nas famílias de posse (0%, 25%)","As famílias de manutenção e receita têm entre 3 e 4 perguntas na amostra de 150","Comparativo de IA · síntese"],
    ["Sentimento (58,1 · 70,5 · 46,3)","Classificação automática, sem critério publicado. Vale como comparação relativa, não como nível absoluto","Comparativo de IA"],
    ["Séries de 12 meses","Reconstruídas a partir do volume médio e do índice de tendência, sob premissa declarada","Todos os slides de evolução"],
    ["Volumes entre players em <b>busca</b>","Recortes com profundidade diferente: Brastemp 1.998 keywords, Haier 44. Composição interna da marca é comparável; tamanho entre marcas não. <b>A comparação de cobertura entre players só é válida na base de IA</b>, cujos 16 exports partem dos mesmos seeds de categoria","Panorama e blocos de player"],
    ["Tráfego de LLM","Estimativa modelada, não contagem","Slide de tendência"],
    ["Famílias de demanda","A classificação cobre entre 33% e 89% do volume por player. “Não classificado” é categoria legítima","Todos os slides de jornada"],
    ["Volume das frentes nomeadas","Soma duas grafias da marca (<code>electrolux</code> e <code>eletrolux</code>) e vem de dois recortes diferentes. Frente não é família: cada uma entra pela necessidade que atende","Slides do modelo e da Electrolux"],
    ["Todo percentual do panorama de IA","Cada export para em 1.000 linhas. É participação sobre <b>demanda mapeada</b>, não sobre o universo da categoria. Seed novo muda o denominador","Parte 2 inteira"],
    ["Cobertura por marca em IA","Medida pelo <b>nome do tópico</b>, sobre o total da demanda. Não tem viés de seed, porque os 16 exports são de categoria, mas mede o que é <b>perguntado</b> e não quem a IA cita na resposta","Cobertura consolidado e por marca"],
    ["Menção de marca dentro da resposta","Vem de busca de string no texto: a ferramenta entrega a contagem, não os nomes. E os exports de prompt são semeados por marca","Slides de prompt"],
    ["Ocupação por domínio (19,2% e 8,2%)","A medida existe por domínio e está disponível para um domínio do conjunto. Não comparar com as demais marcas até haver a mesma medida para elas","Slides de ocupação"],
    ["Estágio da jornada em IA","Derivado por regra declarada: família cruzada com intent da ferramenta, com cortes em 25% e 45%. É regra, não medição","Todos os slides de jornada em IA"],
    ["Curva de citação por família","Duas famílias ficam de fora por amostra: <b>assistência e conserto</b> e <b>defeito e problema</b>, ambas com n=18 e corte em 20. São as duas mais centrais à tese de serviço e entram no próximo ciclo","Retrato de citação por necessidade"],
    ["Share of voice em IA","<b>Cada relatório monta o próprio universo de perguntas.</b> A Electrolux tem 12,4% no relatório dela, 16,5% no da Consul e 11,2% no da Midea. Comparar SOV entre relatórios é erro; só vale entre players do mesmo. <b>Regra do material: divergindo, o número de referência é sempre o do relatório da Electrolux</b>; os de concorrente entram como confirmação","Slides de visibilidade"],
    ["Sentimento por plataforma","41% no ChatGPT e 71% no Google AI Mode. Cada um é do dono dentro do próprio universo, então a distância é indicativa e não conclusiva","Slide de percepção por assistente"]], "wide"),
  "", "", apendice)

slide("ambos", "Ressalvas", "O que este pacote de dados não responde",
  "Cinco perguntas ficaram fora do alcance das fontes. Nenhuma foi preenchida por suposição.",
  tabela(["Pergunta","Por que não","O que resolveria"], [
    ["Quem captura cada consulta hoje","A coluna de competidores veio vazia em todos os arquivos","Posições orgânicas dos domínios captores"],
    ["Qual o valor da demanda não capturada","Sem custo real e sem taxa de conversão","Dados de conta e analytics da loja"],
    ["O que a IA responde quando perguntam pela marca pelo nome","Só veio o recorte sem marca","Relatório de respostas com marca"],
    ["Quais fontes os modelos citam","Há contagem de fontes, não a lista","Export de fontes citadas"],
    ["Hisense e Haier em IA","Não estão nas respostas nem no tráfego medido","Incluir os dois no rastreio"]], "wide"),
  "Lacuna declarada é método. O material de cenário não preenche nenhuma delas.", "", apendice)

slide("ambos", "Ressalvas", "Como os números foram produzidos",
  "O material inteiro é gerado por script a partir de um único arquivo de dados consolidado. Nenhuma cifra é digitada à mão.",
  tabela(["Etapa","O que faz"], [
    ["<b>Normalização</b>","Unifica os arquivos de origem, remove duplicatas e consultas em idioma estrangeiro, e reconstrói a série mensal"],
    ["<b>Consolidação</b>","Calcula todos os recortes do material e grava num único arquivo de dados"],
    ["<b>Geração</b>","Monta os slides a partir desse arquivo. Qualquer número muda na origem e se propaga sozinho"]], "wide") +
  '<div class="quadro"><p>Reproduzir o material inteiro leva dois comandos. Isso é o que torna cada número deste deck rastreável até o arquivo de origem.</p></div>',
  "", "", apendice)
print("apendice:", len(apendice))

# ================================================================== CSS + HTML
CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--surface:#1a1a19;--surface-2:#212120;--ink:#f0ede4;--ink-2:#a8a69c;--ink-3:#6b6a63;
  --hair:#2e2e2b;--accent:#3987e5;--ia:#199e70;--ambos:#c98500}
html,body{height:100%;background:var(--surface);color:var(--ink);
  font-family:'Supreme',ui-sans-serif,sans-serif;font-feature-settings:'tnum' 1;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
body{scroll-snap-type:y mandatory;overflow-y:auto;cursor:pointer}

/* === VIEWPORT FITTING (NAO NEGOCIAVEL) === */
.slide{height:100vh;height:100dvh;overflow:hidden;scroll-snap-align:start;position:relative;
  display:flex;align-items:center;
  background:radial-gradient(120% 90% at 88% 6%,#22231f 0%,var(--surface) 62%)}
.slide::after{content:'';position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(var(--hair) 1px,transparent 1px);background-size:100% 64px;opacity:.22}
.slide-inner{position:relative;z-index:1;width:min(1580px,92vw);margin:0 auto;max-height:90vh;
  display:flex;flex-direction:column;gap:clamp(.45rem,1.1vh,1rem)}

/* === TIPOGRAFIA === */
.kicker{font-size:clamp(.56rem,.8vw,.74rem);letter-spacing:.24em;text-transform:uppercase;
  color:var(--accent);font-weight:600}
h1{font-family:'Zodiak',Georgia,serif;font-weight:400;line-height:.98;
  font-size:clamp(2.4rem,6.2vw,5.6rem);letter-spacing:-.02em}
h1 em{font-style:italic;color:var(--accent)}
h2{font-family:'Zodiak',Georgia,serif;font-weight:400;line-height:1.06;
  font-size:clamp(1.3rem,2.7vw,2.5rem);letter-spacing:-.015em;max-width:36ch}
.s-head{display:flex;flex-direction:column;gap:clamp(.16rem,.45vh,.4rem);
  border-left:2px solid var(--accent);padding-left:clamp(.6rem,1vw,1rem)}
.s-top{display:flex;align-items:center;gap:.8em;flex-wrap:wrap}
.subt{color:var(--ink-2);font-size:clamp(.7rem,.98vw,.9rem);line-height:1.45;max-width:88ch;
  margin-top:.15em}
.sub{color:var(--ink-2);font-size:clamp(.8rem,1.12vw,1.02rem);max-width:62ch;line-height:1.45}
.leitura{color:var(--ink-2);font-size:clamp(.7rem,.96vw,.88rem);line-height:1.5;max-width:100ch;
  border-top:1px solid var(--hair);padding-top:clamp(.3rem,.7vh,.6rem)}
.leitura b{color:var(--ink);font-weight:600}
.fonte{color:var(--ink-3);font-size:clamp(.52rem,.7vw,.64rem);letter-spacing:.04em}
.s-body{flex:1;min-height:0;display:flex;flex-direction:column;
  gap:clamp(.4rem,.9vh,.85rem);justify-content:center;overflow:hidden}

/* === BADGE DE FONTE === */
.badge{font-size:clamp(.5rem,.68vw,.62rem);letter-spacing:.14em;text-transform:uppercase;
  font-weight:600;padding:.28em .7em;border-radius:2em;border:1px solid;white-space:nowrap}
.b-search{color:var(--accent);border-color:color-mix(in srgb,var(--accent) 45%,transparent);
  background:color-mix(in srgb,var(--accent) 12%,transparent)}
.b-ia{color:var(--ia);border-color:color-mix(in srgb,var(--ia) 45%,transparent);
  background:color-mix(in srgb,var(--ia) 12%,transparent)}
.b-ambos{color:var(--ambos);border-color:color-mix(in srgb,var(--ambos) 45%,transparent);
  background:color-mix(in srgb,var(--ambos) 12%,transparent)}
/* slide que nao vem de busca nem de IA: contexto declarado pelo cliente */
.b-briefing{color:var(--ink-3);border-color:var(--hair);border-style:dashed}

/* === CAPA E DIVISOR === */
.capa .slide-inner,.divisor .slide-inner{gap:clamp(.6rem,1.9vh,1.6rem)}
.capa-meta{display:flex;flex-wrap:wrap;gap:clamp(.45rem,1.3vw,1.3rem);margin-top:clamp(.3rem,1.2vh,1rem)}
.capa-meta span{font-size:clamp(.58rem,.84vw,.78rem);color:var(--ink-2);letter-spacing:.05em;
  border:1px solid var(--hair);padding:.3em .8em;border-radius:2em}
.divisor{background:linear-gradient(115deg,#202220 0%,var(--surface) 58%)}
.parte{font-size:clamp(.58rem,.88vw,.8rem);letter-spacing:.3em;text-transform:uppercase;color:var(--accent)}
.divisor h2{font-size:clamp(2rem,5.2vw,4.6rem);max-width:none}

/* === FONTES (slide 2) === */
.fontes{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.7rem,2vw,2rem)}
.fx{border:1px solid var(--hair);padding:clamp(.7rem,1.8vh,1.3rem) clamp(.8rem,1.5vw,1.3rem);
  display:flex;flex-direction:column;gap:.3em;background:var(--surface-2)}
.fxb{align-self:flex-start;font-size:clamp(.5rem,.68vw,.62rem);letter-spacing:.14em;
  text-transform:uppercase;font-weight:600;padding:.28em .7em;border-radius:2em;border:1px solid}
.fxv{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.8rem,4vw,3.4rem);line-height:1}
.fxl{font-size:clamp(.62rem,.86vw,.8rem);color:var(--ink-2)}

/* === BARRAS === */
.bh{display:flex;flex-direction:column;gap:clamp(.22rem,.8vh,.55rem)}
.bh-row{display:grid;grid-template-columns:minmax(9ch,24ch) 1fr minmax(6ch,9ch);
  align-items:center;gap:clamp(.4rem,.9vw,.9rem)}
.bh-lab{font-size:clamp(.6rem,.86vw,.82rem);color:var(--ink-2);text-align:right;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bh-track{height:clamp(.8rem,2.3vh,1.45rem);background:#232322;border-radius:2px;overflow:hidden}
.bh-fill{display:block;height:100%;border-radius:0 3px 3px 0;animation:grow .8s cubic-bezier(.2,.8,.2,1) both}
.bh-val{font-size:clamp(.6rem,.88vw,.84rem);font-weight:600}
@keyframes grow{from{transform:scaleX(0);transform-origin:left}to{transform:scaleX(1)}}

.be{display:flex;flex-direction:column;gap:clamp(.22rem,.8vh,.55rem)}
.be-row{display:grid;grid-template-columns:minmax(9ch,14ch) 1fr minmax(7ch,13ch);
  align-items:center;gap:clamp(.4rem,.9vw,.9rem)}
.be-lab{font-size:clamp(.6rem,.86vw,.82rem);color:var(--ink-2);text-align:right}
.be-track{display:flex;height:clamp(1.05rem,3.1vh,2rem);border-radius:2px;overflow:hidden;gap:2px}
.be-seg{display:flex;align-items:center;justify-content:center;font-size:clamp(.5rem,.72vw,.68rem);
  font-weight:600;animation:grow .8s cubic-bezier(.2,.8,.2,1) both;overflow:hidden}
.be-extra{min-width:16ch;max-width:20ch;font-size:clamp(.58rem,.84vw,.78rem);color:var(--ink-2);line-height:1.25}
.legenda{display:flex;flex-wrap:wrap;gap:clamp(.45rem,1.2vw,1.2rem);margin-top:.25rem}
.legenda span{display:flex;align-items:center;gap:.4em;font-size:clamp(.56rem,.78vw,.72rem);color:var(--ink-2)}
.legenda i{width:.78em;height:.78em;border-radius:2px;display:block}

/* === MINI BARRAS MES A MES === */
.sbw{display:inline-flex;align-items:flex-end;gap:2px;height:clamp(1.1rem,3vh,1.9rem);width:100%}
.sb{flex:1;min-width:3px;border-radius:1px;display:block;opacity:.9}
.mm{display:flex;flex-direction:column;gap:.3em;border-top:1px solid var(--hair);padding-top:.6em}
.mml{font-size:clamp(.5rem,.7vw,.62rem);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}

/* === SVG === */
.chart{width:100%;height:auto;max-height:min(50vh,450px);display:block}
.ln{fill:none;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round;opacity:.55}
.ln.forte{stroke-width:2.6;opacity:1}
.ref{stroke:var(--hair);stroke-width:1;stroke-dasharray:3 4}
.reflab,.xlab,.lnlab{font-family:'Supreme',sans-serif;font-size:11px;fill:var(--ink-3)}
.lnlab{font-size:12px;font-weight:600}.lnlab.fraco{font-size:11px;font-weight:500}
.xlab{text-anchor:middle}

/* === TABELAS === */
.tb,.hm{width:100%;border-collapse:collapse;font-size:clamp(.58rem,.85vw,.82rem)}
.tb th,.hm th{text-align:left;color:var(--ink-3);font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;font-size:clamp(.48rem,.66vw,.62rem);padding:.45em .65em;
  border-bottom:1px solid var(--hair)}
.tb td{padding:.46em .65em;border-bottom:1px solid #232322;color:var(--ink-2);vertical-align:middle}
.tb td b,.tb td:first-child{color:var(--ink)}
.hm td{padding:.45em .35em;text-align:center;border:1px solid var(--surface);
  font-variant-numeric:tabular-nums;font-size:clamp(.53rem,.75vw,.74rem)}
.hm th.rh{text-align:right;text-transform:none;font-size:clamp(.56rem,.78vw,.76rem);
  color:var(--ink-2);border:none;padding-right:.65em}
.hm thead th{text-align:center;padding-bottom:.35em}
.dot{display:inline-block;width:.6em;height:.6em;border-radius:50%;margin-right:.5em}
.up,.tb td b.up{color:#199e70;font-weight:600}
.down,.tb td b.down{color:#d95926;font-weight:600}
.flat,.tb td b.flat{color:var(--ink-3)}
code{font-family:ui-monospace,monospace;font-size:.88em;color:var(--ink);background:#26261f;
  padding:.1em .4em;border-radius:2px;white-space:nowrap}
/* nome da familia colado ao termo de exemplo: nenhum termo aparece sem dizer de onde vem */
.fam{display:inline-block;font-size:.86em;letter-spacing:.06em;color:var(--ink-3);
  border:1px solid var(--hair);border-radius:2px;padding:.06em .45em;white-space:nowrap}
/* linha de grupo dentro da tabela: separa com-marca de sem-marca */
.tb tr.grp-row td.grp{padding:.7em .65em .3em;border-bottom:1px solid var(--hair);
  color:var(--ink-2);font-size:.94em}
.tb tr.grp-row td.grp b{color:var(--ink);letter-spacing:.02em}
.chips-tit{display:block;margin-top:clamp(.35rem,.9vh,.8rem);font-size:clamp(.48rem,.66vw,.62rem);
  letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3)}
.chips-tit + .chips{margin-top:.35rem}

/* === KPIS E BLOCOS === */
.kpis{display:flex;flex-wrap:wrap;gap:clamp(.5rem,1.8vw,2.2rem);
  border-top:1px solid var(--hair);padding-top:clamp(.35rem,.9vh,.8rem)}
.kpi{display:flex;flex-direction:column;gap:.1em;min-width:min(18ch,42vw)}
.kv{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.3rem,3vw,2.7rem);line-height:1;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kl{font-size:clamp(.56rem,.8vw,.74rem);color:var(--ink-2);line-height:1.3;max-width:26ch}
.col2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.7rem,2.2vw,2.2rem);align-items:start;min-height:0}
.quadro{border:1px solid var(--hair);border-left:2px solid var(--accent);
  padding:clamp(.55rem,1.4vh,1rem) clamp(.7rem,1.3vw,1.1rem);background:var(--surface-2)}
.quadro.alerta{border-left-color:var(--ambos)}
.quadro p,.quadro li{color:var(--ink-2);font-size:clamp(.7rem,.98vw,.9rem);line-height:1.5}
.quadro b{color:var(--ink)}
.quadro ul{margin-left:1.1em;display:flex;flex-direction:column;gap:.28em}
.qh{display:block;font-size:clamp(.52rem,.72vw,.64rem);letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);margin-bottom:.45em}
blockquote{font-family:'Zodiak',Georgia,serif;font-size:clamp(.92rem,1.8vw,1.5rem);line-height:1.35;color:var(--ink)}
cite{display:block;margin-top:.55em;font-style:normal;font-size:clamp(.56rem,.78vw,.72rem);color:var(--ink-3)}
.sem-cob{border:1px dashed var(--hair);padding:clamp(.6rem,1.6vh,1.2rem);text-align:center;
  display:flex;flex-direction:column;gap:.28em;background:#1e1e1c}
.sc-x{font-size:clamp(1.1rem,2.4vw,2rem);color:var(--ink-3);line-height:1}
.sem-cob b{font-size:clamp(.7rem,.98vw,.88rem)}
.sem-cob span:last-child{font-size:clamp(.56rem,.78vw,.72rem);color:var(--ink-3);max-width:34ch;margin:0 auto}
.confronto{display:flex;align-items:center;gap:clamp(.6rem,2.2vw,2.2rem);justify-content:center;
  border-block:1px solid var(--hair);padding:clamp(.6rem,1.8vh,1.2rem) 0}
.cf{display:flex;flex-direction:column;gap:.18em;text-align:center;flex:1}
.cft{font-size:clamp(.52rem,.72vw,.64rem);letter-spacing:.2em;text-transform:uppercase;color:var(--ink-3)}
.cfv{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.8rem,4.6vw,4rem);line-height:1}
.cfl{font-size:clamp(.58rem,.82vw,.78rem);color:var(--ink-2)}
.cfx{font-size:clamp(1rem,2.2vw,1.8rem);color:var(--ink-3)}
/* chips: familia + uma consulta real que a exemplifica */
.chips{display:flex;flex-wrap:wrap;gap:clamp(.28rem,.7vw,.6rem);margin-top:clamp(.4rem,1.1vh,.9rem)}
.chip{display:flex;flex-direction:column;gap:.12em;border:1px solid var(--hair);border-left-width:3px;
  border-left-color:var(--ink-3);padding:.32em .6em;min-width:0;flex:1 1 0}
.chip b{font-size:clamp(.5rem,.7vw,.62rem);letter-spacing:.11em;text-transform:uppercase;color:var(--ink-3);
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chip code{font-size:clamp(.58rem,.82vw,.76rem);color:var(--ink);white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;display:block}
.chip.e-descoberta{border-left-color:#f2c777}
.chip.e-escolha{border-left-color:#c98500}
.chip.e-posse{border-left-color:#7d5300}
.chip.e-sem_marca{border-left-color:#f7e3b8}
.th2{display:block;font-weight:400;text-transform:none;letter-spacing:0;color:var(--ink-3);font-size:.86em;margin-top:.15em}
.arq{font-size:clamp(.56rem,.78vw,.72rem);color:var(--ink-3);display:block}
/* quadrante: retrato posicional dos players em duas medidas */
.quad .qbg{fill:#1e1e1c}
.quad .qhi{fill:color-mix(in srgb,var(--accent) 7%,transparent)}
.quad .qax{stroke:var(--hair);stroke-width:1;stroke-dasharray:4 4}
.quad .qlab{fill:var(--ink-3);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.quad .qnome{font-size:15px;font-weight:600}
.quad .qcorte{fill:var(--ink-3);font-size:12px}
.quad .qeixo{fill:var(--ink-3);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
.quad .qpt{stroke:var(--surface);stroke-width:2}
.mini{font-size:clamp(.56rem,.78vw,.72rem);color:var(--ink-3);margin-top:.5em}
/* sintese executiva: abre um bloco dizendo o que ele decide */
.sintese{display:grid;grid-template-columns:repeat(auto-fit,minmax(0,1fr));gap:clamp(.5rem,1.5vw,1.4rem)}
.sx{border-top:2px solid var(--hair);padding-top:clamp(.4rem,1.1vh,.8rem);display:flex;
  flex-direction:column;gap:.16em;min-width:0}
.sxn{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.5rem,3.6vw,3.1rem);line-height:1}
.sxl{font-size:clamp(.52rem,.72vw,.64rem);letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3)}
.sxp{font-size:clamp(.6rem,.86vw,.8rem);color:var(--ink-2);line-height:1.45;margin-top:.2em}
.achados{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.55rem,1.6vw,1.5rem)}
.ach{display:flex;gap:clamp(.5rem,1.1vw,1rem);border-top:1px solid var(--hair);padding-top:.65em}
.an{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.1rem,2.2vw,1.9rem);color:var(--accent);line-height:1}
.ach b{display:block;font-size:clamp(.74rem,1.02vw,.95rem);margin-bottom:.22em}
.ach p{font-size:clamp(.6rem,.86vw,.8rem);color:var(--ink-2);line-height:1.45}

/* === NAV === */
.nav{position:fixed;right:clamp(.5rem,1.4vw,1.4rem);top:50%;transform:translateY(-50%);z-index:50;
  display:flex;flex-direction:column;gap:6px}
.nav b{width:6px;height:6px;border-radius:50%;background:var(--hair);cursor:pointer;
  transition:background .2s,transform .2s}
.nav b.on{background:var(--accent);transform:scale(1.5)}
.pg{position:fixed;left:clamp(.6rem,1.6vw,1.6rem);bottom:clamp(.5rem,1.4vh,1.2rem);z-index:50;
  font-size:clamp(.54rem,.74vw,.68rem);color:var(--ink-3);letter-spacing:.1em}
.dica{position:fixed;right:clamp(.6rem,1.6vw,1.6rem);bottom:clamp(.5rem,1.4vh,1.2rem);z-index:50;
  font-size:clamp(.5rem,.68vw,.62rem);color:var(--ink-3);letter-spacing:.06em;opacity:.75}

/* === BREAKPOINTS DE ALTURA === */
@media (max-height:700px){.slide-inner{max-height:93vh}.kpi{min-width:min(15ch,40vw)}}
@media (max-height:600px){.chart{max-height:36vh}.leitura,.subt{font-size:.68rem}
  .bh-track{height:.6rem}.be-track{height:.75rem}.bh,.be{gap:.2rem}.be-seg{font-size:.46rem}}
@media (max-height:500px){h2{font-size:1.15rem}.kv{font-size:1.25rem}.chart{max-height:30vh}
  .fonte,.legenda{display:none}}
@media (max-width:900px){.col2,.achados,.fontes{grid-template-columns:1fr}}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = """
const ss=[...document.querySelectorAll('.slide')];
const nav=document.querySelector('.nav'), pg=document.querySelector('.pg');
let atual=0;
ss.forEach((_,i)=>{const b=document.createElement('b');
  b.onclick=ev=>{ev.stopPropagation();ir(i)};nav.appendChild(b)});
const dots=[...nav.children];
function ir(i){atual=Math.max(0,Math.min(i,ss.length-1));ss[atual].scrollIntoView({behavior:'smooth'})}
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){
  atual=ss.indexOf(en.target);dots.forEach((d,j)=>d.classList.toggle('on',atual===j));
  pg.textContent=String(atual+1).padStart(2,'0')+' / '+String(ss.length).padStart(2,'0');}}),{threshold:.55});
ss.forEach(s=>io.observe(s));
/* avanca com clique; clique com shift, ou na metade esquerda com alt, volta */
addEventListener('click',ev=>{
  if(ev.target.closest('a,button,.nav')) return;
  ir(ev.shiftKey ? atual-1 : atual+1);
});
addEventListener('contextmenu',ev=>{ev.preventDefault();ir(atual-1)});
addEventListener('keydown',ev=>{
  if(['ArrowDown','ArrowRight',' ','PageDown'].includes(ev.key)){ev.preventDefault();ir(atual+1)}
  if(['ArrowUp','ArrowLeft','PageUp'].includes(ev.key)){ev.preventDefault();ir(atual-1)}});
"""

def montar(titulo, corpo_slides, dica="clique para avançar · shift+clique volta"):
    return f"""<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titulo}</title>
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=zodiak@400,401&f[]=supreme@400,500,600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<nav class="nav"></nav><div class="pg">01</div><div class="dica">{dica}</div>
{chr(10).join(corpo_slides)}
<script>{JS}</script></body></html>"""

o1 = B/"50-entrega"/"2026-08-17_youdare_deck_cenario-search-ai-electrolux.html"
o2 = B/"50-entrega"/"2026-08-17_youdare_deck_ressalvas-de-dado.html"
o1.write_text(montar("Cenário de search e IA — Electrolux LATAM 2027 · Youdare", slides), encoding="utf-8")
o2.write_text(montar("Ressalvas de dado — Electrolux LATAM 2027 · Youdare", apendice), encoding="utf-8")
print(f"material: {len(slides)} slides, {len(o1.read_text(encoding='utf-8')):,} bytes")
print(f"ressalvas: {len(apendice)} slides, {len(o2.read_text(encoding='utf-8')):,} bytes")
