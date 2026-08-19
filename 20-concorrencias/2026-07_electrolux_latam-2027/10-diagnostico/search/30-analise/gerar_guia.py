# -*- coding: utf-8 -*-
"""
Gera o texto de apoio do material executivo: o que e cada dado, de onde vem,
como se le e o que ele nao responde.

E documento de leitura corrida, nao deck. Quem for usar o material em reuniao
le isto antes; quem for contestar um numero na banca acha aqui a definicao.

Saida: 50-entrega/2026-08-17_youdare_guia_como-ler-o-dado.html
"""
import json, html
from pathlib import Path

B = Path(__file__).resolve().parent.parent
D = json.load(open(B/"30-analise"/"dados_do_deck.json", encoding="utf-8"))
P, SD, AI, J4 = D["players"], D["sem_dono"], D["ai"], D["jornada4"]
PAN, U = D["panorama"], D["panorama"]["universo"]
CN, SM, ES, PP = PAN["cobertura_nome"], PAN["sem_marca"], PAN["estagios"], PAN["prompts"]
OC = list(PAN["ocupacao"].values())[0]

def e(s): return html.escape(str(s))
def n(v): return f"{v:,.0f}".replace(",", ".")
def pct(v, d=1): return f"{v:.{d}f}".replace(".", ",") + "%"

def secao(num, titulo, corpo):
    return f'<section class="sec"><h2><span class="num">{num}</span>{titulo}</h2>{corpo}</section>'

def medida(nome, o_que, denominador, como_ler, erro, onde):
    return f"""<div class="med">
      <h3>{nome}</h3>
      <dl>
        <dt>O que é</dt><dd>{o_que}</dd>
        <dt>Sobre o quê é calculada</dt><dd><b>{denominador}</b></dd>
        <dt>Como se lê</dt><dd>{como_ler}</dd>
        <dt class="al">Onde engana</dt><dd class="al">{erro}</dd>
        <dt>Onde aparece</dt><dd class="on">{onde}</dd>
      </dl></div>"""

def tab(cab, linhas, cls=""):
    th = "".join(f"<th>{c}</th>" for c in cab)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in l) + "</tr>" for l in linhas)
    return f'<table class="{cls}"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'

# ============================================================== conteudo
S = []

S.append(secao("01", "Para que serve este documento", """
<p class="lead">O material de cenário mostra os números. Este documento explica <b>o que cada
número é</b>, de onde ele vem, sobre o que ele é calculado e onde ele engana. Leia antes de
apresentar; consulte quando alguém contestar.</p>
<p>Duas regras valem para o material inteiro e resolvem a maior parte das dúvidas:</p>
<ul class="regras">
  <li><b>Cobertura é sempre sobre o total da demanda da categoria.</b> Quando a comparação for
  de marca contra marca, é esta a medida. Nunca sobre a fatia já ocupada pelas marcas, nunca
  sobre uma amostra de perguntas.</li>
  <li><b>Busca e IA não se somam.</b> Medem coisas diferentes, em unidades diferentes. Toda
  comparação entre as duas fontes é de posição relativa dentro de cada uma.</li>
</ul>"""))

