# -*- coding: utf-8 -*-
"""
Gerador das páginas do site VÉRTICE Residencial (demonstrativo).

O site final é HTML estático: index.html, aurora.html, jardins.html, atelier.html e creditos.html.
Os arquivos publicados ficam em site/ (é essa pasta que vai para o Netlify).
Você pode editar os HTML à mão. Este gerador existe para mudanças que se repetem em
todas as páginas (menu, rodapé, dados dos empreendimentos): edite aqui e rode, na pasta do projeto,

    python ferramentas/gerar_site.py

Ele reescreve os HTML de site/. Precisa só de Python 3, sem bibliotecas extras.
Atenção: se você editou um HTML à mão, a edição some quando o gerador roda de novo.
"""
import html, json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'site'
os.chdir(ROOT)

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------------
# Endereço público do site, sem barra no final (ex.: 'https://vertice-residencial.netlify.app').
# Com ele preenchido, a prévia do link no WhatsApp/redes usa a imagem img/og-vertice.jpg.
SITE_URL = 'https://vertice-residencial.netlify.app'
# Número de WhatsApp do corretor (só dígitos, com 55 e DDD, ex.: '5593999999999').
# Vazio = modo demonstração: o botão mostra a mensagem pronta em vez de abrir o WhatsApp.
WHATSAPP = ''

# ---------------------------------------------------------------------------
# FOTOS: arquivo -> (autor, endereço no Unsplash, texto alternativo, é perspectiva 3D?)
# ---------------------------------------------------------------------------
P = {
 # institucional e capítulos (referências)
 'hero-casa-horizonte': ('João Emanuel', 'casa-moderna-com-muro-de-pedra-sh2gc8APbEk', 'Casa térrea de linhas retas com muro de pedra e gramado', False),
 'institucional-concreto': ('Dorsa Masghati', 'parede-de-concreto-branco-durante-o-dia-NRLnzGXtoE4', 'Escada de concreto aparente presa a uma parede', False),
 'arquitetura-luz': ('Lysander Yuen', 'parede-e-teto-de-concreto-branco-0IuRkaouQzw', 'Laje de concreto aparente recortando o céu', False),
 'detalhe-curva': ('Clarisse Croset', 'edificio-de-concreto-cinza-sob-o-ceu-branco-durante-o-dia-be2lj7tGAI0', 'Laje curva de concreto vista de baixo', False),
 'material-concreto': ('the blowup', 'foto-em-escala-de-cinza-da-porta-de-madeira-_GBw5sVMmPU', 'Painéis de concreto com marcas de fôrma', False),
 'material-quina': ('Rowan Heuvel', 'foto-em-tons-de-cinza-do-piso-de-concreto-5K94bFkCLks', 'Quina de concreto polido em preto e branco', False),
 'material-detalhe': ('Karolina Grabowska', 'vela-acesa-e-pequeno-prato-na-superficie-texturizada-ozu_xlDz5Ec', 'Bancada de pedra texturizada com vela acesa', False),
 'paisagismo-esculturas': ('Sergej *****', 'moderna-area-de-estar-ao-ar-livre-com-esculturas-geometricas-uPGEDL9mgi8', 'Jardim com bambus e peças escultóricas brancas', False),
 'paisagismo-noturno': ('Tsuyoshi Kozu', 'jardim-urbano-moderno-com-vegetacao-exuberante-e-elementos-arquitetonicos--h1Dss3b1FY', 'Jardim urbano iluminado entre edifícios', False),
 # galeria de referências
 'galeria-casa-encosta': ('juan verdaguer aguerrebehere', 'uma-casa-em-uma-colina-cercada-por-arvores-e-rochas-mcSZ1pNmUNU', 'Casa de concreto e madeira entre rochas e árvores', False),
 'galeria-torre-ripada': ('Amir Hosseini', 'edificio-de-concreto-marrom-durante-o-dia-3cl6impBd_8', 'Edifício com fachada de ripas curvas em tom terroso', False),
 'galeria-fachada-pedra': ('Carlos Torres', 'projeto-arquitetonico-cinza-e-preto-o7xm8E8R4_U', 'Fachada com módulos de pedra em padrão alternado', False),
 'galeria-volumes': ('Pierre Châtel-Innocenti', 'edificio-de-concreto-branco-h9ek6QA2jOU', 'Volumes brancos escalonados contra o céu do entardecer', False),
 'galeria-pergolado': ('juan verdaguer aguerrebehere', 'uma-casa-moderna-com-um-telhado-pergolado-0n94KqRz6rQ', 'Casa branca com pergolado e jardim lateral', False),
 'galeria-tijolo': ('Javier Garcia Chavez', 'estrutura-arquitetonica-moderna-com-aberturas-geometricas-e-iluminacao-quente-b1kNxnBrA6s', 'Estrutura de tijolos com aberturas triangulares iluminadas', False),
 'galeria-casa-mar': ('Maverick Frame', 'casa-branca-moderna-com-grandes-janelas-com-vista-para-o-oceano-rXq2vzsuLRg', 'Casa branca sobre campo aberto perto do mar', False),
 'galeria-hall': ('Ricardo Gomez Angel', 'uma-grande-sala-vazia-nnvV60Qn-bg', 'Hall de pé-direito alto em concreto claro', False),
 'material-banho': ('Peter Muniz', 'banheiro-moderno-com-chuveiro-de-marmore-e-iluminacao-ambiente-Uemj5k1cpY8', 'Banheiro em pedra com luz embutida', False),
 'galeria-suite': ('Puscas Adryan', 'quarto-luxuoso-com-uma-cama-grande-e-moveis-modernos-KXy7hKJ3EMc', 'Suíte ampla com poltrona e luz indireta', False),
 'galeria-cozinha': ('Jason Briscoe', 'ilha-de-madeira-branca-da-cozinha-e-armarios-perto-da-porta-do-painel-de-vidro-AQl-J19ocWE', 'Cozinha linear em madeira clara', False),
 'paisagismo-patio': ('Declan Sun', 'patio-moderno-com-arvore-verde-e-caminhos-curvos-ln1YU-sbZuQ', 'Pátio circular com árvore e caminhos curvos', False),
 'galeria-jardim-patio': ('Tommaso Ubezio', 'arvores-no-jardim-do-patio-com-sebes-iH9goCiy-UI', 'Jardim de pátio com árvores e cercas vivas', False),
 'galeria-terraco': ('SYKS', 'um-sofa-e-mesas-em-um-patio-com-vista-para-o-oceano-6Iif8DpllLw', 'Terraço com sofá de alvenaria e almofadas', False),
 'galeria-piscina': ('Roberto Nickson', 'mulher-nadando-na-piscina-infinita-ao-nascer-do-sol-dPBdgcSXHXY', 'Piscina de borda infinita ao nascer do sol', False),
 # AURORA: série única de perspectivas 3D (Aalo Lens)
 'aurora-torre': ('Aalo Lens', 'predio-de-apartamentos-moderno-ao-por-do-sol-com-arvores-e-carro-80CF4JbhlyM', 'Torre residencial ao entardecer, cercada de árvores', True),
 'aurora-entrada': ('Aalo Lens', 'casa-moderna-com-grandes-janelas-e-jardim-exuberante-eWOgoFHlE8g', 'Térreo envidraçado com jardim na entrada do edifício', True),
 'aurora-hall': ('Aalo Lens', 'entrada-de-edificio-moderno-com-caracteristica-da-agua-e-vegetacao-HQpFFY7eSEw', 'Hall de entrada com espelho d’água e vegetação', True),
 'aurora-elevadores': ('Aalo Lens', 'lobby-do-hotel-moderno-com-elevadores-e-detalhes-em-madeira-1PXsFfTbEcI', 'Hall dos elevadores com painéis de madeira', True),
 'aurora-living': ('Aalo Lens', 'sala-de-estar-moderna-com-grande-janela-e-vista-para-o-mar-Z30QQmCIppU', 'Sala de estar com janela de piso a teto', True),
 'aurora-sala': ('Aalo Lens', 'sala-de-estar-moderna-com-sofa-seccional-e-janela-grande-yxO8YG082v8', 'Sala com sofá seccional e painel de madeira', True),
 'aurora-academia': ('Aalo Lens', 'ginasio-moderno-com-equipamento-de-ginastica-e-vista-para-a-cidade-fuyulf8cNmg', 'Academia com vista para a cidade', True),
 'aurora-jardim': ('Aalo Lens', 'edificio-moderno-com-relvado-verde-e-arvores-_BeghWWtme0', 'Vista aérea do terraço-jardim', True),
 # JARDINS: série única de fotos de uma casa no vale (Caroline Badran)
 'jardins-jantar': ('Caroline Badran', 'sala-de-jantar-moderna-com-janelas-amplas-e-vista-panoramica-n2lSnn0tVKk', 'Sala de jantar aberta para o vale por grandes janelas', False),
 'jardins-living': ('Caroline Badran', 'sala-de-estar-moderna-com-grandes-janelas-e-vista-panoramica-12WFO8yWrsw', 'Sala de estar com teto de concreto e vista para as colinas', False),
 'jardins-cozinha': ('Caroline Badran', 'cozinha-moderna-e-sala-de-jantar-com-grandes-janelas-8FIqK2J7jSc', 'Cozinha integrada ao jantar, em madeira clara', False),
 'jardins-ilha': ('Caroline Badran', 'ilha-de-cozinha-moderna-com-bancos-de-bar-e-eletrodomesticos-OsnRGqOj4Bo', 'Ilha da cozinha vista através da porta de vidro', False),
 'jardins-mesa': ('Caroline Badran', 'mesa-de-jantar-com-vaso-e-ramos-floridos-AH1qU8YkyaQ', 'Mesa de madeira com vaso de flores diante da paisagem', False),
 'jardins-cozinha-concreto': ('Caroline Badran', 'ilha-de-cozinha-moderna-com-area-de-jantar-e-teto-de-concreto-FU13vB_pm_4', 'Ilha em pedra sob o teto de concreto aparente', False),
 # ATELIER: fachada + série única de interiores de um galpão de concreto (Neon Wang)
 'atelier-fachada': ('Jinish Shah', 'um-edificio-alto-com-varias-varandas-no-topo-dele-d844Y_wSgx4', 'Edifício de concreto aparente visto de baixo, com varandas em balanço', False),
 'atelier-loft': ('Neon Wang', 'moveis-modernos-de-lounge-no-estudio-l6YnCrvjVDY', 'Estar sob pé-direito alto, com mezanino e paredes de concreto', False),
 'atelier-vao': ('Neon Wang', 'estudio-industrial-com-paredes-de-concreto-GzMNrGthWns', 'Vão livre de concreto com mezanino metálico', False),
 'atelier-copa': ('Neon Wang', 'pia-de-cozinha-com-armarios-cinza-ayIDFHEA-Nk', 'Copa com armários cinza e azulejos brancos', False),
 'atelier-sala': ('Neon Wang', 'poltronas-modulares-bege-na-sala-de-estar-SYhavUIu43g', 'Poltronas bege diante de parede de concreto e cortina', False),
}

