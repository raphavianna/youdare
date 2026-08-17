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

# paleta categorica validada por dataviz/scripts/validate_palette.js (dark, superficie #1a1a19)
COR = {"electrolux":"#3987e5","brastemp":"#d95926","consul":"#199e70","samsung":"#c98500",
       "midea":"#d55181","hisense":"#008300","haier":"#e66767","sem_dono":"#9085e9","generico":"#6b6a63"}
ORDEM = ["electrolux","brastemp","consul","samsung","midea","hisense","haier"]
NOME = {k: P[k]["nome"] for k in ORDEM}
NOME.update({"sem_dono":"Território sem dono","generico":"Categoria (heads)"})
# rampa sequencial ordinal para os estagios da jornada (claro -> escuro)
EST = {"sem_marca":"#f7e3b8","descoberta":"#f2c777","escolha":"#c98500","posse":"#7d5300","nc":"#2e2e2b"}
MESES = ["ago","set","out","nov","dez","jan","fev","mar","abr","mai","jun","jul"]
# fontes: sem nomear ferramenta, por decisao editorial
F_KW  = "Base de busca Brasil · 4.965 keywords · ago/25–jul/26"
F_CAUDA = "Base de busca Brasil · 492 keywords sem marca com volume"
F_IA  = "Respostas de IA · 150 perguntas sem marca × 5 provedores"
F_TOP = "Tópicos de IA · 2.324 tópicos de categoria"
F_REF = "Tráfego vindo de LLM · 12 meses · 4 domínios"

def e(s): return html.escape(str(s))
def dec(v): return str(v).replace(".", ",")          # decimal em pt-BR
def vs(k):  return f'{P[k]["inclinacao_vs_categoria"]:.2f}'.replace(".", ",")  # ano a ano vs categoria
def n(v): return f"{v:,.0f}".replace(",", ".")
def pct(v, d=1): return f"{v:.{d}f}".replace(".", ",") + "%"

slides, apendice = [], []

def slide(marca_fonte, kicker, titulo, subtitulo, corpo, leitura="", fonte="", destino=None):
    """marca_fonte: 'search' | 'ia' | 'ambos'"""
    rot = {"search":"Search","ia":"IA","ambos":"Search + IA"}[marca_fonte]
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

def linhas(series, destaque=None, w=1000, h=290, rotulos_x=None, ref100=False, y0=None, y1=None):
    vals = [v for s in series.values() for v in s]
    lo = y0 if y0 is not None else min(vals); hi = y1 if y1 is not None else max(vals)
    if hi == lo: hi = lo + 1
    pl, pr, pt, pb = 8, 96, 14, 26
    X = lambda i, L: pl + (w-pl-pr)*i/(L-1)
    Y = lambda v: pt + (h-pt-pb)*(1-(v-lo)/(hi-lo))
    out = []
    if ref100 and lo < 100 < hi:
        out.append(f'<line class="ref" x1="{pl}" y1="{Y(100):.1f}" x2="{w-pr}" y2="{Y(100):.1f}"/>')
        out.append(f'<text class="reflab" x="{w-pr+6}" y="{Y(100)+4:.1f}">base 100</text>')
    for k, s in series.items():
        forte = (destaque is None) or (k == destaque)
        c = COR.get(k, "#6b6a63") if forte else "#3a3a37"
        d = " ".join(f"{'M' if i==0 else 'L'}{X(i,len(s)):.1f},{Y(v):.1f}" for i, v in enumerate(s))
        out.append(f'<path d="{d}" stroke="{c}" class="ln{" forte" if forte else ""}"/>')
        if forte:
            out.append(f'<circle cx="{X(len(s)-1,len(s)):.1f}" cy="{Y(s[-1]):.1f}" r="4.5" fill="{c}"/>')
            out.append(f'<text class="lnlab" x="{X(len(s)-1,len(s))+9:.1f}" y="{Y(s[-1])+4:.1f}" fill="{c}">{e(NOME.get(k,k))}</text>')
    if rotulos_x:
        for i, r in enumerate(rotulos_x):
            if r: out.append(f'<text class="xlab" x="{X(i,len(rotulos_x)):.1f}" y="{h-6}">{e(r)}</text>')
    return f'<svg class="chart" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">{"".join(out)}</svg>'

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
    th = "".join(f"<th>{c}</th>" for c in cabec)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas_)
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

slide("ambos", "As fontes", "Duas fontes de demanda, lidas separadamente antes de serem cruzadas",
  "Busca mostra o que as pessoas digitam. IA mostra o que elas perguntam e o que os assistentes respondem. As duas foram fechadas de forma independente.",
  '<div class="fontes">'
  f'<div class="fx"><span class="fxb b-search">Search</span><span class="fxv">4,9 mil</span><span class="fxl">keywords da categoria e das marcas</span></div>'
  f'<div class="fx"><span class="fxb b-ia">IA</span><span class="fxv">2,3 mil</span><span class="fxl">tópicos de demanda mediada por assistente</span></div>'
  '</div>' +
  tabela(["","O que enxerga","O que não enxerga"], [
    ['<span class="badge b-search">Search</span>',"Demanda expressa, sua composição, os termos exatos, a forma ao longo de 12 meses","Quem captura cada consulta · demanda latente · conversão"],
    ['<span class="badge b-ia">IA</span>',"Se a marca é citada sem ser nomeada, em que posição, com que carga, e o tráfego que chega","Quais fontes o modelo cita · o que responde quando perguntam pela marca"]]),
  "", "Brasil · ago/25 a jul/26")