S.append(secao("02", "As duas fontes", f"""
<p>O material tem duas bases independentes. Elas foram construídas separadamente, sem consulta
uma à outra, e só depois cruzadas. É essa independência que dá valor às convergências.</p>
<div class="fontes">
  <div class="fonte f-search">
    <span class="tag">Search</span>
    <h3>Demanda de busca</h3>
    <p class="cifra">{n(J4["total"])}</p><p class="cl">buscas/mês mapeadas · Brasil · ago/25 a jul/26</p>
    <p><b>O que é.</b> Volume de busca por palavra-chave, com série mensal de doze meses.
    Um arquivo por marca, mais um de cabeças de categoria e uma lista de cauda sem marca
    construída por nós.</p>
    <p><b>Enxerga.</b> A demanda que a pessoa expressa digitando, os termos exatos, a composição
    por necessidade e a forma da curva ao longo do ano.</p>
    <p><b>Não enxerga.</b> Quem captura cada consulta hoje, demanda latente, conversão.</p>
  </div>
  <div class="fonte f-ia">
    <span class="tag">IA</span>
    <h3>Demanda mediada por assistente</h3>
    <p class="cifra">{n(U["volume"])}</p><p class="cl">de volume em {n(U["topicos_categoria"])} tópicos de categoria · Brasil</p>
    <p><b>O que é.</b> Tópicos que os assistentes tratam como o mesmo assunto, com volume e
    intenção; e os prompts reais dentro deles, com a resposta que cada provedor deu.</p>
    <p><b>Enxerga.</b> O que as pessoas perguntam, em que momento da relação com o produto,
    e se alguma marca é nomeada — na pergunta e na resposta.</p>
    <p><b>Não enxerga.</b> Quais fontes o modelo cita para montar a resposta, e o que ele
    responde quando perguntam pela marca pelo nome.</p>
  </div>
</div>
<h3>O que limita as duas</h3>
<p><b>Em busca, os recortes por marca têm profundidade diferente</b> — Brastemp com 1.998
keywords, Haier com 44. A composição interna de cada marca é comparável; o tamanho entre marcas
não. Por isso a comparação de cobertura entre players só é válida na base de IA, cujos
{len(U["seeds"])} pontos de partida são todos de categoria e nenhum carrega nome de marca.</p>
<p><b>Em IA, cada relatório de visibilidade monta o próprio universo de perguntas</b>, em torno
do domínio analisado. O mesmo player aparece com valores diferentes em relatórios diferentes.
Share of voice nunca se compara entre relatórios, só entre players dentro do mesmo — e
<b>quando os relatórios divergem, o número de referência do material é sempre o do relatório da
Electrolux</b>; os de concorrente entram como confirmação.</p>"""))

S.append(secao("03", "As medidas, uma a uma", "".join([
    medida("Cobertura",
      "A fatia da demanda total da categoria cujos tópicos carregam o nome de uma marca.",
      f"O total da demanda de categoria em IA — {n(U['volume'])} de volume",
      f"Electrolux tem {pct(CN['electrolux']['pct'],2)}, Brastemp {pct(CN['brastemp']['pct'],2)}. "
      f"Somando as sete e as demais marcas, {pct(100-SM['pct'],1)}. O resto, {pct(SM['pct'],1)}, não nomeia fabricante.",
      "Ela mede o que é <b>perguntado</b>, não quem a IA cita ao responder. São perguntas diferentes.",
      "Parte 2 · Cobertura consolidado, por marca e por estágio"),
    medida("Citação em resposta",
      "Em quantas das 150 perguntas sem marca de uma amostra a marca aparece no texto da resposta.",
      "A amostra de 150 perguntas — não a demanda da categoria",
      "Electrolux aparece em 33% delas. É a medida de <b>como</b> a marca aparece, não de quanto da demanda ela cobre.",
      "Números de citação e de cobertura têm denominadores diferentes e não se comparam entre si. "
      "Usar 33% numa comparação de marca contra marca é erro: a medida certa ali é a cobertura.",
      "Parte 2 · Cobertura, outras medidas e provedores"),
    medida("Presença e ocupação",
      "<b>Presença</b> é o volume dos tópicos em que um domínio aparece de algum modo. "
      "<b>Ocupação</b> é essa mesma presença ponderada pela visibilidade que o domínio tem dentro de cada tópico.",
      "O total da demanda de categoria em IA",
      f"{OC['dominio']} está presente em {pct(OC['presenca_pct'],1)} do volume e ocupa {pct(OC['ocupacao_pct'],1)}. "
      "A distância entre as duas é o diagnóstico: aparecer em muitos tópicos com pouca visibilidade em cada um.",
      "A medida existe por domínio. Não comparar um player que a tem com outro que não a tem.",
      "Parte 2 · Ocupação"),
    medida("Trajetória (inclinação contra a categoria)",
      "A média dos cinco últimos meses dividida pela dos sete primeiros, depois de dividir a série "
      "da marca pela série da categoria para descontar sazonalidade.",
      "A própria série da marca, relativa à categoria",
      "Acima de 1,00 a marca ganha share de demanda; abaixo, perde. Hisense 1,40; Electrolux 0,99; Samsung 0,85.",
      "Sem descontar a sazonalidade, a Electrolux apareceria em 1,08 e pareceria estar crescendo. "
      "Toda a categoria sobe e desce junto nos mesmos meses.",
      "Parte 1 · Panorama e retrato de arquétipos"),
    medida("Fatia de posse",
      "Quanto da demanda classificada de uma marca vem das famílias de vida com o produto.",
      "O volume classificado daquela marca — os três estágios somam 100%",
      f"Consul {pct(100*P['consul']['posse']/max(P['consul']['descoberta']+P['consul']['escolha']+P['consul']['posse'],.01))}, "
      f"Electrolux {pct(100*P['electrolux']['posse']/max(P['electrolux']['descoberta']+P['electrolux']['escolha']+P['electrolux']['posse'],.01))}. "
      "É leitura de perfil, não de tamanho.",
      "Não use para comparar tamanho entre marcas: os recortes de origem têm profundidades diferentes.",
      "Parte 1 · Retratos de arquétipo e de perfil"),
])))