def webp_size(path):
    b = open(path, 'rb').read(40)
    kind = b[12:16]
    if kind == b'VP8 ':
        return int.from_bytes(b[26:28], 'little') & 0x3FFF, int.from_bytes(b[28:30], 'little') & 0x3FFF
    if kind == b'VP8L':
        bits = int.from_bytes(b[21:25], 'little')
        return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1
    if kind == b'VP8X':
        return int.from_bytes(b[24:27], 'little') + 1, int.from_bytes(b[27:30], 'little') + 1
    raise ValueError('WebP desconhecido: ' + str(path))

SIZE = {k: webp_size(f'img/{k}.webp') for k in P}
SM = {k: webp_size(f'img/sm/{k}.webp') for k in P}
MD = {k: webp_size(f'img/md/{k}.webp') for k in P if os.path.exists(f'img/md/{k}.webp')}
def srcset(k):
    parts = [f'img/sm/{k}.webp {SM[k][0]}w']
    if k in MD: parts.append(f'img/md/{k}.webp {MD[k][0]}w')
    parts.append(f'img/{k}.webp {SIZE[k][0]}w')
    return ', '.join(parts)
e = html.escape
def link(k): return 'https://unsplash.com/photos/' + P[k][1]
def author(k): return P[k][0]
def alt(k): return P[k][2]
def persp(k): return P[k][3]

# Largura que a imagem ocupa na tela: (celular, desktop) em vw. O celular vale até 860 px.
SIZES = {'full': (100, 100), 'hero': (100, 58), 'dev': (100, 56), 'half': (100, 45), 'third': (100, 32),
         'quarter': (100, 25), 'tower': (100, 40), 'floor': (100, 24), 'strip': (85, 50), 'tile': (50, 32), 'tile-wide': (50, 64)}
RATIO = {'r34': 3/4, 'r43': 4/3, 'r32': 3/2, 'r169': 16/9, 'r45': 4/5, 'r11': 1.0}

def sizes_attr(k, size, box=None, box_m=None):
    """Quando a foto é mais larga que a moldura (object-fit: cover), o navegador precisa de uma
    versão mais larga para preencher a altura sem ficar borrada; isto aumenta o 'sizes' na proporção."""
    w, h = SIZE[k]; r = w / h
    mob, desk = SIZES[size]
    bm = box_m if box_m else box
    fm = max(1.0, r / bm) if bm else 1.0
    fd = max(1.0, r / box) if box else 1.0
    return f'(max-width: 860px) {round(mob * fm)}vw, {round(desk * fd)}vw'

def img(k, size='half', eager=False, cls='', box=None, box_m=None):
    w, h = SIZE[k]
    if box is None:
        for c in cls.split():
            if c in RATIO: box = RATIO[c]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    src = (f'img/md/{k}.webp' if k in MD else f'img/{k}.webp') if eager else f'img/sm/{k}.webp'
    return (f'<img src="{src}" srcset="{srcset(k)}" sizes="{sizes_attr(k, size, box, box_m)}" '
            f'width="{w}" height="{h}" alt="{e(alt(k))}" {load} decoding="async"' + (f' class="{cls}"' if cls else '') + '>')

def credit(k):
    tag = '<span class="persp">Perspectiva ilustrada</span>' if persp(k) else ''
    kind = 'Imagem' if persp(k) else 'Foto'
    return f'{tag}<a href="{link(k)}" target="_blank" rel="noopener">{kind}: {e(author(k))} / Unsplash</a>'

def fig(k, cls='', ratio='', caption=None, size='half'):
    cap = (e(caption) + '. ' if caption else '') + credit(k)
    return f'<figure class="{cls} img-reveal"><div class="crop">{img(k, size, cls=ratio)}</div><figcaption>{cap}</figcaption></figure>'

MARK = '<svg class="brand-mark" viewBox="0 0 18 18" aria-hidden="true"><path d="M1 1 L9 17 L17 1" fill="none" stroke="#8A5F36" stroke-width="1.4"/><path d="M0 9.5 H18" stroke="currentColor" stroke-width=".8" opacity=".5"/></svg>'
ARROW_L = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M10 3 L5 8 L10 13"/></svg>'
ARROW_R = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6 3 L11 8 L6 13"/></svg>'

DEV_NAMES = {'aurora': 'Aurora', 'jardins': 'Jardins do Vale', 'atelier': 'Atelier 85'}

def header(current=None):
    """current=None na home; 'aurora' | 'jardins' | 'atelier' | 'creditos' nas internas."""
    if current is None:
        items = [('#sobre', 'Sobre'), ('#empreendimentos', 'Empreendimentos'), ('#arquitetura', 'Arquitetura'), ('#galeria', 'Galeria'), ('#localizacao', 'Localização')]
        links = ''.join(f'<a href="{h}">{t}</a>' for h, t in items)
        cta = '#contato'
    else:
        links = '<a href="index.html#sobre">Sobre</a>' + ''.join(
            f'<a href="{s}.html"' + (' aria-current="page"' if s == current else '') + f'>{n}</a>' for s, n in DEV_NAMES.items())
        links += '<a href="index.html#galeria">Galeria</a>'
        cta = f'index.html?empreendimento={current}#contato' if current in DEV_NAMES else 'index.html#contato'
    return f'''<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<div class="demo-bar" role="note"><strong>Projeto demonstrativo.</strong> <span class="demo-long">A VÉRTICE Residencial, seus empreendimentos, números e endereços são fictícios.</span><span class="demo-short">Empresa e dados fictícios.</span></div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="VÉRTICE Residencial, página inicial">{MARK}<span class="brand-name">VÉRTICE</span><span class="brand-sub">Residencial</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Abrir menu"><span></span><span></span></button>
    <nav class="nav" id="nav" aria-label="Principal">{links}<a class="btn" href="{cta}">Tenho interesse</a></nav>
  </div>
</header>'''

def footer():
    return '''<footer class="site-footer on-dark">
  <div class="wrap">
    <div class="foot-top">
      <div class="foot-brand">
        <span class="brand-name">VÉRTICE</span>
        <p>Incorporadora residencial fictícia, criada para demonstrar um site institucional de alto padrão.</p>
      </div>
      <div class="foot-col">
        <h2>Empreendimentos</h2>
        <ul><li><a href="aurora.html">Aurora</a></li><li><a href="jardins.html">Jardins do Vale</a></li><li><a href="atelier.html">Atelier 85</a></li></ul>
      </div>
      <div class="foot-col">
        <h2>Institucional</h2>
        <ul><li><a href="index.html#sobre">Sobre a VÉRTICE</a></li><li><a href="index.html#arquitetura">Arquitetura</a></li><li><a href="index.html#diferenciais">Como trabalhamos</a></li><li><a href="creditos.html">Créditos das imagens</a></li></ul>
      </div>
      <div class="foot-col">
        <h2>Atendimento</h2>
        <ul><li>Av. do Mirante, 1200<br>Bairro Mirante (endereço fictício)</li><li>Seg. a sex., 9h às 18h</li><li><a href="index.html#contato">Formulário de interesse</a></li></ul>
      </div>
      <div class="foot-col">
        <h2>Dados da empresa</h2>
        <ul><li>VÉRTICE Incorporações Ltda. (fictícia)</li><li>CNPJ 00.000.000/0000-00 (ilustrativo)</li><li>CRECI J-00000 (ilustrativo)</li></ul>
      </div>
    </div>
    <div class="foot-legal">
      <p class="disc">Site demonstrativo de portfólio. Empresa, empreendimentos, plantas, áreas, prazos, valores, endereços e mapas são fictícios e não constituem oferta. As imagens são de autores independentes publicadas no Unsplash sob a Licença Unsplash; as fotografias de casa e de interiores de concreto retratam obras reais de terceiros, usadas como referência, e as perspectivas do Aurora são ilustrações 3D.</p>
      <p class="copy">© <span data-year>2026</span> VÉRTICE Residencial (fictícia)</p>
    </div>
  </div>
</footer>'''

