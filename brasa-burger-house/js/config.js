/* ==========================================================
   BRASA Burger House — configuração
   Tudo o que muda de uma loja para outra fica aqui.
   ========================================================== */

window.BRASA = window.BRASA || {};

window.BRASA.config = {
  // Número de WhatsApp que recebe os pedidos: só dígitos, com DDI (55) e DDD.
  // Exemplo: '5511999998888'. Vazio = o WhatsApp abre para a pessoa escolher o contato.
  whatsapp: '',

  // Taxa de entrega (cobrada só quando o cliente escolhe "Entrega").
  deliveryFee: 6.9,

  // Telefone exibido no rodapé. Vazio = a linha some.
  phone: { label: '(11) 0000-0000', tel: '' }, // tel: só dígitos com DDI, ex. '551100000000'

  // E-mail de contato. Vazio = a linha some.
  email: 'contato@brasaburger.com.br',

  // Perfis nas redes. Vazio = o ícone some (nada de link quebrado).
  social: {
    instagram: '', // ex. 'https://instagram.com/brasaburgerhouse'
    tiktok: '',
    facebook: ''
  },

  // Texto usado no botão "Como chegar" (Google Maps).
  mapsQuery: 'Rua da Brasa, 400 - Vila Madalena, São Paulo - SP'
};