S.append(secao("04", "O modelo de jornada", f"""
<p>Os mesmos quatro estágios organizam as duas fontes, mas são derivados de formas diferentes,
porque as fontes medem coisas diferentes. Isso está declarado no material e é declarado aqui.</p>
{tab(["Estágio", "Em busca, sai de", "Em IA, sai de", "Peso em busca", "Peso em IA"], [
  ["<b>0 · Sem marca</b>", "A consulta não menciona fabricante", "O nome do tópico não menciona fabricante",
   f'<b>{pct(100*J4["sem_marca"]/J4["total"],1)}</b>', f'<b>{pct(SM["pct"],1)}</b>'],
  ["<b>1 · Descoberta</b>", "Família de marca e navegação", "Família de marca e loja, ou intent navegacional acima de 25%",
   pct(100*J4["descoberta"]/J4["total"],1), pct(ES["descoberta"]["pct"])],
  ["<b>2 · Escolha</b>", "Especificação de produto, aquisição e comparação",
   "Comparação e preço, ou intent comercial + transacional acima de 45%",
   pct(100*J4["escolha"]/J4["total"],1), pct(ES["escolha"]["pct"])],
  ["<b>3 · Posse</b>", "As dez famílias de vida com o produto", "As oito famílias de vida com o produto",
   pct(100*J4["posse"]/J4["total"],1), pct(ES["posse"]["pct"])],
], "wide")}
<p class="obs">Em IA existe um quinto agrupamento, <b>exploração de categoria</b>
({pct(ES["exploracao de categoria"]["pct"])}), para tópicos que nomeiam produto ou categoria sem
expressar necessidade nem intenção de compra dominante. Ele não tem equivalente em busca, onde
esse comportamento aparece dentro do estágio 0.</p>
<p><b>O estágio é regra, não medição.</b> Os cortes em 25% e 45% de intent são decisão nossa,
declarada. Mudar o corte muda a fronteira entre descoberta e escolha, não a leitura de que a
posse pesa mais que a descoberta.</p>"""))

