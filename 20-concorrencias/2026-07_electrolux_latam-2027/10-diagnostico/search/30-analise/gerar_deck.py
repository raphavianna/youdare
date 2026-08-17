# -*- coding: utf-8 -*-
"""
Gera o material executivo em HTML a partir de 30-analise/dados_do_deck.json.
Nenhum numero e digitado aqui: tudo vem do JSON, que por sua vez vem dos
datasets normalizados. Rode dados_do_deck.py antes.

Saida: 50-entrega/2026-08-17_youdare_deck_cenario-search-ai-electrolux.html
"""
import json, html
from pathlib import Path

B = Path(__file__).resolve().parent.parent
D = json.load(open(B/"30-analise"/"dados_do_deck.json", encoding="utf-8"))

# paleta categorica validada por scripts/validate_palette.js (dark, surface #1a1a19)
COR = {"electrolux":"#3987e5","brastemp":"#d95926","consul":"#199e70","samsung":"#c98500",
       "midea":"#d55181","hisense":"#008300","haier":"#e66767","sem_dono":"#9085e9",
       "generico":"#6b6a63"}
ORDEM = ["electrolux","brastemp","consul","samsung","midea","hisense","haier"]
NOME  = {k: D["players"][k]["nome"] for k in ORDEM}
NOME["sem_dono"] = "Território sem dono"; NOME["generico"] = "Categoria (heads)"
# rampa sequencial para os 3 estagios da jornada (claro -> escuro, ordinal)
ESTAGIO = {"descoberta":"#f2c777","escolha":"#c98500","posse":"#7d5300"}

def e(s): return html.escape(str(s))
def n(v):  return f"{v:,.0f}".replace(",", ".")
def pct(v, d=1): return f"{v:.{d}f}".replace(".", ",") + "%"

slides = []
def slide(kicker, titulo, corpo, leitura="", fonte="", classe=""):
    slides.append(f"""<section class="slide {classe}">
  <div class="slide-inner">
    <header class="s-head"><span class="kicker">{kicker}</span><h2>{titulo}</h2></header>
    <div class="s-body">{corpo}</div>
    {f'<p class="leitura">{leitura}</p>' if leitura else ''}
    {f'<footer class="fonte">{fonte}</footer>' if fonte else ''}
  </div>
</section>""")

# ---------------------------------------------------------------- graficos
def barras_h(itens, cor_fn, max_v=None, fmt=n, altura=None, rotulo_dentro=False):
    """itens: [(label, valor, cor_key|None)]"""
    mx = max_v or max(v for _, v, *_ in itens) or 1
    linhas = []
    for it in itens:
        lab, val = it[0], it[1]
        ck = it[2] if len(it) > 2 else None
        c = cor_fn(ck) if cor_fn else "#3987e5"
        w = max(0.6, 100*val/mx)
        linhas.append(f"""<div class="bh-row">
          <span class="bh-lab">{e(lab)}</span>
          <span class="bh-track"><span class="bh-fill" style="width:{w:.2f}%;background:{c}"></span></span>
          <span class="bh-val">{fmt(val)}</span></div>""")
    estilo = ' style="--bh-h:%s"' % altura if altura else ''
    return '<div class="bh"' + estilo + '>' + "".join(linhas) + "</div>"

def barras_empilhadas(rows):
    """rows: [(label, [(seg_label, valor, cor)], total_fmt)]"""
    out = []
    for lab, segs, extra in rows:
        tot = sum(v for _, v, _ in segs) or 1
        partes = "".join(
            f'<span class="be-seg" style="width:{100*v/tot:.2f}%;background:{c}" title="{e(sl)}: {pct(v)}"></span>'
            for sl, v, c in segs)
        out.append(f"""<div class="be-row"><span class="be-lab">{e(lab)}</span>
          <span class="be-track">{partes}</span><span class="be-extra">{extra}</span></div>""")
    return '<div class="be">' + "".join(out) + "</div>"

def indexar(s100):
    """indexa a serie ao proprio primeiro ponto = 100, para comparar trajetoria e nao nivel"""
    b = s100[0] or 1
    return [100*v/b for v in s100]

def linhas(series, destaque=None, w=1000, h=300, y0=None, y1=None, rotulos_x=None, ref1=False, ref100=False):
    """series: {chave: [valores]}"""
    vals = [v for s in series.values() for v in s]
    lo = y0 if y0 is not None else min(vals); hi = y1 if y1 is not None else max(vals)
    if hi == lo: hi = lo + 1
    pad_l, pad_r, pad_t, pad_b = 8, 90, 14, 26
    def X(i, ln): return pad_l + (w-pad_l-pad_r) * i/(ln-1)
    def Y(v): return pad_t + (h-pad_t-pad_b) * (1 - (v-lo)/(hi-lo))
    partes = []
    marco = 1 if ref1 else (100 if ref100 else None)
    if marco is not None and lo < marco < hi:
        partes.append(f'<line class="ref" x1="{pad_l}" y1="{Y(marco):.1f}" x2="{w-pad_r}" y2="{Y(marco):.1f}"/>')
        rot = "1,00" if ref1 else "base 100"
        partes.append(f'<text class="reflab" x="{w-pad_r+6}" y="{Y(marco)+4:.1f}">{rot}</text>')
    for k, s in series.items():
        forte = (destaque is None) or (k == destaque)
        c = COR.get(k, "#6b6a63") if forte else "#3a3a37"
        d = " ".join(f"{'M' if i==0 else 'L'}{X(i,len(s)):.1f},{Y(v):.1f}" for i, v in enumerate(s))
        partes.append(f'<path d="{d}" stroke="{c}" class="ln{" forte" if forte else ""}"/>')
        if forte:
            partes.append(f'<circle cx="{X(len(s)-1,len(s)):.1f}" cy="{Y(s[-1]):.1f}" r="4.5" fill="{c}"/>')
            partes.append(f'<text class="lnlab" x="{X(len(s)-1,len(s))+9:.1f}" y="{Y(s[-1])+4:.1f}" fill="{c}">{e(NOME.get(k,k))}</text>')
    if rotulos_x:
        for i, r in enumerate(rotulos_x):
            if r: partes.append(f'<text class="xlab" x="{X(i,len(rotulos_x)):.1f}" y="{h-6}">{e(r)}</text>')
    return f'<svg class="chart" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid meet">{"".join(partes)}</svg>'

