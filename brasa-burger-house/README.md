# BRASA Burger House

Site institucional e cardápio com carrinho para a BRASA Burger House, hamburgueria artesanal (marca fictícia).
HTML, CSS e JavaScript puros: sem build, sem dependências. Abre direto no navegador e publica em qualquer hospedagem estática.

## Estrutura

```
├── index.html          página única: header, hero, destaques, cardápio, preparo, galeria, história, localização, rodapé, carrinho
├── 404.html            página de erro
├── css/style.css       todo o visual (cores e fontes em variáveis no topo)
├── js/config.js        WhatsApp, taxa de entrega, telefone, e-mail, redes, endereço do mapa
├── js/menu-data.js     categorias e produtos do cardápio
├── js/app.js           filtros, carrinho, finalização, menu móvel, animações
├── img/                fotos em 1600 px
├── img/sm/             as mesmas fotos em 800 px (celular e cards)
├── favicon.svg, site.webmanifest, robots.txt, sitemap.xml
└── netlify.toml        publicação e cabeçalhos de cache/segurança
```

## Antes de publicar

| O quê | Onde |
|---|---|
| Número do WhatsApp que recebe os pedidos | `js/config.js` → `whatsapp` (só dígitos, ex. `5511999998888`) |
| Telefone, e-mail, perfis nas redes | `js/config.js` (campo vazio = o item some da página) |
| Taxa de entrega | `js/config.js` → `deliveryFee` |
| Endereço e horários | `index.html` (seção `#visite` e o bloco `application/ld+json` no `<head>`) e `js/config.js` → `mapsQuery` |
| Produtos e preços | `js/menu-data.js` (os 4 destaques ficam em `index.html`, seção `#destaques`) |
| Domínio do site | troque `https://brasaburguerhouse.netlify.app` em `index.html`, `robots.txt` e `sitemap.xml` |

## Rodar localmente

Abra `index.html` no navegador, ou sirva a pasta:

```bash
npx serve .
```

## Publicar

**Netlify:** arraste a pasta em app.netlify.com/drop, ou conecte o repositório do GitHub (sem comando de build; diretório de publicação `.`).

**GitHub:**

```bash
git init
git add .
git commit -m "Site BRASA Burger House"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/brasa-burger-house.git
git push -u origin main
```

## Como funciona o pedido

1. O cliente adiciona produtos (o carrinho fica salvo no navegador).
2. Em **Finalizar pedido** informa nome, entrega ou retirada, endereço, pagamento e observações.
3. **Enviar pedido no WhatsApp** abre uma conversa com a lista de itens, totais e dados preenchidos, pronta para enviar.

Não há pagamento online nem banco de dados: a confirmação acontece no WhatsApp.

## Créditos

Fotos: [Unsplash](https://unsplash.com) (licença Unsplash). Fontes: Big Shoulders Display, Instrument Serif e Manrope (Google Fonts).