FAM = [("Assistência e conserto", "conserto de geladeira", "Procura quem arruma"),
       ("Defeito e problema", "ar condicionado pingando agua", "Descreve o sintoma antes de saber o que é"),
       ("Peça e consumível", "copo liquidificador", "Procura o componente pelo nome dele, não por “peça”"),
       ("Instalação", "instalação de ar condicionado", "Comprou e precisa pôr para funcionar"),
       ("Manutenção e limpeza", "como limpar ferro de passar", "Cuida do produto para ele durar"),
       ("Manual e uso", "como usar air fryer", "Tem o produto e não sabe operar"),
       ("Consumo e energia", "air fryer gasta muita energia", "Preocupação de custo depois da compra"),
       ("Garantia e suporte", "garantia estendida electrolux", "Procura cobertura, não conserto"),
       ("Receita e preparo", "receitas air fryer", "Usa o produto para o fim dele"),
       ("Descarte e sustentabilidade", "coleta consciente", "Fim de vida do produto")]

S.append(secao("05", "As famílias de necessidade", f"""
<p>Família é o nível mais fino da leitura. Ela agrupa consultas e tópicos <b>pela necessidade
que os gera</b>, e é o eixo do material inteiro. O estágio de posse é a soma dessas famílias.</p>
{tab(["Família", "Consulta real que a exemplifica", "A necessidade por trás"],
     [[f"<b>{a}</b>", f"<code>{e(b)}</code>", c] for a, b, c in FAM], "wide")}
<h3>A regra que mais gera dúvida: nome comercial não é família</h3>
<p>A Electrolux criou frentes nomeadas — Cuida, Instala, Projeta, Pro, Shopclub, Outlet, Coleta
Consciente. Nenhuma delas é uma família. Cada uma <b>entra pela necessidade que atende</b>:
Cuida é assistência, Instala é instalação, Outlet e Shopclub são aquisição e comparação.</p>
<p>O nome comercial é um atributo transversal, que convive com a família e não a substitui.
Por isso <code>assistência técnica electrolux</code> e <code>electrolux cuida</code> caem as duas
em assistência. O que os separa não é a família: é se a pessoa digitou a necessidade ou o nome
comercial que a marca deu a ela.</p>
<p class="obs">A demanda pelo nome existe e é pequena: as sete frentes somam
<b>10.600 buscas/mês</b>, 1,5% da demanda pela marca. A necessidade correspondente é muito maior
— <code>assistência técnica electrolux</code> sozinha tem 5.400 contra 2.790 de Cuida somando as
duas grafias da marca.</p>"""))

S.append(secao("06", "O que pode e o que não pode ser comparado", f"""
{tab(["Comparação", "Pode?", "Por quê"], [
  ["Cobertura de uma marca contra outra, em IA", '<b class="ok">Sim</b>',
   f"Os {len(U['seeds'])} pontos de partida são todos de categoria e nenhum carrega nome de marca. Marca que aparece foi descoberta pela ferramenta."],
  ["Perfil de jornada de uma marca contra outra, em busca", '<b class="ok">Sim</b>',
   "A composição interna de cada marca não depende da profundidade do recorte."],
  ["Trajetória de uma marca contra outra", '<b class="ok">Sim</b>',
   "A inclinação é relativa à própria série da marca, descontada a categoria."],
  ["Volume absoluto de uma marca contra outra, em busca", '<b class="nao">Não</b>',
   "O recorte de Brastemp tem 1.998 keywords e o de Haier, 44. O tamanho reflete a profundidade do recorte, não a marca."],
  ["Citação em resposta de uma marca contra outra", '<b class="nao">Não</b>',
   "Os recortes de prompt partem de nomes de marca, e Consul, Samsung e Haier não têm um. Quem tem aparece mais por construção — por isso a leitura de citação usa só o recorte limpo."],
  ["Volume de busca somado com volume de IA", '<b class="nao">Não</b>',
   "Unidades diferentes. Buscas por mês e volume de tópico não são a mesma coisa."],
  ["Ocupação de um domínio contra a cobertura de outra marca", '<b class="nao">Não</b>',
   "São medidas distintas. Ocupação só se compara com ocupação."],
  ["Share of voice entre dois relatórios de visibilidade", '<b class="nao">Não</b>',
   "Cada relatório monta o próprio universo de perguntas. Só vale a comparação entre players dentro do mesmo relatório, e o número de referência do material é o do relatório da Electrolux."],
], "wide")}
<h3>O recorte limpo dos prompts</h3>
<p>Onde a leitura depende de a IA citar uma marca, o material usa só as <b>{n(PP["n_limpo"])}
respostas do seed sem marca</b>. É o único recorte em que citar um fabricante é decisão do
modelo e não eco do prompt. Nele, {pct(PP["taxa_marca_geral"],1)} das respostas nomeiam alguma
das sete marcas.</p>"""))