HEAD_SCRIPT = ("<script>document.documentElement.classList.add('js');"
               "setTimeout(function(){if(!window.VERTICE_OK){document.documentElement.classList.add('js-fail','loaded')}},2500)</script>")

def page(title, desc, body, cls='', current=None, extra_js='', fname='index.html'):
    base = '<base href="/">\n' if fname == '404.html' else ''  # a 404 aparece em qualquer endereço; caminhos partem da raiz
    og_img = (SITE_URL + '/img/og-vertice.jpg') if SITE_URL else 'img/og-vertice.jpg'
    og_url = f'<meta property="og:url" content="{SITE_URL}/{fname}">\n' if SITE_URL else ''
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#2B2A28">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="VÉRTICE Residencial (demonstrativo)">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Perspectiva ilustrada de uma torre residencial ao entardecer">
{og_url}<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/schibsted-grotesk-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/style.css">
{HEAD_SCRIPT}
</head>
<body class="{cls}">
{header(current)}
<main id="conteudo" tabindex="-1">
{body}
</main>
{footer()}
{extra_js}
<script src="js/main.js" defer></script>
</body>
</html>
'''

def other_devs(current):
    cards = {'aurora': ('aurora-torre', 'Torre residencial no Mirante'), 'jardins': ('jardins-jantar', 'Casas térreas no Vale Verde'), 'atelier': ('atelier-fachada', 'Estúdios e lofts no centro')}
    out = ''.join(f'<a href="{s}.html">{img(cards[s][0], "half", box=1.25)}<h3>{DEV_NAMES[s]}</h3><p class="small">{cards[s][1]}</p></a>' for s in DEV_NAMES if s != current)
    return f'''<section class="section tight" aria-labelledby="out-t">
  <div class="wrap">
    <h2 id="out-t" class="h3 mb-m">Outros empreendimentos</h2>
    <div class="other-devs">{out}</div>
  </div>
</section>'''

# ===========================================================================
# HOME
# ===========================================================================
DEVS = [
 dict(slug='aurora', status='Lançamento', place='Bairro Mirante', img='aurora-torre', tall=True,
      text='Torre de 16 pavimentos com quatro apartamentos por andar, salas nas quinas e um terraço-jardim no topo.',
      spec=[('Tipologia', '3 e 4 suítes'), ('Área privativa', '148 a 236 m²'), ('Unidades', '56'), ('Previsão de entrega', 'Dez. 2029')]),
 dict(slug='jardins', status='Em obras', place='Vale Verde', img='jardins-jantar', tall=False,
      text='Dezoito casas térreas em condomínio fechado, implantadas para preservar as árvores existentes e abrir as salas para o vale.',
      spec=[('Tipologia', 'Casas térreas, 4 suítes'), ('Terrenos', '600 a 820 m²'), ('Unidades', '18'), ('Previsão de entrega', 'Jun. 2028')]),
 dict(slug='atelier', status='Pronto para morar', place='Centro Histórico', img='atelier-fachada', tall=True,
      text='Estúdios e lofts em concreto aparente, a duas quadras da praça principal, com térreo aberto para cafés e ateliês de bairro.',
      spec=[('Tipologia', 'Estúdio, loft e duplex'), ('Área privativa', '38 a 112 m²'), ('Unidades', '64'), ('Entrega', 'Concluído em 2025')]),
]

def dev_block(d):
    name = DEV_NAMES[d['slug']]
    spec = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in d['spec'])
    return f'''<article class="dev{' tall' if d['tall'] else ''}">
  <a class="dev-media img-reveal" href="{d['slug']}.html" aria-label="Conhecer o {name}">{img(d['img'], 'dev', box=(0.8 if d['tall'] else 4/3), box_m=4/3)}</a>
  <div class="dev-info reveal">
    <p class="dev-status">{d['status']}</p>
    <h3>{name}</h3>
    <p class="place">{d['place']} (localização fictícia)</p>
    <p>{d['text']}</p>
    <dl class="spec">{spec}</dl>
    <a class="link" href="{d['slug']}.html">Conhecer o {name}</a>
    <p class="credit">{credit(d['img'])}</p>
  </div>
</article>'''

# galeria em linhas: L = larga (2 colunas). A ordem forma linhas completas de 3 colunas.
GALLERY = [
 ('galeria-torre-ripada', 'fachadas', 'Ripado curvo', 'L'), ('galeria-casa-encosta', 'fachadas', 'Casa entre rochas', ''),
 ('galeria-hall', 'interiores', 'Hall em concreto', ''), ('galeria-jardim-patio', 'paisagismo', 'Jardim de pátio', ''), ('galeria-fachada-pedra', 'fachadas', 'Módulos de pedra', ''),
 ('material-banho', 'interiores', 'Banho em pedra', ''), ('paisagismo-patio', 'paisagismo', 'Pátio circular', 'L'),
 ('galeria-volumes', 'fachadas', 'Volumes ao entardecer', ''), ('galeria-suite', 'interiores', 'Suíte', ''), ('galeria-piscina', 'paisagismo', 'Borda infinita', ''),
 ('galeria-pergolado', 'fachadas', 'Pergolado e jardim', 'L'), ('galeria-cozinha', 'interiores', 'Cozinha linear', ''),
 ('galeria-tijolo', 'fachadas', 'Aberturas em tijolo', ''), ('galeria-terraco', 'paisagismo', 'Terraço', ''), ('galeria-casa-mar', 'fachadas', 'Casa no campo', ''),
]
def gallery():
    out = ''
    for k, c, t, w in GALLERY:
        out += (f'<button class="tile{" wide" if w else ""}" type="button" data-cat="{c}" data-full="img/{k}.webp" data-caption="{e(t)}" '
                f'data-author="{e(author(k))}" data-link="{link(k)}" aria-label="Ampliar: {e(t)}">'
                f'<img src="img/sm/{k}.webp" srcset="{srcset(k)}" sizes="{sizes_attr(k, "tile-wide" if w else "tile", 1.65 if w else 0.8, 0.8)}" '
                f'width="{SM[k][0]}" height="{SM[k][1]}" alt="{e(alt(k))}" loading="lazy" decoding="async"><span class="cap">{e(t)}</span></button>')
    return out

POIS = [
 ('aurora', 'Aurora', 'Empreendimento', 'x', 440, 190), ('jardins', 'Jardins do Vale', 'Empreendimento', 'x', 170, 420),
 ('atelier', 'Atelier 85', 'Empreendimento', 'x', 640, 360), ('parque', 'Parque do Mirante', '6 min a pé do Aurora', 'p', 360, 120),
 ('escola', 'Colégio Horizonte', '8 min de carro do Jardins', 'p', 255, 330), ('mercado', 'Mercado Central', '4 min a pé do Atelier', 'p', 700, 430),
 ('hospital', 'Hospital Regional', '10 min de carro', 'p', 560, 250),
]

def map_svg():
    pins = ''
    for pid, name, _, kind, x, y in POIS:
        if kind == 'x':
            pins += (f'<g class="map-pin" data-poi="{pid}" tabindex="0" role="button" aria-pressed="false" aria-label="{name}">'
                     f'<circle class="pin-hit" cx="{x}" cy="{y}" r="24"/><circle class="pin-halo" cx="{x}" cy="{y}" r="26"/>'
                     f'<rect class="pin-core" x="{x-7}" y="{y-7}" width="14" height="14" transform="rotate(45 {x} {y})" fill="#2B2A28"/>'
                     f'<text x="{x+16}" y="{y+4}">{name}</text></g>')
        else:
            pins += (f'<g class="map-pin poi" data-poi="{pid}" tabindex="0" role="button" aria-pressed="false" aria-label="{name}">'
                     f'<circle class="pin-hit" cx="{x}" cy="{y}" r="20"/><circle class="pin-halo" cx="{x}" cy="{y}" r="20"/>'
                     f'<circle class="pin-core" cx="{x}" cy="{y}" r="6"/><text x="{x+12}" y="{y+4}">{name}</text></g>')
    return f'''<svg viewBox="0 0 860 560" role="group" aria-label="Mapa ilustrativo de uma cidade fictícia com os três empreendimentos e pontos de interesse. Selecione um ponto.">