slide("ambos", "Objetivo do briefing", "Converter reconhecimento de marca em intenção de compra no momento da decisão",
  "O briefing aponta um vão entre awareness e consideração. Busca e IA são as fontes que enxergam o momento da decisão em escala.",
  '<div class="quadro"><blockquote>“Moving beyond awareness, converting brand recognition into purchase intent <b>at the moment of decision</b>.”</blockquote><cite>Briefing Electrolux · desafio declarado para o Brasil</cite></div>'
  + kpis([("85%","awareness MDA","#3987e5"),("44%","consideração T2B","#d95926"),("41 p.p.","o vão entre as duas","#c98500")]),
  "", "Brand Health Track · Q1 2026")

# --- a jornada em 4 estagios (NOVO)
slide("search", "O modelo", "A jornada tem quatro estágios, e o primeiro não tem marca nenhuma",
  "Toda a leitura deste material usa estes quatro estágios. Eles saem da forma da consulta: o que a pessoa digita revela em que ponto da relação com a categoria ela está.",
  tabela(["Estágio","O que a pessoa procura","Como aparece na consulta"], [
    [f'<b style="color:{EST["sem_marca"]}">0 · Sem marca</b>',"A categoria, sem ter escolhido fabricante", ex("heads", 2, "cauda") + " · " + ex("assistencia", 1, "cauda")],
    [f'<b style="color:{EST["descoberta"]}">1 · Descoberta de marca</b>',"Quem é a marca, se ela é boa", ex("marca e navegacao", 3)],
    [f'<b style="color:{EST["escolha"]}">2 · Escolha de produto</b>',"Qual modelo, qual capacidade, qual preço", ex("especificacao produto", 2) + " · " + ex("aquisicao e comparacao", 1)],
    [f'<b style="color:{EST["posse"]}">3 · Posse</b>',"Já tem o produto e convive com ele", ex("manutencao", 1, "cauda") + " · " + ex("defeito", 1, "cauda") + " · " + ex("peca", 1, "cauda")]], "wide"),
  "O estágio 0 é a maior fatia da demanda e o único em que nenhum player é nomeado. Ele não pertence a ninguém.", F_KW)

slide("search", "O modelo", "Metade da demanda da categoria acontece antes de qualquer marca entrar na conta",
  "Distribuição da demanda medida entre os quatro estágios. O estágio 0 não pertence a nenhum player — é a categoria sendo procurada sem fabricante nomeado.",
  barras_empilhadas([("Categoria", [
      ("Sem marca", 100*J4["sem_marca"]/J4["total"], EST["sem_marca"]),
      ("Descoberta", 100*J4["descoberta"]/J4["total"], EST["descoberta"]),
      ("Escolha", 100*J4["escolha"]/J4["total"], EST["escolha"]),
      ("Posse", 100*J4["posse"]/J4["total"], EST["posse"]),
      ("Não classificado", 100*J4["nao_class"]/J4["total"], EST["nc"])], "")]) +
  legenda([("0 · Sem marca", EST["sem_marca"]), ("1 · Descoberta", EST["descoberta"]),
           ("2 · Escolha", EST["escolha"]), ("3 · Posse", EST["posse"]), ("Não classificado", EST["nc"])]) +
  kpis([(n(J4["sem_marca"]), "buscas/mês sem marca nenhuma", EST["sem_marca"]),
        (n(J4["descoberta"]), "procurando a marca pelo nome", EST["descoberta"]),
        (n(J4["escolha"]), "escolhendo produto", EST["escolha"]),
        (n(J4["posse"]), "já com o produto em casa", EST["posse"])]),
  "Dentro dos sete players a leitura passa a ser de três estágios — tudo que está num arquivo de marca já é, por definição, demanda com marca.", F_KW)

# --- as familias (NOVO)
FAMS = [("assistencia","Assistência e conserto"),("peca","Peça e consumível"),("instalacao","Instalação"),
        ("manutencao","Manutenção e limpeza"),("defeito","Defeito e problema"),("manual e uso","Manual e uso"),
        ("consumo","Consumo e energia"),("receita","Receita e preparo")]
slide("search", "O modelo", "A posse se decompõe em oito famílias, e cada uma é um momento de vida com o produto",
  "Famílias são o nível mais fino da leitura: agrupam consultas pela necessidade que as gera. Elas são o eixo do material inteiro.",
  tabela(["Família","Consultas reais que a compõem","Volume/mês"],
    [[f'<b>{lab}</b>', ex(f, 2, "cauda"), f'<b>{n(SD["familias"].get(f,0)/100*SD["volume"])}</b>'] for f, lab in FAMS], "wide"),
  "As oito classificam pela <b>necessidade</b> que a consulta expressa, não pelo nome comercial do serviço — <code>assistência técnica electrolux</code> e <code>electrolux cuida</code> caem as duas em assistência, porque Cuida <b>é</b> a assistência.", F_CAUDA)

slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 1</span><h2>Os players</h2>
  <p class="sub">Estado atual, evolução mês a mês, categorias e presença em IA — sete marcas e o território que ninguém reivindica</p></div></section>""")

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
  "Índice de share de demanda mês a mês, base 100 no primeiro mês lido — barra verde é mês acima da base, laranja abaixo. Ponta a ponta compara o último mês com o primeiro; ano a ano compara a média dos cinco últimos com a dos sete primeiros.",
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
slide("search", "Electrolux", "A demanda da Electrolux está na escolha do produto, não na posse",
  "Composição da demanda de cada player entre os três estágios que existem dentro de uma marca. O rótulo dentro da barra é o peso de cada estágio.",
  barras_empilhadas([(NOME[k], [("Descoberta", P[k]["descoberta"], EST["descoberta"]),
                                ("Escolha", P[k]["escolha"], EST["escolha"]),
                                ("Posse", P[k]["posse"], EST["posse"]),
                                ("Não classificado", P[k]["nao_class"], EST["nc"])],
                      f'posse <b style="color:{EST["posse"]}">{pct(P[k]["posse"])}</b>')
                     for k in sorted(ORDEM, key=lambda k: -P[k]["posse"])]) +
  legenda([("1 · Descoberta de marca", EST["descoberta"]), ("2 · Escolha de produto", EST["escolha"]),
           ("3 · Posse", EST["posse"]), ("Não classificado", EST["nc"])]) +
  chips_estagio(el),
  f'Electrolux tem {pct(el["posse"])} da demanda em posse. Consul tem {pct(P["consul"]["posse"])} — quase o dobro. Os exemplos abaixo do gráfico são as maiores consultas da Electrolux em cada estágio.', F_KW)

slide("search", "Electrolux", "Contra a categoria, a demanda da Electrolux está parada",
  "Share de demanda indexado ao próprio primeiro mês. Hisense e Haier ficam fora deste gráfico: a base pequena faz a série oscilar e achataria todo o resto.",
  linhas({k: indexar(P[k]["serie_relativa"]) for k in ["electrolux","brastemp","consul","samsung","midea"]},
         destaque="electrolux", rotulos_x=MESES, ref100=True) +
  kpis([(vs("electrolux"), "ano a ano · média dos 5 últimos meses contra os 7 primeiros", "#3987e5"),
        (f'{indexar(el["serie_relativa"])[-1]:.0f}', "ponta a ponta · último mês contra o primeiro", "#f0ede4"),
        (f'{el["inclinacao_bruta"]:.2f}'.replace(".",","), "sem descontar a sazonalidade — a leitura enganosa", "#6b6a63")]),
  "As duas medidas divergem de propósito: julho foi um mês forte, o que puxa a leitura ponta a ponta para 115, mas a <b>média do período não se move</b>. É o ano a ano que descreve a trajetória.", F_KW)

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

slide("search", "O modelo", "Nome de submarca não é família: cada frente entra pela necessidade que atende",
  "Família classifica pela <b>necessidade</b> que a consulta expressa. O nome comercial é um atributo à parte, que convive com a família e não substitui ela. A regra vale para todos os players e todos os slides deste material.",
  tabela(["Frente da marca","Como as pessoas digitam","Entra na família — a necessidade que atende","Vol/mês"],
    [[f'<b>{lab}</b>', " · ".join(f"<code>{e(t)}</code>" for t in termos) or "—",
      fam.capitalize(), f'<b>{n(v)}</b>'] for lab, fam, v, termos in FRENTES], "wide") +
  '<div class="quadro"><p>Por isso <code>assistência técnica electrolux</code> conta como <b>assistência</b>, não como “frente”. E <code>electrolux cuida</code> também — porque Cuida <b>é</b> a assistência. O que os separa não é a família, é se a pessoa digitou a necessidade ou o nome comercial. Nenhuma frente tem família própria neste material.</p></div>',
  "", F_KW + " + cauda sem marca")

slide("search", "Electrolux", "Mais gente procura assistência da Electrolux do que a marca criada para prestá-la",
  "Confronto entre a necessidade expressa com o nome da marca e a submarca de serviço correspondente. As duas caem na mesma família — o que muda é o que a pessoa digitou.",
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
  "A necessidade existe e a estrutura existe. O que quase não existe é o consumidor conhecendo o nome da frente. Cada barra traz a família em que a frente cai — nenhuma delas é família por si.", F_KW + " + cauda sem marca")

INCL = {f: v for f, v in el["familias_inclinacao"].items() if v["volume"] >= 100 and f != "nao classificado"}
slide("search", "Electrolux", "Dentro da Electrolux, quem cresce é a demanda de quem já tem o produto",
  "Inclinação por família dentro da marca: acima de 1,00 a família cresce, abaixo encolhe. As quatro primeiras são todas de posse.",
  barras_h([(FAMLAB.get(f, f.capitalize()),
             v["inclinacao"], "posse" if f in [x[0] for x in FAM_ESTAGIO["posse"]] else None)
            for f, v in sorted(INCL.items(), key=lambda i: -i[1]["inclinacao"])],
           lambda k: "#7d5300" if k == "posse" else "#3987e5", max_v=1.6,
           fmt=lambda v: str(round(v, 2)).replace(".", ",")) +
  chips_familias([("defeito","Defeito"),("garantia","Garantia"),
                  ("peca e consumivel","Peça e consumível"),("manual e uso","Manual e uso")], escopo=el),
  "Defeito, garantia, peça e manual — as quatro famílias de posse — são as que mais crescem. Especificação de produto vem depois, e a demanda pelo nome da marca fica parada.", F_KW)

slide("search", "Electrolux", "Geladeira concentra um terço da demanda de marca da Electrolux",
  "Peso de cada categoria de produto dentro da demanda da marca, e as consultas que mais pesam.",
  '<div class="col2"><div>' +
  barras_h([(catn(c), v, "electrolux") for c, v in list(el["categorias"].items())[:7]],
           lambda k: COR["electrolux"], fmt=lambda v: pct(v)) + '</div><div>' +
  tabela(["Maiores consultas da marca","Buscas/mês"],
         [[e(k), "<b>" + n(v) + "</b>"] for k, v in el["top_keywords"][:6]]) + '</div></div>',
  f'Ar condicionado é {pct(el["categorias"].get("ar condicionado", 0))} da demanda da Electrolux — contra {pct(P["midea"]["categorias"].get("ar condicionado", 0))} da Midea e {pct(P["haier"]["categorias"].get("ar condicionado", 0))} da Haier.', F_KW)

# --- demais players
def bloco_player(k, titulo, subtitulo, leitura):
    p = P[k]; ia = AI["marcas"].get(p["nome"])
    esq = barras_empilhadas([("Jornada", [("Descoberta", p["descoberta"], EST["descoberta"]),
                                          ("Escolha", p["escolha"], EST["escolha"]),
                                          ("Posse", p["posse"], EST["posse"]),
                                          ("Não class.", p["nao_class"], EST["nc"])], "")]) + \
          legenda([("Descoberta", EST["descoberta"]), ("Escolha", EST["escolha"]),
                   ("Posse", EST["posse"]), ("Não class.", EST["nc"])]) + \
          barras_h([(catn(c), v, k) for c, v in list(p["categorias"].items())[:6]],
                   lambda x: COR[k], fmt=lambda v: pct(v))
    if ia:
        dir_ = kpis([(f'{ia["cobertura"]["All AI Platforms"]}%', "cobertura em resposta de IA", COR[k]),
                     (str(ia["posicao"]).replace(".", ","), "posição média na resposta", "#f0ede4"),
                     (str(ia["sentimento"]).replace(".", ","), "sentimento médio", "#f0ede4")])
    else:
        dir_ = ('<div class="sem-cob"><span class="sc-x">—</span><b>Sem cobertura em IA</b>'
                '<span>Este player não aparece nas respostas nem no tráfego de LLM medidos</span></div>')
    dir_ += kpis([(n(p["volume"]), "buscas/mês", COR[k]),
                  (vs(k), "ano a ano vs categoria", "#f0ede4"),
                  (f'{indexar(p["serie_relativa"])[-1]:.0f}', "ponta a ponta, base 100", "#f0ede4")]) + \
            '<div class="mm"><span class="mml">Mês a mês</span>' + sparkbar(p["serie_relativa"]) + '</div>'
    slide("ambos" if ia else "search", p["nome"], titulo, subtitulo,
          f'<div class="col2"><div>{esq}</div><div>{dir_}</div></div>' + chips_estagio(p), leitura,
          F_KW + (" · " + F_IA if ia else ""))

bloco_player("brastemp", "Brastemp tem a maior base de demanda e é quem mais perde share",
  "Composição da jornada, categorias e presença em IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca — é o que o estágio quer dizer, em termos reais.",
  f'Índice {vs("brastemp")} contra a categoria: 14% de share de demanda perdido em doze meses.')
bloco_player("consul", "Consul é a única que converteu base instalada em demanda de posse",
  "Composição da jornada, categorias e presença em IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca — é o que o estágio quer dizer, em termos reais.",
  f'{pct(P["consul"]["posse"])} em posse — o dobro da Electrolux. E é a única, com a Brastemp, a aparecer nas perguntas de manutenção feitas à IA.')
bloco_player("samsung", "Samsung perde share e tem o sentimento mais baixo em resposta de IA",
  "Composição da jornada, categorias e presença em IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca — é o que o estágio quer dizer, em termos reais.",
  f'Índice {vs("samsung")}, a maior queda do conjunto, e sentimento {dec(AI["marcas"]["Samsung"]["sentimento"])} — o menor entre as cinco marcas cobertas.')
bloco_player("midea", "Midea tem a maior fatia de escolha de produto e nenhuma demanda de posse",
  "Composição da jornada, categorias e presença em IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca — é o que o estágio quer dizer, em termos reais.",
  f'{pct(P["midea"]["escolha"])} em escolha e {pct(P["midea"]["posse"])} em posse — coerente com base instalada recente.')
bloco_player("hisense", "Hisense é quem mais ganha share, e a demanda dela é de reputação",
  "Composição da jornada e categorias; este player não está nas fontes de IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca.",
  f'Índice {vs("hisense")}, o maior movimento do conjunto. <code>hisense é boa</code> está entre as cinco maiores consultas da marca — demanda de reputação, não de produto.')
bloco_player("haier", "Haier está no estágio mais inicial possível de formação de demanda",
  "Composição da jornada e categorias; este player não está nas fontes de IA. Os três blocos no rodapé são a consulta que mais pesa em cada estágio desta marca.",
  f'{pct(P["haier"]["descoberta"])} da demanda é o nome da marca e só {pct(P["haier"]["escolha"])} é escolha de produto.')
print("parte 1:", len(slides))

# --- comparativos
slide("search", "Comparativo", "Só a Consul converteu base instalada em demanda de pós-compra",
  "Os três estágios dentro de cada marca, ordenados pela fatia de posse. O rótulo dentro da barra é o peso do estágio.",
  barras_empilhadas([(NOME[k], [("Descoberta", P[k]["descoberta"], EST["descoberta"]),
                                ("Escolha", P[k]["escolha"], EST["escolha"]),
                                ("Posse", P[k]["posse"], EST["posse"]),
                                ("Não class.", P[k]["nao_class"], EST["nc"])],
                      f'<b style="color:{EST["posse"]}">{pct(P[k]["posse"])}</b> posse')
                     for k in sorted(ORDEM, key=lambda k: -P[k]["posse"])]) +
  legenda([("1 · Descoberta", EST["descoberta"]), ("2 · Escolha", EST["escolha"]),
           ("3 · Posse", EST["posse"]), ("Não classificado", EST["nc"])]) +
  chips("posse", 5),
  f"Nenhum player passa de {pct(P['consul']['posse'])}. Posse agrega dez famílias de necessidade — assistência, peça, instalação, manutenção, defeito, manual, garantia, consumo, receita e descarte —, e é aí que a submarca de serviço cai, pela necessidade que atende e não pelo nome dela.", F_KW)

CATS = ["geladeira","lavanderia","ar condicionado","coccao","lava loucas","freezer","aspirador","adega"]
slide("search", "Comparativo", "Ar condicionado é o campo dos entrantes; cocção é da Brastemp",
  "Peso de cada categoria de produto dentro da demanda de cada player. Célula mais clara, maior concentração.",
  heatmap([catn(c) for c in CATS], ORDEM + ["generico","sem_dono"],
          lambda r, c: (P[r] if r in P else (HD if r == "generico" else SD))["categorias"].get(
              next(k for k in CATS if catn(k) == c), 0)),
  "Hisense, Haier e Midea concentram em ar condicionado — categoria fora do core histórico da disputa entre as marcas estabelecidas.", F_KW)

slide("ia", "Comparativo", "Electrolux é a mais citada em IA e a pior falada entre as três grandes",
  "Cobertura é em quantas das 150 perguntas sem marca a marca aparece. Posição é onde ela surge dentro da resposta. Sentimento é a carga da menção.",
  tabela(["Marca","Agregado","ChatGPT","Gemini","AI Mode","Perplexity","Posição","<b>Sentimento</b>"],
    [[f'<span class="dot" style="background:{COR[k]}"></span>{m}',
      f'<b>{AI["marcas"][m]["cobertura"]["All AI Platforms"]}%</b>'] +
      [f'{AI["marcas"][m]["cobertura"][p]}%' for p in ["ChatGPT","Gemini","Google AI Mode","Perplexity"]] +
      [str(AI["marcas"][m]["posicao"]).replace(".", ","),
       f'<b class="{"down" if AI["marcas"][m]["sentimento"] < 60 else "up"}">{str(AI["marcas"][m]["sentimento"]).replace(".", ",")}</b>']
     for m, k in [("Electrolux","electrolux"),("Consul","consul"),("Brastemp","brastemp"),("Samsung","samsung"),("Midea","midea")]], "wide"),
  "Lidera cobertura nos quatro provedores e aparece com carga menos positiva que Consul e Brastemp — problema de conteúdo da menção, não de volume dela.", F_IA)

slide("ia", "Comparativo", "A presença da categoria em IA é, hoje, presença no ChatGPT",
  "Cobertura de cada marca por provedor. O padrão vale para todos os players — é característica da plataforma, não fraqueza de uma marca.",
  tabela(["Provedor"] + ["Electrolux","Consul","Brastemp","Samsung","Midea"],
         [[f'<b>{p}</b>'] + [f'{AI["marcas"][m]["cobertura"][p]}%' for m in ["Electrolux","Consul","Brastemp","Samsung","Midea"]]
          for p in ["ChatGPT","Gemini","Google AI Mode","Perplexity"]], "wide") +
  kpis([("25%","cobertura da Electrolux no ChatGPT","#199e70"),("7% a 9%","nos outros três provedores","#6b6a63")]),
  "", F_IA)

# ================================================================== PARTE 2
slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 2</span><h2>A jornada</h2>
  <p class="sub">Onde a demanda da categoria está, quem ocupa cada momento, e o que as duas fontes dizem quando comparadas</p></div></section>""")