S.append(secao("07", "Glossário rápido", tab(["Termo", "O que quer dizer aqui"], [
  ["<b>Tópico</b>", "Agrupamento de prompts que os assistentes tratam como o mesmo assunto. É a unidade da base de IA."],
  ["<b>Prompt</b>", "A pergunta real que uma pessoa fez a um assistente."],
  ["<b>Seed</b>", "O termo de partida de um recorte. Define o que a ferramenta foi procurar, e por isso define o viés."],
  ["<b>Intent</b>", "Classificação da própria ferramenta sobre a disposição da consulta: informacional, comercial, transacional, navegacional, tarefa."],
  ["<b>Visibility</b>", "Nota de 0 a 100 que mede quanto de um tópico um domínio ocupa. Entra no cálculo de ocupação."],
  ["<b>AI Overview</b>", "Resumo gerado que o Google entrega no topo da busca em vez de links. Mede mediação, não presença da marca dentro do resumo."],
  ["<b>Território sem dono</b>", f"As {n(SD['volume'])} buscas/mês de posse que nenhum player reivindica em posicionamento nem tem demanda atrelada ao nome. Não quer dizer que ninguém receba esse tráfego."],
  ["<b>Vazamento de clustering</b>", "Tópicos que a ferramenta agrupou mas que não são sobre a categoria. São excluídos de todo agregado."],
], "wide")))