<rect width="860" height="560" fill="#E7E2D8"/>
<path d="M-10 470 C 120 430 230 520 380 480 S 640 400 870 470 L870 570 L-10 570Z" fill="#D3DAD6"/>
<path d="M-10 478 C 120 438 230 528 380 488 S 640 408 870 478" fill="none" stroke="#B9C4C0" stroke-width="2"/>
<path d="M290 70 C 340 40 420 60 430 110 C 440 160 360 170 320 150 C 280 130 260 95 290 70Z" fill="#CFD3C2"/>
<path d="M90 370 C 130 340 220 350 230 400 C 240 450 150 470 110 450 C 70 430 60 395 90 370Z" fill="#CFD3C2" opacity=".8"/>
<g fill="none" stroke="#FBF9F5" stroke-linecap="round">
<path d="M-10 250 C 200 230 400 260 870 210" stroke-width="16"/>
<path d="M520 -10 C 500 150 560 330 620 570" stroke-width="12"/>
<path d="M-10 140 L 870 330" stroke-width="7"/>
<path d="M180 -10 C 200 200 150 350 200 570" stroke-width="7"/>
<path d="M660 300 L 860 300 M 660 340 L 860 380 M 600 380 L 860 430 M 700 260 L 700 470" stroke-width="5"/>
</g>
<g fill="#DED7CA">
<rect x="610" y="390" width="40" height="30"/><rect x="720" y="320" width="50" height="34"/><rect x="740" y="395" width="44" height="26"/><rect x="560" y="300" width="36" height="40"/><rect x="460" y="300" width="50" height="34"/><rect x="380" y="200" width="38" height="28" fill="#D5CCBC"/>
</g>
<text class="svg-street" x="40" y="236">Av. do Mirante</text>
<text class="svg-water" x="40" y="545">Rio das Pedras</text>
{pins}
<g transform="translate(800 60)"><circle r="18" fill="none" stroke="#8B847A"/><path d="M0 -12 L4 2 L0 0 L-4 2Z" fill="#2B2A28"/><text class="svg-north" y="34" text-anchor="middle">N</text></g>
</svg>'''

home_body = f'''
<section class="hero on-dark" aria-labelledby="hero-title">
  <div class="hero-copy">
    <div>
      <h1 id="hero-title"><span class="line"><span>Casas e</span></span><span class="line"><span>edifícios que</span></span><span class="line"><span>começam pelo lugar.</span></span></h1>
      <p class="fade">Projetamos cada empreendimento a partir do terreno: a luz de cada hora, as árvores que ficam, o caminho que as pessoas já fazem.</p>
      <div class="hero-actions fade"><a class="btn" href="#empreendimentos">Ver empreendimentos</a><a class="btn ghost" href="#sobre">Conhecer a VÉRTICE</a></div>
    </div>
    <div class="hero-meta fade">
      <div><b>17 entregues</b>desde 2009 (dado fictício)</div>
      <div><b>3 à venda</b>lançamento, obra e pronto</div>
      <span class="vertex-dot" aria-hidden="true"></span>
    </div>
  </div>
  <div class="hero-media">{img('hero-casa-horizonte', 'hero', eager=True, box=1.05)}</div>
  <span class="vertex" aria-hidden="true"></span>
  <p class="hero-caption">{credit('hero-casa-horizonte')}</p>
</section>

<section class="section about" id="sobre" aria-labelledby="sobre-t">
  <div class="wrap grid">
    <div class="about-statement">
      <p class="kicker">A incorporadora</p>
      <h2 id="sobre-t" class="serif-quote reveal">Fazemos poucos empreendimentos por vez, com os mesmos arquitetos do primeiro croqui à entrega das chaves.</h2>
      <div class="about-body reveal">
        <p>A VÉRTICE nasceu de um escritório de arquitetura que passou a incorporar os próprios projetos. Isso muda a ordem das decisões: primeiro estudamos o terreno e o desenho, depois o número de unidades.</p>
        <p>Cada obra tem um responsável técnico que acompanha o cliente até o fim da garantia. Relatórios mensais com fotos mostram o andamento real, sem maquete por cima.</p>
      </div>
    </div>
    {fig('institucional-concreto', 'about-figure', 'r43', 'Concreto aparente, matéria-prima frequente nos nossos projetos', 'third')}
    <dl class="facts">
      <div class="fact"><dt>17</dt><dd>empreendimentos entregues</dd></div>
      <div class="fact"><dt>1.240</dt><dd>famílias morando em projetos VÉRTICE</dd></div>
      <div class="fact"><dt>98%</dt><dd>das obras entregues no prazo contratado</dd></div>
      <div class="fact"><dt>5 anos</dt><dd>de assistência técnica após a entrega</dd></div>
    </dl>
    <p class="note col-full"><span class="demo-tag">Dados demonstrativos</span> Os números acima são fictícios e servem apenas para compor o layout.</p>
  </div>
</section>

<section class="section flush-top" id="empreendimentos" aria-labelledby="emp-t">
  <div class="wrap">
    <div class="dev-head">
      <h2 id="emp-t" class="h2">Três endereços, três formas de morar</h2>
      <p>Uma torre, um condomínio de casas e um edifício de estúdios. Cada um tem a própria página, com plantas e informações técnicas. <span class="demo-tag">Fictícios</span></p>
    </div>
    {''.join(dev_block(d) for d in DEVS)}
  </div>
</section>

<section class="section chapters" id="arquitetura" aria-label="Arquitetura, materiais e paisagismo">
  <div class="wrap">
    <article class="chapter" aria-labelledby="cap1">
      <div class="chapter-title">
        <p class="kicker">Arquitetura</p>
        <h2 id="cap1" class="h2">Luz antes da fachada</h2>
        <p>Antes de desenhar a planta, mapeamos o sol do terreno ao longo do ano. A posição das salas, dos beirais e das varandas sai desse estudo.</p>
      </div>
      <div class="chapter-body">
        <div class="chapter-figs">
          {fig('arquitetura-luz', 'a', 'r34', 'Laje em balanço sombreando a fachada', 'third')}
          {fig('detalhe-curva', 'b', 'r43', None, 'third')}
        </div>
        <div class="chapter-text reveal">
          <div><h3>Ventilação cruzada</h3><p>Toda unidade tem aberturas em duas faces opostas. O ar circula sem depender do ar-condicionado nas estações amenas.</p></div>
          <div><h3>Beirais e brises</h3><p>Proteções horizontais nas fachadas norte e brises verticais a oeste reduzem o calor sem fechar a vista.</p></div>
        </div>
      </div>
    </article>
    <article class="chapter" aria-labelledby="cap2">
      <div class="chapter-title">
        <p class="kicker">Materiais</p>
        <h2 id="cap2" class="h2">Poucos materiais, bem resolvidos</h2>
        <p>Concreto, pedra natural, madeira certificada e metal escovado. Materiais que envelhecem bem e não pedem pintura a cada dois anos.</p>
      </div>
      <div class="chapter-body">
        <div class="chapter-figs alt">
          {fig('material-concreto', 'a', 'r43', 'Marcas de fôrma no concreto aparente', 'half')}
          {fig('material-quina', 'b', 'r11', None, 'third')}
          {fig('material-detalhe', 'c', 'r45', 'Bancada em pedra com acabamento levigado', 'third')}
        </div>
        <div class="materials reveal">
          <div class="material"><div class="swatch sw-concreto"></div><b>Concreto aparente</b><span>Estrutura e fachadas</span></div>
          <div class="material"><div class="swatch sw-travertino"></div><b>Travertino</b><span>Pisos de áreas sociais</span></div>
          <div class="material"><div class="swatch sw-freijo"></div><b>Freijó certificado</b><span>Marcenaria e forros</span></div>
          <div class="material"><div class="swatch sw-bronze"></div><b>Bronze escovado</b><span>Metais e ferragens</span></div>
        </div>
      </div>
    </article>
    <article class="chapter" aria-labelledby="cap3">
      <div class="chapter-title">
        <p class="kicker">Paisagismo</p>
        <h2 id="cap3" class="h2">O jardim entra no projeto no primeiro dia</h2>
        <p>Árvores existentes são levantadas uma a uma e o desenho se acomoda a elas. Espécies nativas pedem menos água e atraem a fauna local.</p>
      </div>
      <div class="chapter-body">
        <div class="chapter-figs">
          {fig('paisagismo-esculturas', 'a', 'r34', 'Bambus e peças escultóricas no térreo', 'third')}
          {fig('paisagismo-noturno', 'b', 'r34', None, 'third')}
        </div>
        <div class="chapter-text reveal">
          <div><h3>Reuso de água</h3><p>Cisternas captam a chuva para a irrigação por gotejamento das áreas comuns.</p></div>
          <div><h3>Luz noturna baixa</h3><p>Balizadores próximos ao chão iluminam os caminhos sem ofuscar as janelas vizinhas.</p></div>
        </div>
      </div>
    </article>
  </div>
</section>

<section class="section" id="galeria" aria-labelledby="gal-t">
  <div class="wrap">
    <div class="gallery-head">
      <h2 id="gal-t" class="h2">Galeria de referências</h2>
      <div class="filters" role="group" aria-label="Filtrar imagens">
        <button class="filter" type="button" data-filter="todas" aria-pressed="true">Todas</button>
        <button class="filter" type="button" data-filter="fachadas" aria-pressed="false">Fachadas</button>
        <button class="filter" type="button" data-filter="interiores" aria-pressed="false">Interiores</button>
        <button class="filter" type="button" data-filter="paisagismo" aria-pressed="false">Paisagismo</button>
      </div>
    </div>
    <p class="small gallery-note">Fotografias de referência de autores do Unsplash, usadas para ilustrar a linguagem dos projetos. Não são obras da VÉRTICE. <span class="gallery-count" aria-live="polite">{len(GALLERY)} imagens</span></p>
    <div class="gallery-grid">{gallery()}</div>
  </div>
</section>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Imagem ampliada" inert>
  <div class="lb-top"><span class="lb-count"></span><button class="lb-btn lb-close" type="button" aria-label="Fechar"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3 L13 13 M13 3 L3 13"/></svg></button></div>
  <div class="lb-stage"><button class="lb-btn lb-prev" type="button" aria-label="Imagem anterior">{ARROW_L}</button><button class="lb-btn lb-next" type="button" aria-label="Próxima imagem">{ARROW_R}</button></div>
  <div class="lb-bottom"><span class="lb-caption"></span><span class="lb-credit"></span></div>
</div>