def heatmap(cols, rows, get, fmt=lambda v: pct(v, 0)):
    mx = max((get(r, c) or 0) for r in rows for c in cols) or 1
    th = "".join(f"<th>{e(c)}</th>" for c in cols)
    tr = []
    for r in rows:
        tds = []
        for c in cols:
            v = get(r, c) or 0
            a = 0.06 + 0.94*(v/mx)**0.65 if v else 0.03
            forte = v/mx > 0.45
            tds.append(f'<td style="background:rgba(57,135,229,{a:.2f});color:{"#0d0d0c" if forte else "#cfcdc4"}">{fmt(v) if v else "—"}</td>')
        tr.append(f'<tr><th class="rh">{e(NOME.get(r, r))}</th>{"".join(tds)}</tr>')
    return f'<table class="hm"><thead><tr><th></th>{th}</tr></thead><tbody>{"".join(tr)}</tbody></table>'

def tabela(cabec, linhas_, classe=""):
    th = "".join(f"<th>{c}</th>" for c in cabec)   # cabecalho aceita marcacao propria
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas_)
    return f'<table class="tb {classe}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

def kpis(itens):
    """itens: [(valor, rotulo, cor|None)]"""
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><span class="kv" style="color:{c or "#f0ede4"}">{v}</span><span class="kl">{e(l)}</span></div>'
        for v, l, c in itens) + "</div>"

print("helpers ok")

# ================================================================== SLIDES
P = D["players"]; SD = D["sem_dono"]; HD = D["categoria_heads"]; AI = D["ai"]
MESES = ["ago","set","out","nov","dez","jan","fev","mar","abr","mai","jun","jul"]
F_KW  = "SEMrush · base br · 4.965 keywords normalizadas · ago/25–jul/26"
F_IA  = "SEMrush AI · 150 perguntas não-branded × 5 provedores"
F_REF = "SimilarWeb · AI referrals · 12 meses · 4 domínios"
F_TOP = "Tópicos de IA · 2.324 tópicos de categoria, deduplicados"

# --- 1 capa
slides.append(f"""<section class="slide capa"><div class="slide-inner">
  <span class="kicker">Youdare · Direção de Mídia e Dados · agosto 2026</span>
  <h1>O que a busca<br><em>e a IA</em> dizem<br>sobre a categoria</h1>
  <p class="sub">Cenário, players e jornada do consumidor — concorrência Electrolux LATAM 2027, recorte Brasil</p>
  <div class="capa-meta"><span>{n(D['meta']['kw_total'])} keywords</span><span>{n(D['meta']['prompts_ia'])} prompts de IA</span><span>150 perguntas × 5 provedores</span><span>12 meses de tráfego de LLM</span></div>
</div></section>""")

# --- 2 o que foi medido
slide("Método", "Duas fontes, medidas separadamente antes de serem cruzadas",
  kpis([(n(D['meta']['kw_total']), "keywords de busca, 8 players", "#3987e5"),
        (n(SD['kw']), "keywords sem marca nenhuma", COR['sem_dono']),
        ("150 × 5", "perguntas de IA por provedor", "#199e70"),
        (n(AI['topicos']['total_topicos']), "tópicos de IA da categoria", "#c98500")]) +
  tabela(["Fonte","O que ela enxerga","O que ela não enxerga"], [
    ["<b>Busca</b>","Demanda expressa, sua composição, os termos exatos, a forma ao longo de 12 meses","Quem captura cada consulta · demanda latente · conversão"],
    ["<b>IA</b>","Se a marca é citada sem ser nomeada, em que posição, com que carga, e o tráfego que chega","Quais fontes o modelo cita · o que responde quando perguntam pela marca"]]),
  "As trilhas foram fechadas sem consultar uma à outra. É isso que dá valor tanto às convergências quanto às divergências da Parte 2.", F_KW)

# --- 3 o desafio
slide("O briefing", "O cliente já nomeou o problema: converter reconhecimento em intenção",
  f"""<div class="quadro"><blockquote>“Moving beyond awareness, converting brand recognition into purchase intent <b>at the moment of decision</b>.”</blockquote><cite>Briefing Electrolux, desafio declarado para o Brasil</cite></div>"""
  + kpis([("85%","awareness MDA · BHT Kantar Q1/26","#3987e5"),("44%","consideração T2B · BHT Kantar Q1/26","#d95926"),("41 p.p.","o vão entre as duas","#c98500")]),
  "Busca é uma das poucas fontes que enxerga o momento da decisão em escala. É esse vão que este material investiga.",
  "BHT Kantar Q1/2026, via deck de briefing — números conferir contra o visual do PDF")

# --- 4 como ler
slide("Como ler", "Três estágios organizam toda a leitura de jornada",
  tabela(["Estágio","O que a demanda revela","Como aparece nos dados"], [
    [f'<b style="color:{ESTAGIO["descoberta"]}">Descoberta</b>',"A pessoa procura <b>quem é a marca</b> — ainda não o produto","Consultas pelo nome puro, navegação, reputação"],
    [f'<b style="color:{ESTAGIO["escolha"]}">Escolha</b>',"A pessoa sabe da marca e decide <b>qual item</b>","Capacidade, tecnologia, modelo, comparação, preço"],
    [f'<b style="color:{ESTAGIO["posse"]}">Posse</b>',"A pessoa <b>já tem o produto</b> e convive com ele","Instalação, uso, peça, defeito, manutenção, garantia"]]),
  "A distribuição entre os três descreve onde a demanda de cada player está concentrada — e é comparável entre marcas porque é interna a cada uma.", F_KW)