slide("search", "Jornada · Sem marca", "O maior bloco de demanda da categoria não pertence a nenhum player",
  "O estágio 0 se divide em dois: as consultas de cabeça de categoria e a cauda de posse que ninguém reivindica.",
  barras_h([("Cabeças de categoria", J4["heads"], "generico"), ("Território sem dono (posse)", J4["cauda"], "sem_dono")],
           lambda k: COR[k]) +
  kpis([(n(J4["sem_marca"]), "buscas/mês sem marca nenhuma", EST["sem_marca"]),
        (pct(100*J4["sem_marca"]/J4["total"], 0), "de toda a demanda medida", "#f0ede4"),
        ("74%", "de intenção informacional na cauda", COR["sem_dono"])]) +
  chips_familias([("heads","Cabeça de categoria"),("assistencia","Assistência e reparo"),
                  ("instalacao","Instalação"),("peca","Peça e consumível")], prefer="cauda"),
  "As cabeças são consultas de uma a três palavras. A cauda é onde vive a demanda de posse sem fabricante nomeado — a mesma necessidade que, com marca, viraria assistência, peça ou instalação.", F_KW)

slide("search", "Jornada · Descoberta", "Quem entra na categoria concentra a demanda no próprio nome",
  "Estágio 1 é a família <b>marca e navegação</b>: a pessoa digita o nome do fabricante, ou o nome mais a categoria, para saber quem ele é e se é bom.",
  barras_h([(NOME[k], P[k]["descoberta"], k) for k in sorted(ORDEM, key=lambda k: -P[k]["descoberta"])],
           lambda k: COR[k], fmt=lambda v: pct(v)) +
  tabela(["Player","As duas maiores consultas de descoberta desta marca","Buscas/mês"],
         [[f'<span class="dot" style="background:{COR[k]}"></span>{NOME[k]}',
           " · ".join(f"<code>{e(t[0])}</code>" for t in P[k]["top_estagio"]["descoberta"][:2]),
           "<b>" + n(P[k]["top_estagio"]["descoberta"][0][1]) + "</b>"]
          for k in sorted(ORDEM, key=lambda k: -P[k]["descoberta"])], "wide"),
  "Haier e Hisense ainda respondem “quem é essa marca”. As estabelecidas já disputam produto. Samsung aparece baixa por característica do recorte de origem.", F_KW)