CSS = """
:root{--surface:#1a1a19;--ink:#f0ede4;--ink-2:#cfcdc4;--ink-3:#8a8880;--hair:#33322e;
  --accent:#3987e5;--ia:#199e70;--alerta:#c98500}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--surface);color:var(--ink);font-family:'Supreme',ui-sans-serif,system-ui,sans-serif;
  line-height:1.6;font-size:16px;-webkit-font-smoothing:antialiased}
.wrap{max-width:74ch;margin:0 auto;padding:clamp(2rem,6vw,5rem) clamp(1.1rem,4vw,2rem) 6rem}
header.capa{border-bottom:1px solid var(--hair);padding-bottom:2.2rem;margin-bottom:3rem}
.kicker{font-size:.68rem;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}
h1{font-family:'Zodiak',Georgia,serif;font-size:clamp(2rem,5vw,3.2rem);line-height:1.08;margin:.5em 0 .3em;font-weight:400}
h1 em{font-style:italic;color:var(--ink-2)}
.sub{color:var(--ink-2);font-size:1.02rem;max-width:56ch}
.sec{margin-bottom:3.6rem;scroll-margin-top:2rem}
h2{font-family:'Zodiak',Georgia,serif;font-size:clamp(1.3rem,2.9vw,1.95rem);font-weight:400;
  line-height:1.2;margin-bottom:1.1rem;display:flex;gap:.7em;align-items:baseline}
.num{font-size:.52em;color:var(--accent);letter-spacing:.1em}
h3{font-size:.95rem;font-weight:600;margin:1.8rem 0 .6rem;color:var(--ink)}
p{color:var(--ink-2);margin-bottom:.85rem}
p.lead{font-size:1.08rem;color:var(--ink)}
p.obs{font-size:.88rem;color:var(--ink-3);border-left:2px solid var(--hair);padding-left:1em}
b{color:var(--ink);font-weight:600}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.86em;
  background:#232322;padding:.12em .4em;border-radius:2px;color:var(--ink)}
ul.regras{list-style:none;display:flex;flex-direction:column;gap:.7rem;margin:1.2rem 0}
ul.regras li{color:var(--ink-2);border-left:2px solid var(--accent);padding-left:1em}
table{width:100%;border-collapse:collapse;margin:1rem 0 1.4rem;font-size:.88rem}
th{text-align:left;font-size:.62rem;letter-spacing:.16em;text-transform:uppercase;color:var(--ink-3);
  border-bottom:1px solid var(--hair);padding:.5em .7em .5em 0;font-weight:500;vertical-align:bottom}
td{padding:.6em .7em .6em 0;border-bottom:1px solid #26262330;color:var(--ink-2);vertical-align:top}
table.wide td:first-child{white-space:nowrap;color:var(--ink)}
.ok{color:var(--ia)} .nao{color:#d95926}
.fontes{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr));gap:1.2rem;margin:1.4rem 0}
.fonte{border:1px solid var(--hair);border-top-width:3px;padding:1.2rem}
.f-search{border-top-color:var(--accent)} .f-ia{border-top-color:var(--ia)}
.fonte .tag{font-size:.58rem;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-3)}
.fonte h3{margin:.3rem 0 .6rem}
.cifra{font-family:'Zodiak',Georgia,serif;font-size:1.9rem;color:var(--ink);line-height:1;margin-bottom:.15rem}
.cl{font-size:.76rem;color:var(--ink-3);margin-bottom:1rem}
.fonte p{font-size:.86rem}
.med{border-top:1px solid var(--hair);padding-top:1.1rem;margin-top:1.6rem}
.med h3{margin-top:0;font-size:1.05rem;font-family:'Zodiak',Georgia,serif;font-weight:400}
dl{display:grid;grid-template-columns:minmax(8rem,12rem) 1fr;gap:.35rem 1.2rem;font-size:.88rem;margin-top:.6rem}
dt{font-size:.62rem;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-3);padding-top:.28em}
dd{color:var(--ink-2)}
dt.al{color:var(--alerta)} dd.al{color:var(--ink-2)}
dd.on{color:var(--ink-3);font-size:.82rem}
footer{border-top:1px solid var(--hair);padding-top:1.4rem;font-size:.78rem;color:var(--ink-3)}
@media (max-width:34rem){dl{grid-template-columns:1fr;gap:.1rem .6rem}dt{padding-top:.7em}}
"""

doc = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Como ler o dado — Electrolux LATAM 2027 · Youdare</title>
<link rel="preconnect" href="https://api.fontshare.com">
<link href="https://api.fontshare.com/v2/css?f[]=zodiak@400,401&f[]=supreme@400,500,600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="wrap">
<header class="capa">
  <span class="kicker">Youdare · Direção de Mídia e Dados · agosto 2026</span>
  <h1>Como ler<br><em>o dado</em></h1>
  <p class="sub">Texto de apoio ao material de cenário de search e IA. O que cada número é, de
  onde vem, sobre o que é calculado e onde ele engana.</p>
</header>
{"".join(S)}
<footer>Complemento do material <b>Cenário de search e IA · Electrolux LATAM 2027</b>.
As ressalvas de número específico vivem no deck <b>Ressalvas de dado</b>.<br>
Gerado por <code>30-analise/gerar_guia.py</code> a partir de <code>dados_do_deck.json</code>.
Nenhuma cifra deste documento é digitada à mão.</footer>
</div></body></html>"""

o = B/"50-entrega"/"2026-08-17_youdare_guia_como-ler-o-dado.html"
o.write_text(doc, encoding="utf-8")
print(f"guia: {len(S)} seções, {len(doc):,} bytes -> {o.name}")