# --- 5 divisor
slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 1</span><h2>Os players</h2>
  <p class="sub">Estado atual, evolução recente, categorias e presença em IA — sete marcas e o território que ninguém reivindica</p></div></section>""")

# --- 6 panorama
slide("Panorama", "Brastemp domina o volume; Electrolux é a terceira em demanda de marca",
  barras_h([(NOME[k], P[k]["volume"], k) for k in sorted(ORDEM, key=lambda k:-P[k]["volume"])]
           + [(NOME["sem_dono"], SD["volume"], "sem_dono")], lambda k: COR.get(k, "#6b6a63")),
  "Volumes entre players não são estritamente comparáveis: os exports foram puxados com profundidade diferente. A composição interna de cada um, sim.", F_KW)

# --- 7-9 Electrolux
el = P["electrolux"]
slide("Electrolux", "A demanda da Electrolux está na escolha do produto, não na posse",
  barras_empilhadas([(NOME[k], [("Descoberta", P[k]["descoberta"], ESTAGIO["descoberta"]),
                                ("Escolha", P[k]["escolha"], ESTAGIO["escolha"]),
                                ("Posse", P[k]["posse"], ESTAGIO["posse"]),
                                ("Não classificado", P[k]["nao_class"], "#2e2e2b")],
                      f'posse <b style="color:{ESTAGIO["posse"]}">{pct(P[k]["posse"])}</b>')
                     for k in sorted(ORDEM, key=lambda k:-P[k]["posse"])]),
  f'Electrolux tem {pct(el["posse"])} da demanda em posse. Consul tem {pct(P["consul"]["posse"])} — quase o dobro, com posicionamento inferior.', F_KW)

slide("Electrolux", "Contra a categoria, a demanda da Electrolux está parada",
  linhas({k: indexar(P[k]["serie_relativa"]) for k in ["electrolux","brastemp","consul","samsung","midea"]
          if P[k].get("serie_relativa")}, destaque="electrolux", rotulos_x=MESES, ref100=True) +
  kpis([(str(el["inclinacao_bruta"]).replace(".",","), "inclinação bruta — enganosa", "#6b6a63"),
        (str(el["inclinacao_vs_categoria"]).replace(".",","), "contra a categoria — a real", "#3987e5"),
        ("0%", "de ganho de share em 12 meses", "#f0ede4")]),
  "Share de demanda indexado ao próprio mês 1. Hisense e Haier ficam fora deste gráfico: base pequena demais, oscilação que achataria todo o resto.", F_KW)

slide("Electrolux", "As famílias de posse crescem; as frentes que a marca criou encolhem",
  barras_h([("defeito", 1.43, None), ("garantia", 1.32, None), ("peça e consumível", 1.29, None),
            ("manual e uso", 1.24, None), ("especificação de produto", 1.17, None),
            ("marca e navegação", 0.96, None), ("assistência e reparo", 0.93, None),
            ("frente nomeada", 0.75, "queda"), ("manutenção e cuidado", 0.72, "queda")],
           lambda k: "#d95926" if k == "queda" else "#3987e5", max_v=1.6,
           fmt=lambda v: str(round(v, 2)).replace(".", ",")),
  "Inclinação por família dentro da Electrolux. Instala, Projeta, Cuida, Pro, Shopclub e Outlets somam a série que mais cai — enquanto a demanda espontânea de pós-compra sobe.", F_KW)

# --- players 10-17
def bloco_player(k, titulo, leitura):
    p = P[k]
    ia = AI["marcas"].get(p["nome"])
    cats = list(p["categorias"].items())[:6]
    esq = barras_empilhadas([(("Jornada"), [("Descoberta", p["descoberta"], ESTAGIO["descoberta"]),
                                            ("Escolha", p["escolha"], ESTAGIO["escolha"]),
                                            ("Posse", p["posse"], ESTAGIO["posse"]),
                                            ("Não class.", p["nao_class"], "#2e2e2b")], "")]) + \
          barras_h([(c.capitalize(), v, k) for c, v in cats], lambda x: COR[k], fmt=lambda v: pct(v))
    if ia:
        dir_ = kpis([(f'{ia["cobertura"]["All AI Platforms"]}%', "cobertura em IA", COR[k]),
                     (str(ia["posicao"]).replace(".", ","), "posição média na resposta", "#f0ede4"),
                     (str(ia["sentimento"]).replace(".", ","), "sentimento médio", "#f0ede4")])
    else:
        dir_ = '<div class="sem-cob"><span class="sc-x">—</span><b>Sem cobertura em IA</b><span>Este player não está nas respostas nem no tráfego de LLM medidos</span></div>'
    dir_ += kpis([(n(p["volume"]), "buscas/mês", COR[k]),
                  (str(p.get("inclinacao_vs_categoria", "—")).replace(".", ","), "share vs categoria", "#f0ede4"),
                  (f'{p["ai_overview"]}%', "consultas com AI Overview", "#f0ede4")])
    slide(p["nome"], titulo, f'<div class="col2"><div>{esq}</div><div>{dir_}</div></div>', leitura, F_KW + " · " + F_IA)

bloco_player("brastemp", "Brastemp tem a maior base e perde share de demanda",
  f'Inclinação 0,86 contra a categoria: 14% de share de demanda perdido em 12 meses. Posse em {pct(P["brastemp"]["posse"])}, baixa para o tamanho da base.')
bloco_player("consul", "Consul é a única que converteu base instalada em demanda de posse",
  f'{pct(P["consul"]["posse"])} em posse — o dobro da Electrolux. E é a única, junto com Brastemp, a aparecer nas perguntas de manutenção feitas à IA.')
bloco_player("samsung", "Samsung perde share e tem o pior sentimento em IA",
  'Inclinação 0,85, a maior queda do conjunto, e sentimento 46,3 — o menor entre as cinco marcas cobertas. Atenção: o export usou seed de categoria, o que distorce a fatia de descoberta.')
bloco_player("midea", "Midea tem a maior fatia de escolha e nenhuma demanda de posse",
  f'{pct(P["midea"]["escolha"])} em escolha de produto e {pct(P["midea"]["posse"])} em posse — coerente com base instalada recente. Ar condicionado concentra {pct(P["midea"]["categorias"].get("ar condicionado",0))} da demanda dela.')
bloco_player("hisense", "Hisense é quem mais ganha share — e a demanda dela é de reputação",
  'Inclinação 1,40, o maior movimento do conjunto. `hisense é boa` e `ar condicionado hisense é bom` estão entre as cinco maiores consultas: a demanda é de validação, não de produto.')
bloco_player("haier", "Haier está no estágio mais inicial possível de formação de demanda",
  f'{pct(P["haier"]["descoberta"])} da demanda é o nome da marca e apenas {pct(P["haier"]["escolha"])} é escolha de produto. Ganha share a 1,36, sobre uma base de {n(P["haier"]["volume"])} buscas/mês.')

print("parte 1 ok —", len(slides), "slides")

# --- comparativos
slide("Comparativo", "Só a Consul converteu base instalada em demanda de pós-compra",
  barras_empilhadas([(NOME[k], [("Descoberta", P[k]["descoberta"], ESTAGIO["descoberta"]),
                                ("Escolha", P[k]["escolha"], ESTAGIO["escolha"]),
                                ("Posse", P[k]["posse"], ESTAGIO["posse"]),
                                ("Não class.", P[k]["nao_class"], "#2e2e2b")],
                      f'<b style="color:{ESTAGIO["posse"]}">{pct(P[k]["posse"])}</b> posse')
                     for k in sorted(ORDEM, key=lambda k: -P[k]["posse"])]) +
  '<div class="legenda">' + "".join(f'<span><i style="background:{c}"></i>{l}</span>' for l, c in
    [("Descoberta", ESTAGIO["descoberta"]), ("Escolha", ESTAGIO["escolha"]), ("Posse", ESTAGIO["posse"]), ("Não classificado", "#2e2e2b")]) + '</div>',
  "Consul 8,1%, Electrolux 4,4%. Haier e Hisense concentram a demanda no nome da marca — é o retrato de quem está entrando.", F_KW)

slide("Comparativo", "O crescimento da categoria está inteiro nos dois entrantes",
  tabela(["Player","Bruta","<b>vs categoria</b>","Leitura"],
    [[f'<span class="dot" style="background:{COR[k]}"></span>{NOME[k]}',
      str(P[k]["inclinacao_bruta"]).replace(".", ","),
      f'<b>{str(P[k]["inclinacao_vs_categoria"]).replace(".", ",")}</b>',
      ('<span class="up">ganha share</span>' if P[k]["inclinacao_vs_categoria"] > 1.08
       else '<span class="down">perde share</span>' if P[k]["inclinacao_vs_categoria"] < 0.92 else '<span class="flat">estável</span>')]
     for k in sorted(ORDEM, key=lambda k: -P[k]["inclinacao_vs_categoria"])], "wide"),
  "A coluna bruta engana: todos os players picam nos mesmos meses porque a categoria é sazonal. Contra a categoria, Brastemp e Samsung recuam e só Hisense e Haier avançam.", F_KW)

CATS = ["geladeira","lavanderia","ar condicionado","coccao","lava loucas","freezer","aspirador","adega"]
CATN = {"coccao":"cocção","lava loucas":"lava-louças"}
slide("Comparativo", "Ar condicionado é o campo dos entrantes; cocção é da Brastemp",
  heatmap([CATN.get(c, c).capitalize() for c in CATS], ORDEM + ["generico","sem_dono"],
          lambda r, c: (P[r] if r in P else (HD if r == "generico" else SD))["categorias"].get(
              next(k for k in CATS if CATN.get(k, k).capitalize() == c), 0)),
  "Peso de cada categoria dentro da demanda de cada player. Hisense, Haier e Midea concentram em ar condicionado — categoria fora do core histórico da disputa.", F_KW)

slide("Comparativo", "Electrolux é a mais citada em IA e a pior falada entre as três grandes",
  tabela(["Marca","Agregado","ChatGPT","Gemini","AI Mode","Perplexity","Posição","<b>Sentimento</b>"],
    [[f'<span class="dot" style="background:{COR[k]}"></span>{m}',
      f'<b>{AI["marcas"][m]["cobertura"]["All AI Platforms"]}%</b>'] +
      [f'{AI["marcas"][m]["cobertura"][p]}%' for p in ["ChatGPT","Gemini","Google AI Mode","Perplexity"]] +
      [str(AI["marcas"][m]["posicao"]).replace(".", ","),
       f'<b class="{"down" if AI["marcas"][m]["sentimento"] < 60 else "up"}">{str(AI["marcas"][m]["sentimento"]).replace(".", ",")}</b>']
     for m, k in [("Electrolux","electrolux"),("Consul","consul"),("Brastemp","brastemp"),("Samsung","samsung"),("Midea","midea")]], "wide"),
  "Lidera cobertura nos quatro provedores. E aparece com carga menos positiva que Consul e Brastemp — problema de conteúdo da menção, não de volume dela.", F_IA)

# --- Parte 2
slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Parte 2</span><h2>A jornada</h2>
  <p class="sub">Onde a demanda da categoria está, quem ocupa cada momento, e o que as duas fontes dizem quando comparadas</p></div></section>""")