<section class="section diff on-dark" id="diferenciais" aria-labelledby="dif-t">
  <div class="wrap grid">
    <div class="diff-intro">
      <h2 id="dif-t" class="h2">Como trabalhamos</h2>
      <p>O que você pode cobrar de nós, por escrito, em qualquer empreendimento.</p>
    </div>
    <ul class="diff-list">
      <li class="reveal"><h3>Um arquiteto do início ao fim</h3><p>O mesmo responsável técnico conduz projeto, obra e entrega, e responde às suas dúvidas diretamente.</p></li>
      <li class="reveal"><h3>Obra aberta mensalmente</h3><p>Visitas guiadas ao canteiro uma vez por mês e relatório com fotos datadas no seu e-mail.</p></li>
      <li class="reveal"><h3>Personalização com prazo</h3><p>Até a fase de alvenaria você escolhe entre três layouts de planta e duas paletas de acabamento, sem custo.</p></li>
      <li class="reveal"><h3>Manual do proprietário claro</h3><p>Desenhos de instalações, fornecedores e rotinas de manutenção em um só documento, impresso e digital.</p></li>
      <li class="reveal"><h3>Assistência por cinco anos</h3><p>Chamados atendidos em até 72 horas úteis durante o período de garantia estrutural.</p></li>
    </ul>
  </div>
</section>

<section class="section loc" id="localizacao" aria-labelledby="loc-t">
  <div class="wrap grid">
    <div class="loc-text">
      <h2 id="loc-t" class="h2">Onde estamos</h2>
      <p>Três bairros com características diferentes, todos a menos de 15 minutos do centro. Selecione um ponto para destacá-lo no mapa.</p>
      <p><span class="demo-tag">Mapa ilustrativo</span> Cidade, ruas e distâncias são fictícias.</p>
      <ul class="poi-list">{''.join(f'<li><button type="button" data-poi="{pid}" aria-pressed="false"><span>{name}</span><span>{sub}</span></button></li>' for pid, name, sub, *_ in POIS)}</ul>
    </div>
    <div class="map-wrap reveal">{map_svg()}<span class="map-legend">Esquema sem escala</span></div>
  </div>
</section>

<section class="section contact" id="contato" aria-labelledby="ct-t">
  <div class="wrap grid">
    <div class="contact-intro">
      <h2 id="ct-t" class="h2">Quero saber mais</h2>
      <p>Deixe seus dados e o empreendimento de interesse. Em um site real, um consultor responderia em até um dia útil.</p>
      <p class="small"><span class="demo-tag">Formulário demonstrativo</span> Os campos são validados, mas nada é enviado nem armazenado.</p>
    </div>
    <form class="form" id="interest-form" novalidate data-whatsapp="{WHATSAPP}">
      <div class="field full"><label for="f-name">Nome completo</label><input id="f-name" name="name" type="text" autocomplete="name" required aria-describedby="err-name"><span class="error" id="err-name" aria-live="polite"></span></div>
      <div class="field"><label for="f-email">E-mail</label><input id="f-email" name="email" type="email" autocomplete="email" inputmode="email" required aria-describedby="err-email"><span class="error" id="err-email" aria-live="polite"></span></div>
      <div class="field"><label for="f-phone">Telefone com DDD</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="(00) 00000-0000" required aria-describedby="err-phone"><span class="error" id="err-phone" aria-live="polite"></span></div>
      <div class="field"><label for="f-project">Empreendimento</label><select id="f-project" name="project" required aria-describedby="err-project"><option value="">Selecione</option><option value="aurora">Aurora</option><option value="jardins">Jardins do Vale</option><option value="atelier">Atelier 85</option><option value="indefinido">Ainda não sei</option></select><span class="error" id="err-project" aria-live="polite"></span></div>
      <fieldset class="field"><legend>Você prefere</legend>
        <div class="choices"><label class="choice"><input type="radio" name="goal" value="info" id="f-goal-info" checked><span>Receber informações</span></label><label class="choice"><input type="radio" name="goal" value="visita" id="f-goal-visit"><span>Agendar uma visita</span></label></div>
      </fieldset>
      <fieldset class="field full"><legend>Melhor horário para contato <span class="opt">(opcional)</span></legend>
        <div class="choices"><label class="choice"><input type="radio" name="time" value="manha"><span>Manhã</span></label><label class="choice"><input type="radio" name="time" value="tarde"><span>Tarde</span></label><label class="choice"><input type="radio" name="time" value="noite"><span>Noite</span></label></div>
      </fieldset>
      <div class="field full"><label for="f-msg">Mensagem <span class="opt">(opcional)</span></label><textarea id="f-msg" name="message" maxlength="600"></textarea></div>
      <div class="field full"><label class="check"><input type="checkbox" name="consent" id="f-consent" aria-describedby="err-consent"><span>Entendo que este é um site demonstrativo e que meus dados não serão enviados a ninguém.</span></label><span class="error" id="err-consent" aria-live="polite"></span></div>
      <div class="form-actions"><button class="btn" type="submit">Validar meus dados</button><button class="btn ghost" type="button" id="wa-btn">Prefiro falar pelo WhatsApp</button><span class="small">Campos sem a marca “opcional” são obrigatórios.</span></div>
      <div class="wa-panel" id="wa-panel" hidden>
        <p><b>Demonstração:</b> em um site real, este botão abriria o WhatsApp do corretor com esta mensagem pronta.</p>
        <p class="wa-msg"></p>
        <div class="wa-actions"><button class="btn ghost wa-copy" type="button">Copiar mensagem</button><span class="small wa-done" aria-live="polite"></span></div>
      </div>
      <div class="form-status" id="form-status" role="status" tabindex="-1" hidden></div>
    </form>
  </div>