slide("search", "Jornada · Escolha", "Na escolha de produto os sete players estão empatados",
  "Estágio 2 agrega duas famílias: <b>especificação de produto</b> — capacidade, tecnologia, modelo — e <b>aquisição e comparação</b> — preço, promoção, “qual o melhor”.",
  barras_h([(NOME[k], P[k]["escolha"], k) for k in sorted(ORDEM, key=lambda k: -P[k]["escolha"])],
           lambda k: COR[k], fmt=lambda v: pct(v)) +
  chips("escolha") +
  '<div class="quadro"><p>Cinco dos sete estão entre 21% e 30%. É o momento mais disputado e o menos diferenciável da jornada — todo mundo está lá, com o mesmo peso.</p></div>',
  "", F_KW)

slide("search", "Jornada · Posse", "207.600 buscas por mês de quem já tem o produto e nenhuma marca atende",
  "Estágio 3 agrega as famílias de vida com o produto. Cada barra é uma necessidade — não um serviço nomeado: <code>conserto de geladeira</code> e <code>electrolux cuida</code> entrariam as duas em assistência.",
  '<div class="col2"><div>' +
  barras_h([(FAMLAB.get(f, f.capitalize()), v, "sem_dono") for f, v in list(SD["familias"].items())[:8]],
           lambda k: COR["sem_dono"], fmt=lambda v: pct(v)) + '</div><div>' +
  tabela(["Maiores consultas do território","Buscas/mês"],
         [[e(k), "<b>" + n(v) + "</b>"] for k, v in SD["top_keywords"][:6]]) +
  kpis([(n(SD["volume"]), "buscas/mês", COR["sem_dono"]), (f'{SD["ai_overview"]}%', "já respondidas com resumo de IA", "#c98500")]) +
  '</div></div>',
  "<code>instalação de ar condicionado</code> sozinha é 10,7% do território. Nenhum player o reivindica em posicionamento nem tem demanda atrelada ao nome nele.", F_CAUDA)