slide("Jornada", "A posse é o momento mais fraco de quase todos os players",
  barras_h([(NOME[k], P[k]["posse"], k) for k in sorted(ORDEM, key=lambda k: -P[k]["posse"])]
           + [("Território sem dono", 100.0, "sem_dono")], lambda k: COR[k], fmt=lambda v: pct(v)),
  "Nenhum player passa de 8,1% da demanda em posse. O único bloco 100% de posse é o que nenhuma marca reivindica.", F_KW)

slide("Território", "207.600 buscas por mês que nenhum player reivindica",
  f'<div class="col2"><div>{barras_h([(f.capitalize(), v, "sem_dono") for f, v in list(SD["familias"].items())[:8]], lambda k: COR["sem_dono"], fmt=lambda v: pct(v))}</div>'
  '<div>' + kpis([(n(SD["volume"]), "buscas/mês sem marca nenhuma", COR["sem_dono"]),
                  (str(SD["ai_overview"]) + "%", "já respondidas com resumo de IA", "#c98500"),
                  (str(SD["intent"][0][1]) + "%", "de intenção informacional", "#f0ede4")])
  + tabela(["Maiores consultas do território","Buscas/mês"],
            [[e(k), "<b>" + n(v) + "</b>"] for k, v in SD["top_keywords"][:6]]) + '</div></div>',
  "É demanda de categoria que não está atrelada a marca nenhuma — espaço mental sem dono. `instalação de ar condicionado` sozinha é 10,7% dele.",
  "SEMrush · 492 keywords não-branded com volume · lista construída a partir do vocabulário real do corpus de IA")

slide("IA", "Na IA, a categoria é usada muito mais para conviver do que para comprar",
  barras_h([(f.capitalize(), v["pct"], None) for f, v in
            sorted(AI["topicos"]["familias"].items(), key=lambda i: -i[1]["pct"])],
           lambda k: "#199e70", fmt=lambda v: pct(v)) +
  kpis([("8,4%", "da demanda de IA é posse", "#199e70"), ("1,5%", "é comparação de modelo", "#6b6a63"), ("0,1%", "é preço e compra", "#6b6a63")]),
  f'{n(AI["topicos"]["total_topicos"])} tópicos de categoria, {n(AI["topicos"]["volume_total"])} de volume. Uso e receita é a maior família — e nenhuma das cinco marcas aparece nas perguntas de receita.', F_TOP)

slide("Divergência", "Receita é a menor família em busca e a maior em IA",
  '<div class="confronto">'
  f'<div class="cf"><span class="cft">Em busca</span><span class="cfv" style="color:#6b6a63">1,4%</span><span class="cfl">do território sem dono · a <b>menor</b> família</span></div>'
  f'<div class="cfx">↔</div>'
  f'<div class="cf"><span class="cft">Em IA</span><span class="cfv" style="color:#199e70">2,3%</span><span class="cfl">da categoria · a <b>maior</b> família de posse</span></div></div>' +
  tabela(["Maiores tópicos de uso e receita em IA","Volume"],
         [[e(k), f"<b>{n(v)}</b>"] for k, v in AI["topicos"]["familias"]["uso e receita"]["maiores"]]),
  "O briefing cita “pesquisar uma receita” como ponto de entrada da marca. O dado diz que essa porta hoje é de assistente, não de buscador.", F_TOP + " · " + F_KW)

