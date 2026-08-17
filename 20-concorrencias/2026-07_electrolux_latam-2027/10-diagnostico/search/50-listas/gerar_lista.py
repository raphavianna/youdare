"""
Gerador da lista de keywords da CAUDA NAO-BRANDED — o quadrante ausente do dataset.

Constroi combinatoriamente as formulacoes de busca do territorio de ecossistema
(servico, uso, defeito, peca, instalacao, consumo, descarte) sobre as categorias
do portfolio, no vocabulario real observado no corpus de IA.

Ordenada por prioridade: se so couberem N termos, os N primeiros sao os que mais
importam para dimensionar o territorio.

Saidas: lista-cauda-nao-branded.csv (com familia, categoria e racional)
        lista-cauda-nao-branded.txt (so as keywords, para colar na ferramenta)
"""
import csv, unicodedata
from pathlib import Path
BASE = Path(__file__).resolve().parent
TETO = 2000

# ---------------------------------------------------------------- categorias
MDA = ["geladeira","freezer","máquina de lavar","lavadora de roupas","lava e seca",
       "secadora de roupas","fogão","cooktop","forno elétrico","micro-ondas",
       "lava louças","coifa","depurador de ar","adega climatizada","cervejeira",
       "ar condicionado"]
SDA = ["air fryer","fritadeira elétrica","aspirador de pó","robô aspirador",
       "purificador de água","bebedouro","ventilador","batedeira","liquidificador",
       "ferro de passar","cafeteira","panela elétrica","lavadora de alta pressão",
       "sanduicheira","chaleira elétrica"]
TODAS = MDA + SDA
NUCLEO = ["geladeira","máquina de lavar","lava e seca","fogão","micro-ondas",
          "ar condicionado","air fryer","lava louças","aspirador de pó","secadora de roupas"]

# ---------------------------------------------------------------- modificadores
CIDADES = ["são paulo","rio de janeiro","belo horizonte","brasília","curitiba",
    "porto alegre","salvador","recife","fortaleza","campinas","goiânia","manaus",
    "belém","guarulhos","santo andré","são bernardo do campo","osasco","niterói",
    "sorocaba","ribeirão preto","uberlândia","joinville","florianópolis","natal",
    "maceió","joão pessoa","cuiabá","campo grande","vitória","londrina","maringá",
    "santos","são josé dos campos","caxias do sul","contagem","duque de caxias"]

DEFEITOS = {
 "geladeira":["não gela","não está gelando","fazendo barulho","vazando água","não liga",
              "congelando demais","formando gelo","com cheiro ruim","luz não acende","motor não desliga"],
 "freezer":["não congela","não gela","formando gelo","fazendo barulho","não liga"],
 "máquina de lavar":["não centrifuga","não enche de água","não escoa","não liga","fazendo barulho",
                     "vazando água","travada","não bate","parou no meio do ciclo","tambor não gira"],
 "lavadora de roupas":["não centrifuga","não enche","não escoa","fazendo barulho"],
 "lava e seca":["não seca","não centrifuga","não esquenta","não escoa","fazendo barulho"],
 "secadora de roupas":["não seca","não esquenta","não liga","fazendo barulho"],
 "fogão":["não acende","boca não acende","forno não acende","chama amarela","cheiro de gás",
          "acendimento automático não funciona"],
 "cooktop":["não acende","não liga","chama fraca"],
 "forno elétrico":["não esquenta","não liga","resistência queimada"],
 "micro-ondas":["não esquenta","prato não gira","dando faísca","não liga","com barulho"],
 "lava louças":["não seca","não escoa","não lava direito","não liga","vazando"],
 "ar condicionado":["não gela","pingando agua","não liga","com cheiro","luz piscando",
                    "fazendo barulho","desligando sozinho"],
 "air fryer":["não esquenta","não liga","com cheiro de queimado","desligando sozinha"],
 "fritadeira elétrica":["não esquenta","não liga"],
 "aspirador de pó":["perdeu sucção","não liga","não puxa","com pouca forca"],
 "robô aspirador":["não carrega","não liga","não volta para base"],
 "purificador de água":["vazando","não gela","sem pressão","luz vermelha acesa"],
 "bebedouro":["não gela","vazando"],
 "coifa":["não puxa fumaça","fazendo barulho"],
 "depurador de ar":["não puxa","com barulho"],
 "adega climatizada":["não gela","fazendo barulho"],
 "cervejeira":["não gela"],
 "ventilador":["não liga","fazendo barulho"],
 "batedeira":["não liga","perdeu forca"],
 "liquidificador":["não liga","vazando"],
 "ferro de passar":["não esquenta","vazando água","manchando roupa"],
 "cafeteira":["não esquenta","vazando","não passa café"],
 "panela elétrica":["não esquenta","não liga"],
 "lavadora de alta pressão":["sem pressão","não liga"],
 "sanduicheira":["não esquenta"],
 "chaleira elétrica":["não esquenta","não desliga"],
}
PECAS = {
 "geladeira":["borracha da porta","lâmpada","prateleira","gaveta","termostato","compressor","filtro de água","bandeja"],
 "freezer":["borracha da porta","termostato","cesto"],
 "máquina de lavar":["correia","cesto","bomba de drenagem","mangueira","placa eletrônica","rolamento","tampa","filtro"],
 "lava e seca":["correia","resistência","filtro","mangueira"],
 "secadora de roupas":["resistência","filtro","correia"],
 "fogão":["trempe","botão","válvula","resistência do forno","vidro da porta","grelha","queimador"],
 "cooktop":["vidro","queimador","botão"],
 "forno elétrico":["resistência","termostato","vidro da porta"],
 "micro-ondas":["prato giratório","suporte do prato","lâmpada","porta"],
 "lava louças":["filtro","hélice","mangueira","cesto"],
 "ar condicionado":["filtro","controle remoto","capacitor","gás refrigerante","hélice"],
 "air fryer":["cesto","cesto antiaderente","resistência"],
 "aspirador de pó":["filtro hepa","saco","escova","mangueira","bocal"],
 "robô aspirador":["escova","filtro","bateria"],
 "purificador de água":["refil","filtro","válvula"],
 "bebedouro":["filtro","refil","torneira"],
 "coifa":["filtro de carvão","filtro de alumínio","lâmpada"],
 "depurador de ar":["filtro de carvão","filtro"],
 "ventilador":["hélice","grade","motor"],
 "batedeira":["batedor","tigela"],
 "liquidificador":["copo","lâmina","borracha"],
 "ferro de passar":["base","resistência"],
 "cafeteira":["jarra","filtro permanente"],
 "adega climatizada":["prateleira","filtro"],
 "lavadora de alta pressão":["mangueira","bico","gatilho"],
}
RECEITA_CATS = ["air fryer","fritadeira elétrica","forno elétrico","micro-ondas","cooktop","panela elétrica","fogão"]