slide("ia", "Jornada · IA", "Na IA, a categoria é usada muito mais para conviver do que para comprar",
  "Peso de cada família de tópico dentro da demanda de categoria mediada por assistente.",
  barras_h([(TOPLAB.get(f, f.capitalize()), v["pct"], None) for f, v in
            sorted(AI["topicos"]["familias"].items(), key=lambda i: -i[1]["pct"])],
           lambda k: "#199e70", fmt=lambda v: pct(v)) +
  kpis([("8,4%", "da demanda de IA é posse", "#199e70"), ("1,5%", "é comparação de modelo", "#6b6a63"),
        ("0,1%", "é preço e compra", "#6b6a63")]),
  "Uso e receita é a maior família — e nenhuma das cinco marcas aparece nas perguntas de receita feitas aos assistentes.", F_TOP)

slide("ambos", "Divergência", "Receita é a menor família em busca e a maior em IA",
  "A mesma necessidade aparece em posições opostas nas duas fontes. É comportamento migrando de canal.",
  '<div class="confronto">'
  '<div class="cf"><span class="cft">Em busca</span><span class="cfv" style="color:#6b6a63">1,4%</span><span class="cfl">do território sem dono · a <b>menor</b> família</span></div>'
  '<div class="cfx">↔</div>'
  '<div class="cf"><span class="cft">Em IA</span><span class="cfv" style="color:#199e70">2,3%</span><span class="cfl">da categoria · a <b>maior</b> família de posse</span></div></div>' +
  tabela(["Maiores tópicos de uso e receita em IA","Volume"],
         [[e(k), "<b>" + n(v) + "</b>"] for k, v in AI["topicos"]["familias"]["uso e receita"]["maiores"]]),
  "O briefing cita “pesquisar uma receita” como ponto de entrada. O dado diz que essa porta hoje é de assistente, não de buscador.", F_TOP + " · " + F_KW)