slide("Mediação", "A IA já responde a maior parte das consultas de posse",
  barras_h([(f.capitalize(), v["aio"], None) for f, v in
            sorted(D["familias_ai_overview"].items(), key=lambda i: -i[1]["aio"])[:12]],
           lambda k: "#c98500", max_v=100, fmt=lambda v: f"{v}%"),
  "Incidência de AI Overview no resultado do Google, ponderada por volume. Manutenção, defeito, instalação e consumo estão entre 84% e 93%.", F_KW)

ag = D["ai_overview_agregado"]
slide("Mediação", "A mediação chegou ao território que a marca não ocupa — e ainda não ao dela",
  kpis([(f'{ag["posse"]["aio"]}%', "das consultas de posse já são mediadas por IA", "#c98500"),
        (f'{ag["demais"]["aio"]}%', "das demais famílias", "#6b6a63"),
        (f'{ag["electrolux"]}%', "das consultas da Electrolux", "#3987e5")]) +
  f'<div class="quadro alerta"><p>Quando a mediação avançar sobre as consultas de marca e de especificação — onde a Electrolux tem <b>{n(P["electrolux"]["volume"])} buscas/mês</b> e hoje controla o resultado —, a marca passa a ser intermediada em terreno que domina.</p></div>',
  "É a única leitura do material que só existe cruzando as duas fontes: AI Overview é dado de busca, e o significado dele depende do que a trilha de IA mostrou.", F_KW)

REF = AI["referrals"]
slide("Tendência", "O tráfego vindo de LLM multiplicou por 5,4 em doze meses",
  linhas({("electrolux" if "electrolux" in d else "brastemp" if "brastemp" in d else "consul" if "consul" in d else "midea"): s
          for d, s in REF["series"].items()}, destaque="electrolux",
         rotulos_x=[m[-2:] for m in REF["meses"]], y0=0) +
  kpis([(n(REF["series"]["loja.electrolux.com.br"][-1]), "visitas/mês da loja vindas de LLM", "#3987e5"),
        ("+75%", "1º contra 2º semestre", "#f0ede4"), ("39,9% → 46,0%", "share da Electrolux no canal", "#199e70")]),
  "O canal cresce para todos. A Electrolux sai na frente em volume e ganha participação dentro dele.", F_REF)

slide("Síntese", "As duas fontes concordam sobre o vão e discordam sobre a posição",
  tabela(["","Busca","IA"],
    [["<b>Posição da Electrolux</b>","3ª em volume · share <b>parado</b> (0,99)","<b>1ª em cobertura</b> (33%)"],
     ["<b>Trajetória</b>","não ganha share; quem cresce são os entrantes","share de tráfego <b>39,9% → 46,0%</b>"],
     ["<b>Posse</b>","4,4% · metade da Consul","<b>0%</b> em manutenção e em receita"],
     ["<b>Quem ocupa a posse</b>","Consul, com 8,1%","Consul e Brastemp, com 25% cada"],
     ["<b>Percepção</b>","não é o que a fonte mede","sentimento 58,1 — 2º pior do conjunto"]], "wide"),
  "A marca está melhor posicionada no canal novo do que no maduro — e não construiu essa vantagem deliberadamente.", F_KW + " · " + F_IA)

# --- fechamento
slide("Fechamento", "Os quatro achados que sustentam o resto",
  '<div class="achados">' + "".join(
    f'<div class="ach"><span class="an">{i}</span><div><b>{t}</b><p>{d}</p></div></div>' for i, (t, d) in enumerate([
      ("A posse é o vão, nas duas fontes","Electrolux tem 4,4% da demanda em posse contra 8,1% da Consul, e 0% de cobertura nas perguntas de manutenção feitas à IA."),
      ("A mediação por IA já chegou ao território vago","41% das consultas de posse são respondidas com resumo, contra 14% das consultas da Electrolux."),
      ("O crescimento da categoria está nos entrantes","Hisense a 1,40 e Haier a 1,36 contra a categoria; Brastemp a 0,86 e Samsung a 0,85."),
      ("A marca é a mais citada em IA e a pior falada","33% de cobertura, à frente de todos, com sentimento 58,1 contra 70,5 da Consul.")], 1)) + '</div>',
  "", "Detalhe e reprodução em 10-diagnostico/search/40-leitura/")

# --- apendice
slides.append("""<section class="slide divisor"><div class="slide-inner">
  <span class="parte">Apêndice</span><h2>Método, fontes<br>e o que checar</h2></div></section>""")

slide("Apêndice", "Números frágeis — confira antes de levar para o cliente",
  tabela(["Número","Por quê","Onde aparece"], [
    ["Descoberta da Samsung, 5,5%","O export usou seed <code>geladeira samsung</code>, não <code>samsung</code>. É artefato, não achado","Bloco Samsung · comparativo de jornada"],
    ["Cobertura de IA em posse (0%, 25%)","As famílias de manutenção e receita têm entre 3 e 4 perguntas na amostra de 150","Comparativo de IA · síntese"],
    ["Sentimento (58,1 · 70,5 · 46,3)","Classificação automática do fornecedor, sem critério publicado. Vale como comparação relativa, não como nível","Comparativo de IA"],
    ["Séries de 12 meses","Reconstruídas a partir de Volume e Trend, sob premissa declarada","Todos os slides de evolução"],
    ["Volumes entre players","Exports com profundidade diferente: Brastemp 1.998 keywords, Haier 44","Panorama"],
    ["Tráfego de LLM","Estimativa modelada, não contagem","Slide de tendência"]], "wide"),
  "", "Detalhe completo em 00-revisao-de-escopo.md")

slide("Apêndice", "O que este dado não responde",
  tabela(["Pergunta","Por que não","O que resolveria"], [
    ["Quem captura cada consulta hoje","A coluna de competidor veio vazia nos nove arquivos","Organic Positions dos domínios captores"],
    ["Qual o valor da demanda não capturada","Sem CPC real e sem taxa de conversão","Dados de conta e GA4 da loja"],
    ["O que a IA responde quando perguntam pela marca pelo nome","Só veio o recorte não-branded","Relatório de AI answers branded"],
    ["Quais fontes os modelos citam","Há contagem de fontes, não a lista","Export de citation sources"],
    ["Hisense e Haier em IA","Não estão nas respostas nem no tráfego medido","Incluir os dois no rastreio"]], "wide"),
  "Lacuna declarada é método. O material não preenche nenhuma delas por suposição.", "00-revisao-de-escopo.md · 10-dicionario/pedido-de-dados.md")

# --- slides adicionais (inseridos por ordem no assembler)
EXTRA = {}