</section>
'''

# ===========================================================================
# AURORA (torre — vertical, escura) — 16 pavimentos
# ===========================================================================
FLOORS = {
 'terraco': dict(title='Terraço-jardim, 16º pavimento', text='Gramado, pergolado e área de estar no topo da torre, com vista aberta para o entardecer.', img='aurora-jardim'),
 'tipo': dict(title='Pavimentos tipo, 2º ao 15º', text='Quatro apartamentos por andar, com salas nas quinas abertas para duas fachadas. São 56 unidades no total.', img='aurora-living'),
 'lazer': dict(title='Lazer, 1º pavimento', text='Academia com vista para a cidade, sala de estudos e salão de festas, com acesso independente pela lateral.', img='aurora-academia'),
 'terreo': dict(title='Térreo', text='Hall de pé-direito duplo com espelho d’água, recepção 24 horas e bicicletário.', img='aurora-hall'),
}
floors_js = {k: dict(title=v['title'], text=v['text'], img=f"img/sm/{v['img']}.webp", srcset=srcset(v['img']), sizes=sizes_attr(v['img'], 'floor', 0.8), w=SM[v['img']][0], h=SM[v['img']][1],
                     alt=alt(v['img']), author=author(v['img']), link=link(v['img'])) for k, v in FLOORS.items()}

def tower_svg():
    y0, h = 20, 20
    parts = [f'<rect class="floor" data-floor="terraco" tabindex="0" role="button" aria-pressed="false" aria-label="Terraço-jardim" x="40" y="{y0}" width="120" height="{h*1.3:.0f}"/>']
    yt = y0 + h * 1.3 + 2
    parts.append(f'<rect class="floor active" data-floor="tipo" tabindex="0" role="button" aria-pressed="true" aria-label="Pavimentos tipo" x="30" y="{yt:.0f}" width="140" height="{h*14:.0f}"/>')
    lines = ''.join(f'<line x1="30" x2="170" y1="{yt + h*i:.0f}" y2="{yt + h*i:.0f}" stroke="rgba(255,255,255,.12)"/>' for i in range(1, 14))
    yl = yt + h * 14 + 2
    parts.append(f'<rect class="floor" data-floor="lazer" tabindex="0" role="button" aria-pressed="false" aria-label="Lazer" x="30" y="{yl:.0f}" width="140" height="{h*1.2:.0f}"/>')
    yr = yl + h * 1.2 + 2
    parts.append(f'<rect class="floor" data-floor="terreo" tabindex="0" role="button" aria-pressed="false" aria-label="Térreo" x="20" y="{yr:.0f}" width="160" height="{h*1.8:.0f}"/>')
    yg = yr + h * 1.8
    return (f'<svg viewBox="0 0 200 {yg+20:.0f}" role="group" aria-label="Corte esquemático da torre Aurora; selecione um pavimento">'
            + ''.join(parts) + f'<g pointer-events="none">{lines}</g>'
            + f'<line x1="0" x2="200" y1="{yg:.0f}" y2="{yg:.0f}" stroke="#C29A6B"/></svg>')

# ---- plantas: cômodos em metros; mesma escala nas três (1 m = 30 px) ----
S, OX, OY = 30, 40, 30
PLANS = [
 ('p148', '148 m²', 14, 10.6, [
   ('Varanda', 5, 0, 9, 2), ('Living e jantar', 5, 2, 9, 5), ('Cozinha', 9.5, 7, 4.5, 3.6), ('Hall', 5, 7, 4.5, 1.6),
   ('Lavabo', 5, 8.6, 1.6, 2), ('Serviço', 6.6, 8.6, 2.9, 2),
   ('Suíte 1', 0, 0, 3.6, 4.2), ('Banho', 3.6, 0, 1.4, 2.4), ('Closet', 3.6, 2.4, 1.4, 1.8),
   ('Suíte 2', 0, 4.2, 3.6, 3.2), ('Banho', 3.6, 4.2, 1.4, 2), ('Circ.', 3.6, 6.2, 1.4, 2.2),
   ('Suíte 3', 0, 7.4, 3.6, 3.2), ('Banho', 3.6, 8.4, 1.4, 2.2)],
  [(3.6, 5.2, 'v'), (3.6, 8.6, 'v'), (5, 7.4, 'v')],
  [(0.3, 0, 3, 'h'), (5.4, 0, 8.2, 'h'), (0, 0.6, 3, 'v'), (0, 4.6, 2.6, 'v'), (0, 7.8, 2.6, 'v'), (14, 2.6, 4, 'v')],
  [('Suítes', '3'), ('Vagas', '2'), ('Varanda', '18 m²'), ('Posição', 'Faces norte e leste')]),
 ('p196', '196 m²', 16, 12.25, [
   ('Varanda', 6, 0, 10, 2.4), ('Living integrado', 6, 2.4, 10, 5.2), ('Cozinha', 11, 7.6, 5, 4.65), ('Hall', 6, 7.6, 5, 2),
   ('Lavabo', 6, 9.6, 2.6, 2.65), ('Serviço', 8.6, 9.6, 2.4, 2.65),
   ('Suíte master', 0, 0, 4.4, 4.6), ('Closet', 4.4, 0, 1.6, 2.4), ('Banho', 4.4, 2.4, 1.6, 2.2),
   ('Suíte 2', 0, 4.6, 4.4, 3.6), ('Banho', 4.4, 4.6, 1.6, 2), ('Circ.', 4.4, 6.6, 1.6, 3),
   ('Suíte 3', 0, 8.2, 4.4, 4.05), ('Banho', 4.4, 9.6, 1.6, 2.65)],
  [(4.4, 5.6, 'v'), (4.4, 8.6, 'v'), (6, 8, 'v')],
  [(0.4, 0, 3.6, 'h'), (6.4, 0, 9.2, 'h'), (0, 0.6, 3.4, 'v'), (0, 5, 2.8, 'v'), (0, 8.8, 3, 'v'), (16, 2.8, 4.4, 'v')],
  [('Suítes', '3, com master ampliada'), ('Vagas', '3'), ('Varanda', '24 m²'), ('Posição', 'Quina noroeste')]),
 ('p236', '236 m²', 18, 13.1, [
   ('Varanda', 7, 0, 11, 2.6), ('Living', 7, 2.6, 7, 5.6), ('Suíte 4', 14, 2.6, 4, 4), ('Banho', 14, 6.6, 4, 1.6),
   ('Cozinha e gourmet', 11, 8.2, 7, 4.9), ('Hall', 7, 8.2, 4, 2.2), ('Lavabo', 7, 10.4, 1.8, 2.7), ('Serviço', 8.8, 10.4, 2.2, 2.7),
   ('Suíte master', 0, 0, 4.8, 5), ('Closet', 4.8, 0, 2.2, 2.6), ('Banho', 4.8, 2.6, 2.2, 2.4),
   ('Suíte 2', 0, 5, 4.8, 4), ('Banho', 4.8, 5, 2.2, 1.9), ('Circ.', 4.8, 6.9, 2.2, 4),
   ('Suíte 3', 0, 9, 4.8, 4.1), ('Banho', 4.8, 10.9, 2.2, 2.2)],
  [(4.8, 6, 'v'), (4.8, 9.8, 'v'), (7, 8.6, 'v')],
  [(0.4, 0, 4, 'h'), (7.4, 0, 10.2, 'h'), (0, 0.6, 3.8, 'v'), (0, 5.6, 2.8, 'v'), (0, 9.6, 3, 'v'), (18, 2.8, 3.6, 'v')],
  [('Suítes', '4'), ('Vagas', '3'), ('Varanda', '29 m²'), ('Posição', '12º ao 15º pavimento, vista livre')]),
]

def plan_svg(label, W, H, rooms, doors, wins):
    X = lambda m: OX + m * S
    Y = lambda m: OY + m * S
    vb_h = OY + H * S + 70
    o = [f'<svg class="plan-svg" viewBox="0 0 620 {vb_h:.0f}" role="img" aria-label="Planta esquemática ilustrativa do apartamento de {label}">']
    for name, x, y, w, h in rooms:
        o.append(f'<rect class="room" x="{X(x):.1f}" y="{Y(y):.1f}" width="{w*S:.1f}" height="{h*S:.1f}"/>')
    o.append(f'<rect class="outer" x="{X(0)}" y="{Y(0)}" width="{W*S:.1f}" height="{H*S:.1f}"/>')
    for x, y, length, d in wins:
        if d == 'h': o.append(f'<line class="win" x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x+length):.1f}" y2="{Y(y):.1f}"/>')
        else: o.append(f'<line class="win" x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x):.1f}" y2="{Y(y+length):.1f}"/>')
    for x, y, d in doors:  # porta de 0,8 m com arco de abertura
        r = 0.8 * S
        if d == 'v':
            o.append(f'<line class="door-gap" x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x):.1f}" y2="{Y(y)+r:.1f}"/>')
            o.append(f'<path class="door" d="M{X(x):.1f} {Y(y):.1f} L{X(x)-r:.1f} {Y(y):.1f} A{r:.1f} {r:.1f} 0 0 0 {X(x):.1f} {Y(y)+r:.1f}"/>')
        else:
            o.append(f'<line class="door-gap" x1="{X(x):.1f}" y1="{Y(y):.1f}" x2="{X(x)+r:.1f}" y2="{Y(y):.1f}"/>')
            o.append(f'<path class="door" d="M{X(x):.1f} {Y(y):.1f} L{X(x):.1f} {Y(y)-r:.1f} A{r:.1f} {r:.1f} 0 0 1 {X(x)+r:.1f} {Y(y):.1f}"/>')
    for name, x, y, w, h in rooms:
        cx, cy = X(x + w / 2), Y(y + h / 2)
        area = w * h
        if w * S >= 70 and h * S >= 46:
            o.append(f'<text class="rl" x="{cx:.1f}" y="{cy-2:.1f}" text-anchor="middle">{name}</text>'
                     f'<text class="ra" x="{cx:.1f}" y="{cy+13:.1f}" text-anchor="middle">{area:.1f} m²</text>')
        else:
            o.append(f'<text class="rs" x="{cx:.1f}" y="{cy+3:.1f}" text-anchor="middle">{name}</text>')
    sy = OY + H * S + 34
    o.append(f'<g class="scale"><rect class="f" x="{OX}" y="{sy}" width="{S*1}" height="5"/><rect x="{OX+S}" y="{sy}" width="{S*1}" height="5"/>'
             f'<rect class="f" x="{OX+2*S}" y="{sy}" width="{S*3}" height="5"/>'
             f'<text x="{OX}" y="{sy+20}">0</text><text x="{OX+2*S}" y="{sy+20}" text-anchor="middle">2</text><text x="{OX+5*S}" y="{sy+20}" text-anchor="middle">5 m</text></g>')
    o.append(f'<g class="north" transform="translate(590 {sy+4})"><path d="M0 -14 L5 4 L0 0 L-5 4Z"/><text y="20" text-anchor="middle">N</text></g>')
    o.append('</svg>')
    return ''.join(o)

def fmt_area(svg):  # 12.5 m² -> 12,5 m²
    import re
    return re.sub(r'(\d+)\.(\d) m²', r'\1,\2 m²', svg)

def plans_block():
    tabs = ''.join(f'<button class="tab" type="button" role="tab" id="t-{pid}" aria-controls="{pid}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{label}</button>'
                   for i, (pid, label, *_) in enumerate(PLANS))
    panels = ''
    for i, (pid, label, W, H, rooms, doors, wins, spec) in enumerate(PLANS):
        sp = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in spec)
        panels += (f'<div class="plan-panel" role="tabpanel" id="{pid}" aria-labelledby="t-{pid}"{" hidden" if i else ""}>'
                   f'{fmt_area(plan_svg(label, W, H, rooms, doors, wins))}<dl class="spec">{sp}</dl></div>')
    return tabs, panels

tabs, panels = plans_block()
aurora_body = f'''
<div class="wrap"><p class="crumbs"><a href="index.html#empreendimentos">Empreendimentos</a> / Aurora</p></div>
<section class="wrap au-hero" aria-labelledby="au-t">
  <div class="au-title">
    <p class="dev-status status-light">Lançamento</p>
    <h1 id="au-t" class="display">Aurora</h1>
    <p>Torre residencial de 16 pavimentos no Bairro Mirante, com quatro apartamentos por andar e salas nas quinas, abertas para duas fachadas.</p>
    <p><span class="demo-tag">Empreendimento fictício</span></p>
  </div>
  <figure class="au-tower">{img('aurora-torre', 'tower', eager=True, box=3/4.6, box_m=0.8)}<figcaption>{credit('aurora-torre')}</figcaption></figure>
  <div class="au-spec">
    <div><b>148–236 m²</b><span>área privativa</span></div>
    <div><b>56 unidades</b><span>4 por andar</span></div>
    <div><b>Dez. 2029</b><span>previsão de entrega</span></div>
  </div>
</section>