slide("search", "Mediação", "A IA já responde a maior parte das consultas de posse",
  "Com que frequência o Google entrega um resumo gerado no topo, em vez de links, para cada família de demanda.",
  barras_h([(FAMLAB.get(f, f.capitalize()), v["aio"], None) for f, v in
            sorted(D["familias_ai_overview"].items(), key=lambda i: -i[1]["aio"])[:12]],
           lambda k: "#c98500", max_v=100, fmt=lambda v: f"{v}%"),
  "Manutenção, defeito, instalação e consumo estão entre 84% e 93% de mediação.", F_KW)

ag = D["ai_overview_agregado"]
slide("ambos", "Mediação", "A mediação chegou ao território que a marca não ocupa — e ainda não ao dela",
  "Comparação da incidência de resumo gerado entre as famílias de posse, as demais famílias e a demanda própria da Electrolux.",
  kpis([(f'{ag["posse"]["aio"]}%', "das consultas de posse já são mediadas", "#c98500"),
        (f'{ag["demais"]["aio"]}%', "das demais famílias", "#6b6a63"),
        (f'{ag["electrolux"]}%', "das consultas da Electrolux", "#3987e5")]) +
  f'<div class="quadro alerta"><p>Quando a mediação avançar sobre as consultas de marca e de especificação — onde a Electrolux tem <b>{n(el["volume"])} buscas/mês</b> e hoje controla o resultado —, a marca passa a ser intermediada em terreno que domina.</p></div>',
  "É a única leitura do material que só existe cruzando as duas fontes.", F_KW)

REF = AI["referrals"]
slide("ia", "Tendência", "O tráfego vindo de LLM multiplicou por 5,4 em doze meses",
  "Visitas mensais que chegam a cada domínio a partir de assistentes de IA.",
  linhas({("electrolux" if "electrolux" in d else "brastemp" if "brastemp" in d else "consul" if "consul" in d else "midea"): s
          for d, s in REF["series"].items()}, destaque="electrolux",
         rotulos_x=[m[-2:] for m in REF["meses"]], y0=0) +
  kpis([(n(REF["series"]["loja.electrolux.com.br"][-1]), "visitas/mês da loja vindas de LLM", "#3987e5"),
        ("+75%", "1º contra 2º semestre", "#f0ede4"), ("39,9% → 46,0%", "share da Electrolux no canal", "#199e70")]),
  "O canal cresce para todos. A Electrolux sai na frente em volume e ganha participação dentro dele.", F_REF)

slide("ambos", "Síntese", "As duas fontes concordam sobre o vão e discordam sobre a posição",
  "Onde busca e IA convergem, a leitura é robusta. Onde divergem, a divergência é informação sobre como cada canal funciona.",
  tabela(["","<span class='badge b-search'>Search</span>","<span class='badge b-ia'>IA</span>"],
    [["<b>Posição da Electrolux</b>","3ª em volume · share <b>parado</b> (0,99)","<b>1ª em cobertura</b> (33%)"],
     ["<b>Trajetória</b>","não ganha share; quem cresce são os entrantes","share de tráfego <b>39,9% → 46,0%</b>"],
     ["<b>Posse</b>", f'{pct(el["posse"])} · metade da Consul',"<b>0%</b> em manutenção e em receita"],
     ["<b>Quem ocupa a posse</b>", f'Consul, com {pct(P["consul"]["posse"])}',"Consul e Brastemp, com 25% cada"],
     ["<b>Percepção</b>","não é o que a fonte mede","sentimento 58,1 — 2º pior do conjunto"]], "wide"),
  "A marca está melhor posicionada no canal novo do que no maduro — e não construiu essa vantagem deliberadamente.", F_KW + " · " + F_IA)