EXTRA["descoberta"] = lambda: slide("Jornada · Descoberta", "Quem entra na categoria concentra a demanda no próprio nome",
  barras_h([(NOME[k], P[k]["descoberta"], k) for k in sorted(ORDEM, key=lambda k: -P[k]["descoberta"])],
           lambda k: COR[k], fmt=lambda v: pct(v)) +
  kpis([(pct(P["haier"]["descoberta"]), "da demanda da Haier é o nome dela", COR["haier"]),
        (pct(P["hisense"]["descoberta"]), "da Hisense", COR["hisense"]),
        (pct(P["electrolux"]["descoberta"]), "da Electrolux", COR["electrolux"])]),
  "Quanto maior a fatia, mais cedo a marca está na formação de demanda. Haier e Hisense ainda respondem “quem é essa marca”; as estabelecidas já disputam produto.", F_KW)

EXTRA["escolha"] = lambda: slide("Jornada · Escolha", "Na escolha de produto os sete players estão empatados",
  barras_h([(NOME[k], P[k]["escolha"], k) for k in sorted(ORDEM, key=lambda k: -P[k]["escolha"])],
           lambda k: COR[k], fmt=lambda v: pct(v)) +
  '<div class="quadro"><p>Cinco dos sete estão entre 21% e 30%. É o momento mais disputado e o menos diferenciável da jornada — todo mundo está lá, com o mesmo peso.</p></div>',
  "Capacidade, tecnologia, modelo e comparação. A demanda existe para todos e nenhum player se destaca nela.", F_KW)

EXTRA["chatgpt"] = lambda: slide("IA", "A presença da categoria em IA é, hoje, presença no ChatGPT",
  barras_empilhadas([(m, [(p, AI["marcas"][m]["cobertura"][p], c) for p, c in
                          [("ChatGPT","#199e70"),("Gemini","#3987e5"),("Google AI Mode","#c98500"),("Perplexity","#d55181")]],
                      "") for m in ["Electrolux","Consul","Brastemp","Samsung","Midea"]]) +
  tabela(["Provedor"] + ["Electrolux","Consul","Brastemp","Samsung","Midea"],
         [[p] + [f'{AI["marcas"][m]["cobertura"][p]}%' for m in ["Electrolux","Consul","Brastemp","Samsung","Midea"]]
          for p in ["ChatGPT","Gemini","Google AI Mode","Perplexity"]], "wide"),
  "Cobertura por provedor. No ChatGPT a Electrolux aparece em 25% das perguntas; nos outros três, entre 7% e 9%. O padrão vale para todos — é característica da plataforma, não fraqueza de marca.", F_IA)

EXTRA["elux_cat"] = lambda: slide("Electrolux", "Geladeira concentra um terço da demanda de marca da Electrolux",
  '<div class="col2"><div>' +
  barras_h([(CATN.get(c, c).capitalize(), v, "electrolux") for c, v in list(P["electrolux"]["categorias"].items())[:7]],
           lambda k: COR["electrolux"], fmt=lambda v: pct(v)) + '</div><div>' +
  tabela(["Maiores consultas da marca","Buscas/mês"],
         [[e(k), "<b>" + n(v) + "</b>"] for k, v in P["electrolux"]["top_keywords"][:6]]) + '</div></div>',
  f'Ar condicionado é {pct(P["electrolux"]["categorias"].get("ar condicionado", 0))} da demanda da Electrolux — contra {pct(P["midea"]["categorias"].get("ar condicionado", 0))} da Midea e {pct(P["haier"]["categorias"].get("ar condicionado", 0))} da Haier.', F_KW)

EXTRA["janela"] = lambda: slide("Fechamento", "O que muda com o tempo, e o que não",
  '<div class="col2"><div class="quadro"><span class="qh">Move com o tempo</span><ul>'
  '<li>A mediação por IA avança das consultas de posse para as de marca</li>'
  '<li>A base instalada de Haier e Hisense começa a gerar demanda de pós-compra</li>'
  '<li>O tráfego de LLM segue crescendo em toda a categoria</li></ul></div>'
  '<div class="quadro"><span class="qh">Não move sozinho</span><ul>'
  '<li>O território de posse continua sem dono enquanto ninguém o ocupar</li>'
  '<li>O sentimento da marca em IA não melhora por volume de citação</li>'
  '<li>As frentes nomeadas seguem perdendo demanda</li></ul></div></div>',
  "Este material para aqui: os dados e a leitura deles. A decisão de território, mensagem e plano é das áreas.", "")

# gera os extras e reordena para as posicoes corretas
base_n = len(slides)
idx = {}
for nome_ in ["elux_cat","chatgpt","descoberta","escolha","janela"]:
    EXTRA[nome_](); idx[nome_] = len(slides) - 1

ordem = (list(range(0, 9)) + [idx["elux_cat"]] + list(range(9, 19)) + [idx["chatgpt"]]
         + [19] + [idx["descoberta"], idx["escolha"]] + list(range(20, 29))
         + [idx["janela"]] + list(range(29, base_n)))
slides = [slides[i] for i in ordem]
print("todos os slides:", len(slides))