linhas, vistos = [], set()
def add(prio, familia, categoria, kw, racional):
    k = " ".join(kw.split()).strip().lower()
    if k and k not in vistos:
        vistos.add(k)
        linhas.append({"prioridade":prio,"familia":familia,"categoria":categoria,
                       "keyword":k,"racional":racional})

# P1 · DEFEITO — maior intencao, e a familia mais invisivel no dataset atual
for cat, defs in DEFEITOS.items():
    for d in defs:
        add(1,"defeito",cat,f"{cat} {d}","query de socorro; altissima intencao de servico")
        if cat in NUCLEO:
            add(1,"defeito",cat,f"{cat} {d} o que fazer","formulacao de busca por solucao")
            add(1,"defeito",cat,f"como resolver {cat} {d}","formulacao alternativa")

# P2 · ASSISTENCIA TECNICA — geolocalizada, padrao observado no corpus
for cat in NUCLEO + ["freezer","cooktop","forno elétrico","purificador de água","coifa"]:
    add(2,"assistencia",cat,f"assistência técnica {cat}","cabeca da familia")
    add(2,"assistencia",cat,f"assistência técnica {cat} perto de mim","padrao observado no corpus de IA")
    add(2,"assistencia",cat,f"conserto de {cat}","sinonimo de alta frequencia")
    add(2,"assistencia",cat,f"quanto custa consertar {cat}","decisao consertar x trocar")
    add(2,"assistencia",cat,f"vale a pena consertar {cat}","decisao consertar x trocar")
    add(2,"assistencia",cat,f"orçamento conserto {cat}","intencao transacional de servico")
for cidade in CIDADES:
    add(2,"assistencia","transversal",f"assistência técnica eletrodomésticos {cidade}","geolocalizacao: padrao observado")
    for cat in ["geladeira","máquina de lavar","ar condicionado","fogão","lava e seca",
                "micro-ondas","lava louças","secadora de roupas"]:
        add(2,"assistencia",cat,f"assistência técnica {cat} {cidade}","geolocalizacao por categoria")
    for cat in ["geladeira","máquina de lavar","ar condicionado"]:
        add(2,"assistencia",cat,f"conserto de {cat} {cidade}","sinonimo geolocalizado")
add(2,"assistencia","transversal","assistência técnica autorizada","termo de confianca")
add(2,"assistencia","transversal","técnico de eletrodomésticos perto de mim","formulacao local")
add(2,"assistencia","transversal","conserto de eletrodomésticos a domicílio","modalidade de servico")

