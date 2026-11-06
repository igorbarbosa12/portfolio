/* ==========================================================
   BRASA Burger House — cardápio
   img: nome do arquivo em img/ (sem .jpg). Itens sem img mostram um bloco tipográfico.
   ========================================================== */

window.BRASA = window.BRASA || {};

window.BRASA.categories = [
  { id: 'all', label: 'Todos' },
  { id: 'burgers', label: 'Burgers' },
  { id: 'combos', label: 'Combos' },
  { id: 'sides', label: 'Acompanhamentos' },
  { id: 'drinks', label: 'Bebidas' }
];

window.BRASA.menu = [
  { id: 'b1', cat: 'burgers', name: 'Brasa Clássico', price: 38.9, img: 'brasa-classico', alt: 'Hambúrguer com blend grelhado, molho da casa e picles', desc: 'Blend 180 g na brasa, cheddar inglês, cebola caramelizada e maionese defumada no brioche tostado.' },
  { id: 'b2', cat: 'burgers', name: 'Fumaça Dupla', price: 52.9, tag: 'Mais pedido', img: 'fumaca-dupla', alt: 'Hambúrguer duplo com pastrami, cheddar derretido e pão tostado', desc: 'Dois smash de 120 g, pastrami defumado na casa, cheddar duplo, picles e molho brasa.' },
  { id: 'b3', cat: 'burgers', name: 'Cobre', price: 39.9, img: 'cobre', alt: 'Hambúrguer com queijo, alface, tomate e pão com gergelim', desc: 'Blend 180 g, queijo prato derretido, alface americana, tomate, cebola roxa e pão com gergelim.' },
  { id: 'b4', cat: 'burgers', name: 'Lenha & Bacon', price: 46.9, img: 'lenha-bacon', alt: 'Hambúrguer alto com bacon, queijo e salada', desc: 'Blend 180 g, bacon de barriga defumado 8 h, cheddar, cebola crispy e barbecue de rapadura.' },
  { id: 'b5', cat: 'burgers', name: 'Triplo Carvão', price: 54.9, tag: 'Para os fortes', img: 'triplo-carvao', alt: 'Hambúrguer triplo com cheddar escorrendo entre as carnes', desc: 'Três smash selados na grelha, american cheese triplo e o molho secreto da casa.' },
  { id: 'b6', cat: 'burgers', name: 'Brasa Raclette', price: 58.9, tag: 'Chef', img: 'brasa-raclette', alt: 'Hambúrguer coberto de queijo raclette derretido sobre tábua', desc: 'Blend 200 g, raclette derretido na hora sobre o burger, presunto cru e rúcula.' },
  { id: 'b7', cat: 'burgers', name: 'Smash Noir', price: 44.9, img: 'smash-noir', alt: 'Hambúrguer em pão escuro com queijo e folhas', desc: 'Pão australiano, dois smash de 90 g, cheddar, cebola na chapa e picles da casa.' },
  { id: 'b8', cat: 'burgers', name: 'Frango na Brasa', price: 36.9, img: 'frango-na-brasa', alt: 'Sanduíche de frango grelhado com coleslaw cremoso', desc: 'Sobrecoxa marinada e grelhada no carvão, coleslaw de repolho e maionese de limão.' },
  { id: 'c1', cat: 'combos', name: 'Combo Brasa', price: 54.9, tag: 'Combo', img: 'combo-brasa', alt: 'Hambúrguer servido em tábua com cesta de batatas fritas', desc: 'Brasa Clássico + batata rústica + refrigerante ou limonada.' },
  { id: 'c2', cat: 'combos', name: 'Combo Fumaça', price: 68.9, tag: 'Combo', img: 'combo-fumaca', alt: 'Hambúrguer com batatas rústicas sobre tábua escura', desc: 'Fumaça Dupla + fritas parmesão e trufa + chopp artesanal 300 ml.' },
  { id: 's1', cat: 'sides', name: 'Batata Rústica', price: 22.9, img: 'batata-rustica', alt: 'Batatas fritas em cesta de metal sobre mesa de madeira', desc: 'Corte rústico com casca, alecrim e flor de sal. Maionese defumada à parte.' },
  { id: 's2', cat: 'sides', name: 'Fritas Parmesão & Trufa', price: 26.9, img: 'fritas-parmesao-trufa', alt: 'Batatas fritas com parmesão ralado e salsinha em papel', desc: 'Fritas finas, parmesão curado, salsinha e um fio de azeite trufado.' },
  { id: 's3', cat: 'sides', name: 'Costelinha Defumada', price: 49.9, img: 'costelinha-defumada', alt: 'Costelinha suína defumada com barbecue e tomates', desc: 'Meia costela suína defumada por 6 h, barbecue de rapadura e picles.' },
  { id: 'd1', cat: 'drinks', name: 'Limonada Tostada', short: 'Limão', price: 14.9, img: 'limonada-tostada', alt: 'Limonada com metades de limão grelhado, hortelã, gelo e fio de mel', desc: 'Limões tostados na grelha, mel de laranjeira e hortelã.' },
  { id: 'd2', cat: 'drinks', name: 'Chopp Artesanal', short: 'Chopp', price: 19.9, img: 'chopp-artesanal', alt: 'Copo de chopp pilsen gelado com colarinho cremoso sobre tábua de madeira', desc: 'Pilsen da casa, 500 ml, servido na temperatura certa.' },
  { id: 'd3', cat: 'drinks', name: 'Refrigerante', short: 'Lata', price: 7.9, img: 'refrigerante', alt: 'Lata de refrigerante gelada ao lado de um copo com gelo', desc: 'Lata 350 ml — consulte os sabores do dia.' },
  { id: 'd4', cat: 'drinks', name: 'Shake Doce de Leite', short: 'Shake', price: 24.9, img: 'shake-doce-de-leite', alt: 'Milkshake com chantilly maçaricado e calda de doce de leite escorrendo', desc: 'Sorvete de baunilha com doce de leite queimado no maçarico.' }
];