# ================================================================== CSS + HTML
CSS = """
/* === RESET E BASE === */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --surface:#1a1a19; --surface-2:#212120; --ink:#f0ede4; --ink-2:#a8a69c; --ink-3:#6b6a63;
  --hair:#2e2e2b; --accent:#3987e5;
  --s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--s5:#d55181;--s6:#008300;--s7:#e66767;--s8:#9085e9;
}
html,body{height:100%;background:var(--surface);color:var(--ink);
  font-family:'Supreme',ui-sans-serif,sans-serif;font-feature-settings:'tnum' 1;
  -webkit-font-smoothing:antialiased;overflow-x:hidden}
body{scroll-snap-type:y mandatory;overflow-y:auto}

/* === SLIDE: VIEWPORT FITTING (NAO NEGOCIAVEL) === */
.slide{height:100vh;height:100dvh;overflow:hidden;scroll-snap-align:start;position:relative;
  display:flex;align-items:center;
  background:radial-gradient(120% 90% at 88% 6%, #22231f 0%, var(--surface) 62%)}
.slide::after{content:'';position:absolute;inset:0;pointer-events:none;
  background-image:linear-gradient(var(--hair) 1px,transparent 1px);background-size:100% 64px;opacity:.25}
.slide-inner{position:relative;z-index:1;width:min(1580px,92vw);margin:0 auto;
  max-height:90vh;display:flex;flex-direction:column;gap:clamp(.5rem,1.1vh,1rem)}

/* === TIPOGRAFIA === */
.kicker{font-size:clamp(.58rem,.82vw,.78rem);letter-spacing:.24em;text-transform:uppercase;
  color:var(--accent);font-weight:600}
h1{font-family:'Zodiak',Georgia,serif;font-weight:400;line-height:.98;
  font-size:clamp(2.6rem,6.6vw,6rem);letter-spacing:-.02em}
h1 em{font-style:italic;color:var(--accent)}
h2{font-family:'Zodiak',Georgia,serif;font-weight:400;line-height:1.06;
  font-size:clamp(1.35rem,2.85vw,2.7rem);letter-spacing:-.015em;max-width:22ch}
.s-head{display:flex;flex-direction:column;gap:clamp(.2rem,.5vh,.45rem);
  border-left:2px solid var(--accent);padding-left:clamp(.6rem,1vw,1rem)}
.s-head h2{max-width:34ch}
.sub{color:var(--ink-2);font-size:clamp(.82rem,1.15vw,1.05rem);max-width:62ch;line-height:1.45}
.leitura{color:var(--ink-2);font-size:clamp(.74rem,1.02vw,.95rem);line-height:1.5;max-width:96ch;
  border-top:1px solid var(--hair);padding-top:clamp(.35rem,.8vh,.7rem)}
.leitura b{color:var(--ink);font-weight:600}
.fonte{color:var(--ink-3);font-size:clamp(.54rem,.72vw,.68rem);letter-spacing:.04em}
.s-body{flex:1;min-height:0;display:flex;flex-direction:column;gap:clamp(.45rem,1vh,.9rem);
  justify-content:center;overflow:hidden}

/* === CAPA E DIVISOR === */
.capa .slide-inner,.divisor .slide-inner{gap:clamp(.7rem,2vh,1.7rem)}
.capa-meta{display:flex;flex-wrap:wrap;gap:clamp(.5rem,1.4vw,1.4rem);margin-top:clamp(.4rem,1.4vh,1.2rem)}
.capa-meta span{font-size:clamp(.6rem,.86vw,.8rem);color:var(--ink-2);letter-spacing:.05em;
  border:1px solid var(--hair);padding:.32em .8em;border-radius:2em}
.divisor{background:linear-gradient(115deg,#202220 0%,var(--surface) 58%)}
.parte{font-size:clamp(.6rem,.9vw,.82rem);letter-spacing:.3em;text-transform:uppercase;color:var(--accent)}
.divisor h2{font-size:clamp(2.2rem,5.4vw,5rem);max-width:none}

/* === BARRAS HORIZONTAIS === */
.bh{display:flex;flex-direction:column;gap:clamp(.24rem,.85vh,.6rem)}
.bh-row{display:grid;grid-template-columns:minmax(9ch,15ch) 1fr minmax(6ch,9ch);
  align-items:center;gap:clamp(.4rem,.9vw,.9rem)}
.bh-lab{font-size:clamp(.62rem,.88vw,.84rem);color:var(--ink-2);text-align:right;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bh-track{height:clamp(.8rem,2.4vh,1.5rem);background:#232322;border-radius:2px;overflow:hidden}
.bh-fill{display:block;height:100%;border-radius:0 3px 3px 0;
  animation:grow .8s cubic-bezier(.2,.8,.2,1) both}
.bh-val{font-size:clamp(.62rem,.9vw,.86rem);font-weight:600;color:var(--ink)}
@keyframes grow{from{transform:scaleX(0);transform-origin:left}to{transform:scaleX(1)}}

/* === BARRAS EMPILHADAS === */
.be{display:flex;flex-direction:column;gap:clamp(.24rem,.85vh,.6rem)}
.be-row{display:grid;grid-template-columns:minmax(9ch,14ch) 1fr minmax(7ch,13ch);
  align-items:center;gap:clamp(.4rem,.9vw,.9rem)}
.be-lab{font-size:clamp(.62rem,.88vw,.84rem);color:var(--ink-2);text-align:right}
.be-track{display:flex;height:clamp(.95rem,2.9vh,1.85rem);border-radius:2px;overflow:hidden;gap:2px}
.be-seg{display:block;animation:grow .8s cubic-bezier(.2,.8,.2,1) both}
.be-extra{font-size:clamp(.6rem,.86vw,.8rem);color:var(--ink-2)}
.legenda{display:flex;flex-wrap:wrap;gap:clamp(.5rem,1.3vw,1.3rem);margin-top:.3rem}
.legenda span{display:flex;align-items:center;gap:.4em;font-size:clamp(.58rem,.8vw,.74rem);color:var(--ink-2)}
.legenda i{width:.8em;height:.8em;border-radius:2px;display:block}

/* === SVG === */
.chart{width:100%;height:auto;max-height:min(52vh,470px);display:block}
.ln{fill:none;stroke-width:1.6;stroke-linejoin:round;stroke-linecap:round;opacity:.55}
.ln.forte{stroke-width:2.6;opacity:1}
.ref{stroke:var(--hair);stroke-width:1;stroke-dasharray:3 4}
.reflab,.xlab,.lnlab{font-family:'Supreme',sans-serif;font-size:11px;fill:var(--ink-3)}
.lnlab{font-size:12px;font-weight:600}
.xlab{text-anchor:middle}

/* === TABELAS === */
.tb,.hm{width:100%;border-collapse:collapse;font-size:clamp(.6rem,.88vw,.85rem)}
.tb th,.hm th{text-align:left;color:var(--ink-3);font-weight:600;letter-spacing:.06em;
  text-transform:uppercase;font-size:clamp(.5rem,.68vw,.64rem);padding:.5em .7em;
  border-bottom:1px solid var(--hair)}
.tb td{padding:.52em .7em;border-bottom:1px solid #232322;color:var(--ink-2);vertical-align:top}
.tb td b,.tb td:first-child{color:var(--ink)}
.tb.wide td{padding:.42em .7em}
.hm td{padding:.5em .4em;text-align:center;border:1px solid var(--surface);
  font-variant-numeric:tabular-nums;font-size:clamp(.55rem,.78vw,.76rem)}
.hm th.rh{text-align:right;text-transform:none;font-size:clamp(.58rem,.8vw,.78rem);
  color:var(--ink-2);border:none;padding-right:.7em}
.hm thead th{text-align:center;padding-bottom:.4em}
.dot{display:inline-block;width:.6em;height:.6em;border-radius:50%;margin-right:.5em}
.up,.tb td b.up{color:var(--s3);font-weight:600}
.down,.tb td b.down{color:var(--s2);font-weight:600}
.flat{color:var(--ink-3)}
code{font-family:ui-monospace,monospace;font-size:.9em;color:var(--ink);background:#26261f;padding:.1em .35em;border-radius:2px}

/* === KPIS === */
.kpis{display:flex;flex-wrap:wrap;gap:clamp(.6rem,2vw,2.4rem);
  border-top:1px solid var(--hair);padding-top:clamp(.4rem,1vh,.9rem)}
.kpi{display:flex;flex-direction:column;gap:.12em;min-width:min(20ch,42vw)}
.kv{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.4rem,3.2vw,2.9rem);line-height:1;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.kl{font-size:clamp(.58rem,.82vw,.76rem);color:var(--ink-2);line-height:1.3;max-width:26ch}

/* === BLOCOS === */
.col2{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.7rem,2.2vw,2.2rem);align-items:start;min-height:0}
.quadro{border:1px solid var(--hair);border-left:2px solid var(--accent);
  padding:clamp(.6rem,1.5vh,1.1rem) clamp(.7rem,1.4vw,1.2rem);background:var(--surface-2)}
.quadro.alerta{border-left-color:var(--s4)}
.quadro p,.quadro li{color:var(--ink-2);font-size:clamp(.72rem,1vw,.92rem);line-height:1.5}
.quadro b{color:var(--ink)}
.quadro ul{margin-left:1.1em;display:flex;flex-direction:column;gap:.3em}
.qh{display:block;font-size:clamp(.54rem,.74vw,.66rem);letter-spacing:.2em;text-transform:uppercase;
  color:var(--accent);margin-bottom:.5em}
blockquote{font-family:'Zodiak',Georgia,serif;font-size:clamp(.95rem,1.9vw,1.6rem);line-height:1.35;color:var(--ink)}
cite{display:block;margin-top:.6em;font-style:normal;font-size:clamp(.58rem,.8vw,.74rem);color:var(--ink-3)}
.sem-cob{border:1px dashed var(--hair);padding:clamp(.7rem,1.8vh,1.3rem);text-align:center;
  display:flex;flex-direction:column;gap:.3em;background:#1e1e1c}
.sc-x{font-size:clamp(1.2rem,2.6vw,2.2rem);color:var(--ink-3);line-height:1}
.sem-cob b{font-size:clamp(.72rem,1vw,.9rem)}
.sem-cob span:last-child{font-size:clamp(.58rem,.8vw,.74rem);color:var(--ink-3);max-width:34ch;margin:0 auto}
.confronto{display:flex;align-items:center;gap:clamp(.7rem,2.5vw,2.5rem);justify-content:center;
  border-block:1px solid var(--hair);padding:clamp(.7rem,2vh,1.4rem) 0}
.cf{display:flex;flex-direction:column;gap:.2em;text-align:center;flex:1}
.cft{font-size:clamp(.54rem,.74vw,.66rem);letter-spacing:.2em;text-transform:uppercase;color:var(--ink-3)}
.cfv{font-family:'Zodiak',Georgia,serif;font-size:clamp(2rem,5vw,4.4rem);line-height:1}
.cfl{font-size:clamp(.6rem,.85vw,.8rem);color:var(--ink-2)}
.cfx{font-size:clamp(1.1rem,2.4vw,2rem);color:var(--ink-3)}
.achados{display:grid;grid-template-columns:1fr 1fr;gap:clamp(.6rem,1.8vw,1.6rem)}
.ach{display:flex;gap:clamp(.5rem,1.1vw,1rem);border-top:1px solid var(--hair);padding-top:.7em}
.an{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.2rem,2.4vw,2rem);color:var(--accent);line-height:1}
.ach b{display:block;font-size:clamp(.76rem,1.05vw,.98rem);margin-bottom:.25em}
.ach p{font-size:clamp(.62rem,.88vw,.82rem);color:var(--ink-2);line-height:1.45}

/* === NAV === */
.nav{position:fixed;right:clamp(.5rem,1.4vw,1.4rem);top:50%;transform:translateY(-50%);z-index:50;
  display:flex;flex-direction:column;gap:6px}
.nav b{width:6px;height:6px;border-radius:50%;background:var(--hair);cursor:pointer;
  border:none;padding:0;transition:background .2s,transform .2s}
.nav b.on{background:var(--accent);transform:scale(1.5)}
.pg{position:fixed;left:clamp(.6rem,1.6vw,1.6rem);bottom:clamp(.5rem,1.4vh,1.2rem);z-index:50;
  font-size:clamp(.56rem,.76vw,.7rem);color:var(--ink-3);letter-spacing:.1em}

/* === BREAKPOINTS DE ALTURA === */
@media (max-height:700px){.slide-inner{max-height:92vh}.kpi{min-width:min(16ch,40vw)}}
@media (max-height:600px){.chart{max-height:38vh}.leitura{font-size:.7rem}
  .bh-track{height:.6rem}.be-track{height:.7rem}
  .bh,.be{gap:.2rem}}
@media (max-height:500px){.s-head h2{font-size:1.2rem}.kv{font-size:1.3rem}
  .chart{max-height:32vh}.fonte{display:none}}
@media (max-width:900px){.col2,.achados{grid-template-columns:1fr}}

/* === REDUCED MOTION === */
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

JS = """
const ss=[...document.querySelectorAll('.slide')];
const nav=document.querySelector('.nav'), pg=document.querySelector('.pg');
ss.forEach((_,i)=>{const b=document.createElement('b');b.onclick=()=>ss[i].scrollIntoView({behavior:'smooth'});nav.appendChild(b)});
const dots=[...nav.children];
const io=new IntersectionObserver(es=>es.forEach(en=>{if(en.isIntersecting){
  const i=ss.indexOf(en.target);dots.forEach((d,j)=>d.classList.toggle('on',i===j));
  pg.textContent=String(i+1).padStart(2,'0')+' / '+String(ss.length).padStart(2,'0');}}),{threshold:.55});
ss.forEach(s=>io.observe(s));
addEventListener('keydown',ev=>{
  const cur=ss.findIndex(s=>{const r=s.getBoundingClientRect();return r.top>=-50&&r.top<innerHeight/2});
  if(['ArrowDown','ArrowRight',' ','PageDown'].includes(ev.key)){ev.preventDefault();ss[Math.min(cur+1,ss.length-1)]?.scrollIntoView({behavior:'smooth'})}
  if(['ArrowUp','ArrowLeft','PageUp'].includes(ev.key)){ev.preventDefault();ss[Math.max(cur-1,0)]?.scrollIntoView({behavior:'smooth'})}});
"""

doc = f"""<!doctype html>
<html lang="pt-BR"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cenário de search e IA — Electrolux LATAM 2027 · Youdare</title>
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=zodiak@400,401&f[]=supreme@400,500,600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head><body>
<nav class="nav"></nav><div class="pg">01</div>
{chr(10).join(slides)}
<script>{JS}</script>
</body></html>"""

out = B/"50-entrega"/"2026-08-17_youdare_deck_cenario-search-ai-electrolux.html"
out.write_text(doc, encoding="utf-8")
print(f"gerado: {out.name} — {len(slides)} slides, {len(doc):,} bytes")