<section class="section" aria-labelledby="corte-t">
  <div class="wrap au-section">
    <div class="section-cut">
      <h2 id="corte-t" class="h2">Do térreo ao terraço</h2>
      <p>Selecione um trecho do corte para ver o que acontece em cada nível da torre.</p>
      <ul class="floor-steps">
        <li><button type="button" data-floor="terraco" aria-pressed="false"><span>Terraço-jardim</span><span>16º</span></button></li>
        <li><button type="button" data-floor="tipo" aria-pressed="true"><span>Pavimentos tipo</span><span>2º a 15º</span></button></li>
        <li><button type="button" data-floor="lazer" aria-pressed="false"><span>Lazer</span><span>1º</span></button></li>
        <li><button type="button" data-floor="terreo" aria-pressed="false"><span>Térreo</span><span>0</span></button></li>
      </ul>
    </div>
    <div class="tower-svg">{tower_svg()}</div>
    <div class="floor-info" aria-live="polite">
      <h3 class="h3" id="floor-title">{FLOORS['tipo']['title']}</h3>
      <p id="floor-text">{FLOORS['tipo']['text']}</p>
      <figure><img id="floor-img" src="img/sm/aurora-living.webp" srcset="{srcset('aurora-living')}" sizes="{sizes_attr('aurora-living', 'floor', 0.8)}" alt="{e(alt('aurora-living'))}" width="{SM['aurora-living'][0]}" height="{SM['aurora-living'][1]}" loading="lazy"><figcaption id="floor-credit">{credit('aurora-living')}</figcaption></figure>
    </div>
  </div>
</section>

<section class="section tight" aria-labelledby="int-t">
  <div class="wrap">
    <h2 id="int-t" class="h2 reveal mw-10 mb-xl">Áreas comuns e interiores</h2>
    <div class="au-interiors">
      {fig('aurora-sala', 'i1', 'r32', 'Sala do apartamento de 196 m²', 'half')}
      {fig('aurora-elevadores', 'i2', 'r43', 'Hall dos elevadores', 'third')}
      {fig('aurora-entrada', 'i3', 'r169', 'Térreo envidraçado voltado para o jardim', 'half')}
    </div>
  </div>
</section>

<section class="section" aria-labelledby="pl-t">
  <div class="wrap plans">
    <div class="plans-head">
      <h2 id="pl-t" class="h2">Plantas</h2>
      <p class="muted-dark">Três tipologias, todas com varanda. Plantas esquemáticas e ilustrativas, na mesma escala.</p>
      <div class="tabs" role="tablist" aria-label="Tipologias do Aurora">{tabs}</div>
      <p class="small">Use as setas do teclado para trocar de planta.</p>
    </div>
    {panels}
  </div>
</section>

{other_devs('aurora')}
'''

# ===========================================================================
# JARDINS (casas térreas — horizontal, areia)
# ===========================================================================
LOTS = {}
lot_svg = []
status_cycle = ['free', 'sold', 'free', 'reserved', 'free', 'free', 'sold', 'free', 'reserved', 'free', 'free', 'sold', 'free', 'free', 'reserved', 'free', 'sold', 'free']
orient = ['Vale, a norte', 'Vale, a nordeste', 'Vale, a noroeste']
n = 0
for row in range(2):
    for col in range(9):
        n += 1
        x = 40 + col * 82
        y = 50 if row == 0 else 270
        hgt = 120 + (col % 3) * 10
        yy = y if row == 0 else y + (130 - hgt)
        s = status_cycle[n - 1]
        t = 600 + ((col * 37 + row * 53) % 221)
        LOTS[str(n)] = dict(s=s, t=t, a=310 + (t - 600) // 2, q=4, o=orient[(col + row) % len(orient)])
        st = dict(free='disponível', reserved='reservada', sold='vendida')[s]
        lot_svg.append(f'<rect class="lot {s}" data-lot="{n}" tabindex="0" role="button" aria-pressed="false" aria-label="Casa {n}, {st}" x="{x}" y="{yy}" width="72" height="{hgt}"/>'
                       f'<text class="lot-num{" on-sold" if s == "sold" else ""}" x="{x+36}" y="{yy + hgt/2 + 5:.0f}" text-anchor="middle">{n}</text>')
mp = f'''<svg viewBox="0 0 800 460" role="group" aria-label="Implantação ilustrativa do Jardins do Vale; selecione uma casa">
<rect width="800" height="460" fill="#E3DCCD"/>
<path d="M0 205 C 200 190 600 240 800 205 L 800 255 C 600 290 200 240 0 255Z" fill="#F7F5F0"/>
<path d="M0 230 C 200 215 600 265 800 230" fill="none" stroke="#C9BBA5" stroke-dasharray="8 8"/>
<circle cx="770" cy="60" r="22" fill="#C7CDB6"/><circle cx="20" cy="430" r="28" fill="#C7CDB6"/><circle cx="790" cy="430" r="18" fill="#C7CDB6"/>
{''.join(lot_svg)}
<text class="mp-note" x="400" y="440" text-anchor="middle">Portaria ao sul; o vale fica ao norte (esquema sem escala)</text>
</svg>'''

def strip_img(k):  # a faixa tem altura fixa (52vh, até 560 px): a largura depende da proporção da foto
    w, h = SIZE[k]; r = w / h
    return (f'<img src="img/sm/{k}.webp" srcset="{srcset(k)}" sizes="(max-width: 860px) {round(52 * r * 844 / 390)}vw, {round(560 * r)}px" '
            f'width="{w}" height="{h}" alt="{e(alt(k))}" loading="lazy" decoding="async">')

strip = ''.join(f'<figure>{strip_img(k)}<figcaption>{e(c)}. {credit(k)}</figcaption></figure>' for k, c in [
    ('jardins-cozinha', 'Cozinha integrada ao jantar'), ('jardins-mesa', 'Mesa voltada para o vale'), ('jardins-ilha', 'Ilha da cozinha vista do terraço')])

jardins_body = f'''
<div class="wrap"><p class="crumbs"><a href="index.html#empreendimentos">Empreendimentos</a> / Jardins do Vale</p></div>
<section class="jd-hero jd-top" aria-labelledby="jd-t">
  <img class="jd-hero-img" src="img/jardins-jantar.webp" srcset="{srcset('jardins-jantar')}" sizes="{sizes_attr('jardins-jantar', 'full', 2.3, 0.83)}" width="{SIZE['jardins-jantar'][0]}" height="{SIZE['jardins-jantar'][1]}" alt="{e(alt('jardins-jantar'))}" fetchpriority="high">
  <div class="wrap jd-hero-band">
    <div class="jd-hero-card">
      <p class="dev-status">Em obras</p>
      <h1 id="jd-t" class="display">Jardins do Vale</h1>
      <p class="lead">Dezoito casas térreas ao longo de uma rua curva, com as salas abertas para o vale e as árvores do terreno no lugar onde estavam.</p>
    </div>
    <div class="jd-hero-aside">
      <dl class="spec"><dt>Terrenos</dt><dd>600 a 820 m²</dd><dt>Casas</dt><dd>18 térreas, com 4 suítes</dd><dt>Área preservada</dt><dd>42% do terreno</dd><dt>Entrega prevista</dt><dd>Jun. 2028</dd></dl>
      <p class="small"><span class="demo-tag">Empreendimento fictício</span> As fotos desta página mostram uma casa real usada como referência de padrão. {credit('jardins-jantar')}</p>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="mp-t">
  <div class="wrap masterplan">
    <div class="mp-text">
      <h2 id="mp-t" class="h2">Implantação</h2>
      <p>As casas se alternam em profundidade para que nenhuma janela fique de frente para a do vizinho, e todas as salas olham para o vale. Selecione uma casa para ver os dados.</p>
      <div class="mp-legend"><span><i class="sw-free"></i>Disponível</span><span><i class="sw-res"></i>Reservada</span><span><i class="sw-sold"></i>Vendida</span></div>
      <div class="lot-card" id="lot-card" aria-live="polite"><p class="small">Nenhuma casa selecionada.</p></div>
    </div>
    <div class="mp-map reveal">{mp}</div>
    <p class="scroll-hint col-full">Arraste a implantação para os lados para ver todas as casas.</p>
  </div>
</section>

<section class="section tight flush-top" aria-labelledby="strip-t">
  <div class="wrap"><h2 id="strip-t" class="h2 mb-m">Um dia na casa</h2></div>
  <div class="jd-strip-wrap">
    <div class="strip-ctrl"><button type="button" data-dir="-1" aria-label="Imagens anteriores">{ARROW_L}</button><button type="button" data-dir="1" aria-label="Próximas imagens">{ARROW_R}</button></div>
    <section class="jd-strip" tabindex="0" aria-label="Faixa de fotos com rolagem horizontal">{strip}</section>
  </div>
</section>

<section class="section" aria-label="Detalhes da casa">
  <div class="wrap">
    <div class="jd-pair">
      <div class="img">{fig('jardins-living', '', 'r45', None, 'half')}</div>
      <div class="txt reveal"><h2 class="h3 mb-s">Salas que abrem por inteiro</h2><p>Panos de vidro de piso a teto e esquadrias embutidas deixam a sala e o terraço no mesmo nível, sem trilho aparente no piso.</p></div>
    </div>
    <div class="jd-pair rev mt-l">
      <div class="img">{fig('jardins-cozinha-concreto', '', 'r45', None, 'half')}</div>
      <div class="txt reveal"><h2 class="h3 mb-s">Concreto, pedra e madeira</h2><p>Teto em concreto aparente, ilha em pedra natural e marcenaria em madeira clara. Poucos materiais, repetidos em todas as casas.</p></div>
    </div>
  </div>
</section>