# P3 · MANUAL E USO — porta de entrada de pos-compra hoje entregue a terceiro
for cat in TODAS:
    add(3,"manual e uso",cat,f"manual {cat}","contato de pos-compra")
    add(3,"manual e uso",cat,f"manual {cat} pdf","formulacao observada no corpus")
    add(3,"manual e uso",cat,f"como usar {cat}","uso")
    if cat in NUCLEO:
        add(3,"manual e uso",cat,f"como programar {cat}","uso avancado")
        add(3,"manual e uso",cat,f"funções {cat}","descoberta de recurso")
        add(3,"manual e uso",cat,f"símbolos {cat} significado","duvida recorrente de painel")

# P4 · PECA E CONSUMIVEL — cauda de altissima intencao, hoje de marketplace
for cat, pecas in PECAS.items():
    for p in pecas:
        add(4,"peca",cat,f"{p} {cat}","peca de reposicao")
        add(4,"peca",cat,f"{p} {cat} preco","intencao transacional")
    add(4,"peca",cat,f"peça de reposição {cat}","cabeca da familia")
    add(4,"peca",cat,f"onde comprar peça de {cat}","intencao de compra de peca")

# P5 · MANUTENCAO E LIMPEZA — territorio de conteudo e relacionamento
for cat in TODAS:
    add(5,"manutencao",cat,f"como limpar {cat}","conteudo de relacionamento")
    if cat in NUCLEO:
        add(5,"manutencao",cat,f"como higienizar {cat}","variacao de alta frequencia")
        add(5,"manutencao",cat,f"cuidados com {cat}","manutencao preventiva")
        add(5,"manutencao",cat,f"quanto tempo dura {cat}","durabilidade e recompra")
        add(5,"manutencao",cat,f"manutenção preventiva {cat}","servico recorrente")

# P6 · INSTALACAO
for cat in ["geladeira","máquina de lavar","lava e seca","secadora de roupas","fogão","cooktop",
            "forno elétrico","micro-ondas","lava louças","coifa","depurador de ar",
            "ar condicionado","purificador de água","adega climatizada","bebedouro"]:
    add(6,"instalacao",cat,f"como instalar {cat}","instalacao")
    add(6,"instalacao",cat,f"instalação de {cat}","servico de instalacao")
    add(6,"instalacao",cat,f"quanto custa instalar {cat}","intencao transacional")
    add(6,"instalacao",cat,f"medidas do vão para {cat}","planejamento de ambiente")
    add(6,"instalacao",cat,f"precisa de tomada especial {cat}","duvida pre-instalacao")

# P7 · CONSUMO E EFICIENCIA — unica familia de servico ja com sinal no dataset
for cat in TODAS:
    add(7,"consumo",cat,f"consumo de energia {cat}","eficiencia")
    if cat in NUCLEO:
        add(7,"consumo",cat,f"quanto gasta de energia {cat}","formulacao coloquial")
        add(7,"consumo",cat,f"{cat} gasta muita energia","formulacao coloquial")
        add(7,"consumo",cat,f"quantos kwh consome {cat}","formulacao tecnica")
        add(7,"consumo",cat,f"{cat} econômica","atributo de escolha")
add(7,"consumo","transversal","selo procel o que significa","atributo institucional")
add(7,"consumo","transversal","classificação energética eletrodomésticos","atributo institucional")

# P8 · GARANTIA
for cat in NUCLEO:
    add(8,"garantia",cat,f"garantia {cat}","pos-venda")
    add(8,"garantia",cat,f"garantia estendida {cat}","produto de servico")
add(8,"garantia","transversal","garantia estendida vale a pena","decisao de compra de servico")
add(8,"garantia","transversal","como acionar garantia de eletrodoméstico","jornada de pos-venda")
add(8,"garantia","transversal","garantia legal eletrodoméstico","direito do consumidor")

# P9 · DESCARTE E SUSTENTABILIDADE — territorio declarado com zero demanda no corpus de IA
for cat in ["geladeira","máquina de lavar","fogão","micro-ondas","ar condicionado","freezer"]:
    add(9,"descarte",cat,f"como descartar {cat} velha","territorio declarado a validar")
    add(9,"descarte",cat,f"onde doar {cat} usada","reuso")
add(9,"descarte","transversal","reciclagem de eletrodomésticos","territorio declarado")
add(9,"descarte","transversal","logística reversa eletrodomésticos","termo institucional")
add(9,"descarte","transversal","descarte correto de eletrodomésticos","territorio declarado")
add(9,"descarte","transversal","coleta de eletrodomésticos usados","servico")

# P10 · RECEITA E PREPARO — o briefing cita 'pesquisar uma receita' como ponto de entrada
for cat in RECEITA_CATS:
    add(10,"receita",cat,f"receitas {cat}","ponto de entrada citado no briefing")
    add(10,"receita",cat,f"o que dá para fazer no {cat}","descoberta de uso")
    add(10,"receita",cat,f"tabela de tempo e temperatura {cat}","conteudo utilitario")