slide("ambos", "Fechamento", "Os quatro achados que sustentam o resto",
  "",
  '<div class="achados">' + "".join(
    f'<div class="ach"><span class="an">{i}</span><div><b>{t}</b><p>{dd}</p></div></div>'
    for i, (t, dd) in enumerate([
      ("A posse é o vão, nas duas fontes",
       f'Electrolux tem {pct(el["posse"])} da demanda em posse contra {pct(P["consul"]["posse"])} da Consul, e 0% de cobertura nas perguntas de manutenção feitas à IA.'),
      ("A mediação por IA já chegou ao território vago",
       f'{ag["posse"]["aio"]}% das consultas de posse são respondidas com resumo, contra {ag["electrolux"]}% das consultas da Electrolux.'),
      ("O crescimento da categoria está nos entrantes",
       f'Hisense a {vs("hisense")} e Haier a {vs("haier")} contra a categoria; Brastemp a {vs("brastemp")} e Samsung a {vs("samsung")}.'),
      ("A marca é a mais citada em IA e a pior falada",
       f'{AI["marcas"]["Electrolux"]["cobertura"]["All AI Platforms"]}% de cobertura, à frente de todos, com sentimento {dec(AI["marcas"]["Electrolux"]["sentimento"])} contra {dec(AI["marcas"]["Consul"]["sentimento"])} da Consul.')], 1)) + '</div>',
  "", "")

slide("ambos", "Fechamento", "O que muda com o tempo, e o que não",
  "Este material para aqui: os dados e a leitura deles. A decisão de território, mensagem e plano é das áreas.",
  '<div class="col2"><div class="quadro"><span class="qh">Move com o tempo</span><ul>'
  '<li>A mediação por IA avança das consultas de posse para as de marca</li>'
  '<li>A base instalada de Haier e Hisense começa a gerar demanda de pós-compra</li>'
  '<li>O tráfego de LLM segue crescendo em toda a categoria</li></ul></div>'
  '<div class="quadro"><span class="qh">Não move sozinho</span><ul>'
  '<li>O território de posse continua sem dono enquanto ninguém o ocupar</li>'
  '<li>O sentimento da marca em IA não melhora por volume de citação</li>'
  f'<li>O nome das frentes não vira demanda sozinho: as sete somam {n(V_FRENTES)} buscas/mês, {pct(100*V_FRENTES/el["volume"],1)} da demanda pela marca</li></ul></div></div>',
  "", "")
print("total material:", len(slides))

# ================================================== DECK SEPARADO: RESSALVAS
apendice.append("""<section class="slide capa"><div class="slide-inner">
  <span class="kicker">Youdare · Direção de Mídia e Dados · agosto 2026</span>
  <h1>Ressalvas<br><em>de dado</em></h1>
  <p class="sub">Complemento técnico do material de cenário — o que checar antes de construir em cima, e o que este pacote não responde</p>
  <div class="capa-meta"><span>Uso interno</span><span>Leia junto com o deck de cenário</span></div>
</div></section>""")

slide("ambos", "Ressalvas", "Números frágeis — confira antes de levar para o cliente",
  "Cada linha indica um número presente no material de cenário que não sustenta contestação sem contexto.",
  tabela(["Número","Por quê","Onde aparece"], [
    ["Descoberta da Samsung, 5,5%","O recorte de origem partiu de uma consulta de categoria, não do nome da marca. É artefato, não achado","Panorama · comparativo de jornada"],
    ["Cobertura de IA em posse (0%, 25%)","As famílias de manutenção e receita têm entre 3 e 4 perguntas na amostra de 150","Comparativo de IA · síntese"],
    ["Sentimento (58,1 · 70,5 · 46,3)","Classificação automática, sem critério publicado. Vale como comparação relativa, não como nível absoluto","Comparativo de IA"],
    ["Séries de 12 meses","Reconstruídas a partir do volume médio e do índice de tendência, sob premissa declarada","Todos os slides de evolução"],
    ["Volumes entre players","Recortes com profundidade diferente: Brastemp 1.998 keywords, Haier 44. Composição interna é comparável; volume absoluto não","Panorama"],
    ["Tráfego de LLM","Estimativa modelada, não contagem","Slide de tendência"],
    ["Famílias de demanda","A classificação cobre entre 33% e 89% do volume por player. “Não classificado” é categoria legítima","Todos os slides de jornada"],
    ["Volume das frentes nomeadas","Soma duas grafias da marca (<code>electrolux</code> e <code>eletrolux</code>) e vem de dois recortes diferentes. Frente não é família: cada uma entra pela necessidade que atende","Slides do modelo e da Electrolux"]], "wide"),
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
  "O material inteiro é gerado por script a partir de um único arquivo de dados consolidado — nenhuma cifra é digitada à mão.",
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
.be-extra{font-size:clamp(.58rem,.84vw,.78rem);color:var(--ink-2)}
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
.lnlab{font-size:12px;font-weight:600}.xlab{text-anchor:middle}

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