{other_devs('jardins')}
'''

# ===========================================================================
# ATELIER (urbano — módulos, concreto)
# ===========================================================================
atelier_body = f'''
<div class="wrap"><p class="crumbs"><a href="index.html#empreendimentos">Empreendimentos</a> / Atelier 85</p></div>
<section class="wrap at-hero" aria-labelledby="at-t">
  <h1 id="at-t" class="display">Atelier 85</h1>
  <figure class="at-hero-img">{img('atelier-fachada', 'half', eager=True)}<figcaption>Fachada de referência. {credit('atelier-fachada')}</figcaption></figure>
  <div class="at-hero-text">
    <div>
      <p class="dev-status">Pronto para morar</p>
      <p class="lead">Sessenta e quatro unidades em concreto aparente na Rua dos Ofícios, no Centro Histórico. O térreo é aberto para a calçada, com cafés e ateliês de bairro.</p>
      <p><span class="demo-tag">Empreendimento fictício</span></p>
      <a class="btn" href="index.html?empreendimento=atelier&amp;objetivo=visita#contato">Agendar uma visita</a>
    </div>
    <figure class="at-hero-img2 img-reveal"><div class="crop">{img('atelier-vao', 'half', box=1.5)}</div><figcaption>Vão livre com mezanino metálico. {credit('atelier-vao')}</figcaption></figure>
  </div>
</section>

<section class="section" aria-labelledby="mod-t">
  <div class="wrap">
    <h2 id="mod-t" class="h2 mw-11 mb-l">O que o prédio oferece</h2>
    <div class="modules">
      <div class="module"><h3>Térreo ativo</h3><p>Seis lojas pequenas com fachada para a rua e aluguel subsidiado para comércio local.</p></div>
      <div class="module img">{img('atelier-copa', 'quarter', box=1.4, box_m=1.2)}</div>
      <div class="module"><h3>Oficina comum</h3><p>Bancadas, ferramentas e armários para quem precisa de espaço de trabalho fora do apartamento.</p></div>
      <div class="module"><h3>Bicicletário</h3><p>Uma vaga por unidade e estação de reparo no subsolo.</p></div>
      <div class="module img wide">{img('atelier-loft', 'half', box=2.4, box_m=1.2)}</div>
      <div class="module"><h3>Lavanderia</h3><p>Máquinas compartilhadas no 1º andar, liberando área dentro dos estúdios.</p></div>
      <div class="module"><h3>Terraço-horta</h3><p>Canteiros coletivos e um pergolado para encontros no fim da tarde.</p></div>
    </div>
    <p class="credit">Interiores de um galpão de concreto real, usados como referência: {credit('atelier-copa')}</p>
  </div>
</section>

<section class="section tight flush-top" aria-labelledby="cmp-t">
  <div class="wrap at-split">
    <div class="l">
      <h2 id="cmp-t" class="h2">Três tamanhos</h2>
      <p>Compare as tipologias. Áreas e quantidades são demonstrativas.</p>
    </div>
    <div class="r table-scroll">
      <table class="compare">
        <caption>Comparativo de tipologias (dados fictícios)<span class="table-hint"> Arraste a tabela para o lado para ver todas as colunas.</span></caption>
        <thead><tr><td></td><th scope="col">Estúdio</th><th scope="col" class="hl">Loft</th><th scope="col">Duplex</th></tr></thead>
        <tbody>
          <tr><th scope="row">Área privativa</th><td>38 m²</td><td class="hl">64 m²</td><td>112 m²</td></tr>
          <tr><th scope="row">Pé-direito</th><td>2,80 m</td><td class="hl">5,20 m</td><td>2,80 m por pavimento</td></tr>
          <tr><th scope="row">Dormitórios</th><td>Integrado</td><td class="hl">1 no mezanino</td><td>2 suítes</td></tr>
          <tr><th scope="row">Varanda</th><td>Não</td><td class="hl">Sim, 6 m²</td><td>Sim, 14 m²</td></tr>
          <tr><th scope="row">Unidades</th><td>32</td><td class="hl">24</td><td>8</td></tr>
          <tr><th scope="row">Disponíveis</th><td>3</td><td class="hl">5</td><td>1</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="section tight" aria-labelledby="bairro-t">
  <div class="wrap at-split">
    <div class="l">
      <h2 id="bairro-t" class="h2">A pé, em até dez minutos</h2>
      <p>Distâncias estimadas em um bairro fictício.</p>
    </div>
    <div class="r">
      <dl class="spec">
        <dt>Praça principal</dt><dd>2 min</dd>
        <dt>Mercado Central</dt><dd>4 min</dd>
        <dt>Estação de metrô Ofícios</dt><dd>6 min</dd>
        <dt>Biblioteca municipal</dt><dd>7 min</dd>
        <dt>Parque linear do rio</dt><dd>10 min</dd>
      </dl>
      {fig('atelier-sala', '', 'r43', 'Estar de um loft, com parede de concreto e cortina de linho', 'half')}
    </div>
  </div>
</section>

{other_devs('atelier')}
'''

# ===========================================================================
# CRÉDITOS
# ===========================================================================
def grupo(k):
    if k.startswith('aurora-'): return 'Aurora (perspectivas 3D)'
    if k.startswith('jardins-'): return 'Jardins do Vale (casa de referência)'
    if k.startswith('atelier-'): return 'Atelier 85'
    return 'Institucional, capítulos e galeria'
ordem = ['Aurora (perspectivas 3D)', 'Jardins do Vale (casa de referência)', 'Atelier 85', 'Institucional, capítulos e galeria']
rows = ''
for g in ordem:
    rows += f'<tr><th scope="rowgroup" colspan="4" class="cr-group">{g}</th></tr>'
    for k in sorted(P):
        if grupo(k) == g:
            rows += (f'<tr><td><img src="img/thumb/{k}.webp" alt="" width="72" height="54" loading="lazy"></td><td>{e(alt(k))}</td>'
                     f'<td>{e(author(k))}</td><td><a href="{link(k)}" target="_blank" rel="noopener">Ver no Unsplash</a></td></tr>')
cred_body = f'''
<section class="section tight">
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Início</a> / Créditos</p>
    <h1 class="h2 title-page">Créditos das imagens</h1>
    <p class="measure">Todas as imagens foram obtidas no Unsplash e são distribuídas sob a <a class="link" href="https://unsplash.com/license" target="_blank" rel="noopener">Licença Unsplash</a>, que permite uso comercial e não comercial sem pedido de autorização. A licença não exige atribuição, mas os autores são creditados aqui e junto a cada imagem.</p>
    <p class="measure">Cada empreendimento usa uma única série: as perspectivas 3D do Aurora são do mesmo projeto; as fotos do Jardins do Vale mostram uma mesma casa real; os interiores do Atelier 85 mostram um mesmo galpão de concreto. Nenhuma imagem retrata obras da VÉRTICE, que é uma empresa fictícia.</p>
    <p class="small">Fontes tipográficas: Instrument Serif e Schibsted Grotesk, ambas sob a SIL Open Font License, hospedadas junto com o site.</p>
    <div class="table-scroll mt-m">
      <table class="credits-table"><thead><tr><th scope="col"><span class="sr-only">Miniatura</span></th><th scope="col">Imagem</th><th scope="col">Autor</th><th scope="col">Página original</th></tr></thead><tbody>{rows}</tbody></table>
    </div>
  </div>
</section>'''

# ===========================================================================
# GRAVA
# ===========================================================================
nf_body = '''
<section class="section nf">
  <div class="wrap">
    <p class="kicker">Erro 404</p>
    <h1 class="display">Página não encontrada</h1>
    <p class="lead">O endereço pode ter mudado ou ter sido digitado errado. Os empreendimentos continuam no mesmo lugar.</p>
    <p class="nf-links"><a class="btn" href="index.html">Ir para o início</a><a class="btn ghost" href="index.html#empreendimentos">Ver empreendimentos</a></p>
  </div>
</section>'''

pages = [
 ('index.html', 'VÉRTICE Residencial | Incorporadora (site demonstrativo)', 'Site demonstrativo de uma incorporadora residencial fictícia de alto padrão.', home_body, '', None, ''),
 ('aurora.html', 'Aurora | VÉRTICE Residencial (demonstrativo)', 'Torre residencial fictícia de 16 pavimentos, com apartamentos de 148 a 236 m².', aurora_body, 'p-aurora on-dark', 'aurora',
  f'<script>window.AURORA_FLOORS={json.dumps(floors_js, ensure_ascii=False)};</script>'),
 ('jardins.html', 'Jardins do Vale | VÉRTICE Residencial (demonstrativo)', 'Condomínio fictício de 18 casas térreas abertas para o vale.', jardins_body, 'p-jardins', 'jardins',
  f'<script>window.JARDINS_LOTS={json.dumps(LOTS, ensure_ascii=False)};</script>'),
 ('atelier.html', 'Atelier 85 | VÉRTICE Residencial (demonstrativo)', 'Edifício fictício de estúdios e lofts em concreto aparente.', atelier_body, 'p-atelier', 'atelier', ''),
 ('creditos.html', 'Créditos | VÉRTICE Residencial (demonstrativo)', 'Créditos das imagens usadas no site demonstrativo.', cred_body, '', 'creditos', ''),
 ('404.html', 'Página não encontrada | VÉRTICE Residencial (demonstrativo)', 'Página não encontrada.', nf_body, '', 'creditos', ''),
]
for fname, title, desc, body, cls, cur, js in pages:
    Path(fname).write_text(page(title, desc, body, cls, cur, js, fname), encoding='utf-8')
print('Páginas geradas:', ', '.join(p[0] for p in pages))