# P11 · CONTROLE BRANDED — mesma familia com a marca, para medir quanto da demanda ja a menciona
for cat in NUCLEO:
    add(11,"controle branded",cat,f"assistência técnica {cat} electrolux","controle: fatia branded da familia")
    add(11,"controle branded",cat,f"manual {cat} electrolux","controle: fatia branded da familia")
    add(11,"controle branded",cat,f"{cat} electrolux nao liga","controle: fatia branded da familia")
for f in ["electrolux cuida","electrolux instala","electrolux projeta","electrolux pro",
          "electrolux shopclub","electrolux outlet","coleta consciente electrolux",
          "assistência técnica electrolux","peça original electrolux","garantia estendida electrolux"]:
    add(11,"controle branded","frente nomeada",f,"frente nomeada: quadrante anunciado e vago")

# P12 · variantes coloquiais e sinonimos de alta frequencia
SINONIMOS = {"máquina de lavar":["lavadora","maquina de lavar roupa"],"geladeira":["refrigerador"],
             "micro-ondas":["microondas"],"fogão":["fogao"],"air fryer":["airfryer","fritadeira air fryer"],
             "lava louças":["lava-louças","lavalouças"],"aspirador de pó":["aspirador"]}
for cat, alts in SINONIMOS.items():
    for alt in alts:
        add(12,"sinonimo",cat,f"assistência técnica {alt}","forma alternativa da mesma categoria")
        add(12,"sinonimo",cat,f"manual {alt}","forma alternativa")
        add(12,"sinonimo",cat,f"como limpar {alt}","forma alternativa")
        add(12,"sinonimo",cat,f"consumo de energia {alt}","forma alternativa")
        for d in DEFEITOS.get(cat,[])[:4]:
            add(12,"sinonimo",cat,f"{alt} {d}","forma alternativa em query de defeito")

# P13 · completar cobertura das familias sub-representadas
for cat, defs in DEFEITOS.items():
    for d in defs:
        add(13,"defeito",cat,f"como consertar {cat} {d}","formulacao de auto-servico")
        if cat in NUCLEO:
            add(13,"defeito",cat,f"por que {cat} {d}","formulacao de diagnostico")
for cat in NUCLEO + ["freezer","cooktop","forno elétrico","coifa","purificador de água","adega climatizada"]:
    add(13,"assistencia",cat,f"assistência técnica autorizada {cat}","atributo de confianca")
    add(13,"assistencia",cat,f"assistência técnica {cat} 24 horas","urgencia")
    add(13,"assistencia",cat,f"compensa consertar ou comprar {cat} nova","decisao consertar x trocar")
    add(13,"manutencao",cat,f"com que frequência limpar {cat}","recorrencia de cuidado")
    add(13,"manutencao",cat,f"quando trocar {cat}","gatilho de recompra")
    add(13,"manual e uso",cat,f"código de erro {cat}","painel digital")
    add(13,"manual e uso",cat,f"o que significa erro {cat}","painel digital")
for cat, pecas in PECAS.items():
    for pc in pecas[:5]:
        add(13,"peca",cat,f"{pc} {cat} original","atributo de peca original")
        add(13,"peca",cat,f"{pc} {cat} compativel","alternativa de terceiro")
        add(13,"peca",cat,f"como trocar {pc} {cat}","auto-servico de peca")
for cat in TODAS:
    add(13,"instalacao",cat,f"como configurar {cat}","primeira configuracao")
    add(13,"consumo",cat,f"{cat} consome muita energia","formulacao coloquial")
    add(13,"garantia",cat,f"garantia {cat} quanto tempo","duvida de cobertura")

linhas.sort(key=lambda r: r["prioridade"])
final = linhas[:TETO]

with open(BASE/"lista-cauda-nao-branded.csv","w",newline="",encoding="utf-8") as fh:
    w=csv.DictWriter(fh,fieldnames=["prioridade","familia","categoria","keyword","racional"])
    w.writeheader(); w.writerows(final)
with open(BASE/"lista-cauda-nao-branded.txt","w",encoding="utf-8") as fh:
    fh.write("\n".join(r["keyword"] for r in final))

import collections
print(f"TOTAL GERADO: {len(linhas)}  |  ENTREGUE (teto {TETO}): {len(final)}\n")
c=collections.Counter((r["prioridade"],r["familia"]) for r in final)
print(f"{'P':>2}  {'familia':20} {'n':>5}")
for (p,f),n in sorted(c.items()): print(f"{p:>2}  {f:20} {n:>5}")
print(f"\nnao-branded: {sum(1 for r in final if r['familia']!='controle branded')}  |  controle branded: {sum(1 for r in final if r['familia']=='controle branded')}")
