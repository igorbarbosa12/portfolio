/* ==========================================================
   BRASA Burger House — interface
   Depende de js/config.js e js/menu-data.js (carregados antes).
   ========================================================== */

(function () {
  'use strict';

  const { config, categories: CATEGORIES, menu: MENU } = window.BRASA;

  /* ---------- Utilidades ---------- */

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  const findItem = (id) => MENU.find((i) => i.id === id);
  const money = (v) => 'R$ ' + v.toFixed(2).replace('.', ',');
  const digits = (s) => String(s || '').replace(/\D/g, '');

  function waLink(message) {
    return 'https://wa.me/' + digits(config.whatsapp) + '?text=' + encodeURIComponent(message);
  }

  // Imagem responsiva: 800 px para telas pequenas e cards, 1600 px para telas grandes.
  function imgTag(name, alt, sizes, extra = '') {
    return `<img src="img/sm/${name}.jpg" srcset="img/sm/${name}.jpg 800w, img/${name}.jpg 1600w" sizes="${sizes}" alt="${alt}" loading="lazy" decoding="async" ${extra}>`;
  }

  const ICON = {
    plus: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>',
    minus: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><path d="M5 12h14"/></svg>',
    glass: '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#C27A4A" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 3h12l-1.6 16.2a2 2 0 0 1-2 1.8H9.6a2 2 0 0 1-2-1.8z"/><path d="M6.6 9h10.8"/></svg>'
  };

  /* ---------- Carrinho (estado) ---------- */

  const CART_KEY = 'brasa-cart';

  const cart = {
    items: load(),

    qty(id) { return this.items[id] || 0; },

    change(id, delta) {
      const q = this.qty(id) + delta;
      if (q > 0) this.items[id] = q;
      else delete this.items[id];
      save(this.items);
    },

    clear() { this.items = {}; save(this.items); },

    lines() {
      return Object.entries(this.items).map(([id, qty]) => {
        const item = findItem(id);
        return { ...item, qty, total: item.price * qty };
      });
    },

    totals(delivery = true) {
      const lines = this.lines();
      const count = lines.reduce((a, l) => a + l.qty, 0);
      const subtotal = lines.reduce((a, l) => a + l.total, 0);
      const fee = count && delivery ? config.deliveryFee : 0;
      return { lines, count, subtotal, fee, total: subtotal + fee };
    }
  };

  function load() {
    try {
      const saved = JSON.parse(localStorage.getItem(CART_KEY));
      if (saved && typeof saved === 'object') {
        return Object.fromEntries(Object.entries(saved).filter(([id, q]) => findItem(id) && q > 0));
      }
    } catch (e) { /* armazenamento indisponível */ }
    return {};
  }

  function save(items) {
    try { localStorage.setItem(CART_KEY, JSON.stringify(items)); } catch (e) { /* ignora */ }
  }

  /* ---------- Cardápio ---------- */

  let activeCat = 'all';
  const visibleItems = () => (activeCat === 'all' ? MENU : MENU.filter((i) => i.cat === activeCat));

  function renderFilters() {
    $('#filtros').innerHTML = CATEGORIES.map((c) => {
      const count = c.id === 'all' ? MENU.length : MENU.filter((i) => i.cat === c.id).length;
      return `<button type="button" class="filter" data-cat="${c.id}" aria-pressed="${c.id === activeCat}">${c.label} <span>${count}</span></button>`;
    }).join('');
  }

  function cardAction(item) {
    const qty = cart.qty(item.id);
    if (!qty) {
      return `<button type="button" class="add-btn" data-add="${item.id}">${ICON.plus}Adicionar <span class="sr-only">${item.name}</span></button>`;
    }
    return `<div class="stepper">
      <button type="button" class="stepper__btn" data-dec="${item.id}" aria-label="Remover um ${item.name}">${ICON.minus}</button>
      <span class="stepper__label">${qty} no carrinho</span>
      <button type="button" class="stepper__btn" data-inc="${item.id}" aria-label="Adicionar mais um ${item.name}">${ICON.plus}</button>
    </div>`;
  }

  function menuCard(item) {
    const media = item.img
      ? imgTag(item.img, item.alt, '(max-width: 640px) 100vw, 400px', 'width="800" height="600"')
      : `<div class="menu-card__drink">${ICON.glass}<span class="menu-card__drink-word" aria-hidden="true">${item.short}</span></div>`;
    const tag = item.tag ? `<span class="menu-card__tag">${item.tag}</span>` : '';
    return `<article class="menu-card" data-item="${item.id}">
      <div class="menu-card__media zoom">${media}${tag}</div>
      <div class="menu-card__body">
        <div class="menu-card__top">
          <h3>${item.name}</h3>
          <span class="price">${money(item.price)}</span>
        </div>
        <p class="menu-card__desc">${item.desc}</p>
        <div class="menu-card__action">${cardAction(item)}</div>
      </div>
    </article>`;
  }

  function renderMenu() {
    $('#menu-grid').innerHTML = visibleItems().map(menuCard).join('');
  }

  // Atualiza só os botões dos cards (sem recarregar as fotos), preservando o foco.
  function refreshCardActions(focusId) {
    $$('#menu-grid .menu-card').forEach((card) => {
      const item = findItem(card.dataset.item);
      $('.menu-card__action', card).innerHTML = cardAction(item);
    });
    if (focusId) {
      const card = $(`#menu-grid [data-item="${focusId}"]`);
      const target = card && ($('[data-inc]', card) || $('[data-add]', card));
      if (target) target.focus();
    }
  }

  /* ---------- Gaveta do carrinho ---------- */

  let view = 'cart'; // cart | checkout | done

  function setView(next) {
    view = next;
    $('#cart-view').hidden = view !== 'cart';
    $('#checkout-view').hidden = view !== 'checkout';
    $('#done-view').hidden = view !== 'done';
    $('#cart-title').textContent = { cart: 'Seu pedido', checkout: 'Finalizar', done: 'Pedido enviado' }[view];
    renderCart();
  }

  function isDelivery() {
    const checked = $('input[name="modo"]:checked');
    return !checked || checked.value === 'entrega';
  }

  function renderCart() {
    const t = cart.totals(view === 'checkout' ? isDelivery() : true);

    const badge = $('#cart-badge');
    badge.textContent = t.count;
    badge.hidden = t.count === 0;
    $('#cart-badge-label').textContent = t.count ? `, ${t.count} ${t.count === 1 ? 'item' : 'itens'}` : '';

    $('#cart-count').textContent = view === 'done' ? 'Obrigado!' : (t.count === 1 ? '1 item' : t.count + ' itens');

    // Lista
    $('#cart-empty').hidden = t.count > 0;
    $('#cart-foot').hidden = t.count === 0;
    $('#cart-lines').innerHTML = t.lines.map((l) => `
      <li class="cart-line">
        <div class="cart-line__thumb">${l.img ? `<img src="img/sm/${l.img}.jpg" alt="" width="72" height="72" loading="lazy">` : ''}</div>
        <div class="cart-line__main">
          <div class="cart-line__top">
            <p class="cart-line__name">${l.name}</p>
            <p class="cart-line__total">${money(l.total)}</p>
          </div>
          <div class="cart-line__bottom">
            <div class="qty" role="group" aria-label="Quantidade de ${l.name}">
              <button type="button" data-dec="${l.id}" aria-label="Diminuir ${l.name}">${ICON.minus}</button>
              <span aria-live="polite">${l.qty}</span>
              <button type="button" data-inc="${l.id}" aria-label="Aumentar ${l.name}">${ICON.plus}</button>
            </div>
            <button type="button" class="remove-btn" data-remove="${l.id}">Remover <span class="sr-only">${l.name}</span></button>
          </div>
        </div>
      </li>`).join('');

    // Totais (os mesmos campos aparecem na lista e no checkout)
    $$('[data-total="subtotal"]').forEach((el) => { el.textContent = money(t.subtotal); });
    $$('[data-total="fee"]').forEach((el) => { el.textContent = t.fee ? money(t.fee) : 'Grátis'; });
    $$('[data-total="total"]').forEach((el) => { el.textContent = money(t.total); });
    $('#checkout-fee-label').textContent = isDelivery() ? 'Entrega' : 'Retirada no balcão';

    // Checkout sem itens volta para a lista
    if (view === 'checkout' && t.count === 0) setView('cart');
  }

  /* ---------- Finalização (demonstrativa) ---------- */

  function buildMessage(form) {
    const delivery = form.modo.value === 'entrega';
    const t = cart.totals(delivery);
    const lines = [
      'Olá, BRASA Burger House! Quero fazer um pedido:',
      '',
      ...t.lines.map((l) => `${l.qty}x ${l.name} — ${money(l.total)}`),
      '',
      'Subtotal: ' + money(t.subtotal),
      (delivery ? 'Entrega: ' + money(t.fee) : 'Retirada no balcão'),
      'Total: ' + money(t.total),
      '',
      'Nome: ' + form.nome.value.trim(),
      delivery ? 'Endereço: ' + form.endereco.value.trim() : 'Vou retirar na loja',
      'Pagamento: ' + form.pagamento.value
    ];
    const obs = form.obs.value.trim();
    if (obs) lines.push('Observações: ' + obs);
    return lines.join('\n');
  }

  function validate(form) {
    let ok = true;
    const fields = [form.nome];
    if (form.modo.value === 'entrega') fields.push(form.endereco);
    [form.nome, form.endereco].forEach((f) => {
      f.removeAttribute('aria-invalid');
      $('#' + f.id + '-erro').hidden = true;
    });
    fields.forEach((f) => {
      if (!f.value.trim()) {
        ok = false;
        f.setAttribute('aria-invalid', 'true');
        $('#' + f.id + '-erro').hidden = false;
      }
    });
    if (!ok) $('[aria-invalid="true"]', form).focus();
    return ok;
  }

  function submitOrder(e) {
    e.preventDefault();
    const form = e.target;
    if (!validate(form)) return;
    const link = waLink(buildMessage(form));
    window.open(link, '_blank', 'noopener');
    $('#done-wa').href = link;
    cart.clear();
    form.reset();
    toggleAddress();
    refreshCardActions();
    setView('done');
    $('#done-title').focus();
  }

  function toggleAddress() {
    const delivery = isDelivery();
    $('#campo-endereco').hidden = !delivery;
    $('#endereco').required = delivery;
    renderCart();
  }

  /* ---------- Abrir/fechar gaveta (com foco preso dentro dela) ---------- */

  let lastFocus = null;
  const pageRegions = () => [$('#header'), $('main'), $('footer'), $('.skip-link')];

  function openCart() {
    lastFocus = document.activeElement;
    hideToast();
    closeMenu();
    if (view === 'done') setView('cart');
    $('#cart').hidden = false;
    pageRegions().forEach((el) => el && el.setAttribute('inert', ''));
    document.body.classList.add('no-scroll');
    $('#cart-close').focus();
  }

  function closeCart() {
    $('#cart').hidden = true;
    pageRegions().forEach((el) => el && el.removeAttribute('inert'));
    document.body.classList.remove('no-scroll');
    if (view === 'done') setView('cart');
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
  }

  function trapFocus(e) {
    if (e.key !== 'Tab' || $('#cart').hidden) return;
    const focusables = $$('#cart .cart__panel a[href], #cart .cart__panel button, #cart .cart__panel input, #cart .cart__panel select, #cart .cart__panel textarea')
      .filter((el) => !el.disabled && el.offsetParent !== null);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  /* ---------- Menu móvel ---------- */

  function toggleMenu() {
    const nav = $('#mobile-nav');
    const open = nav.hidden;
    nav.hidden = !open;
    $('#menu-toggle').setAttribute('aria-expanded', String(open));
    $('#menu-toggle').setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
  }

  function closeMenu() {
    $('#mobile-nav').hidden = true;
    $('#menu-toggle').setAttribute('aria-expanded', 'false');
    $('#menu-toggle').setAttribute('aria-label', 'Abrir menu');
  }

  /* ---------- Aviso "adicionado" ---------- */

  let toastTimer = null;

  function showToast(text) {
    if (!$('#cart').hidden) return;
    $('#toast-text').textContent = text;
    $('#toast').hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(hideToast, 2600);
  }

  function hideToast() { $('#toast').hidden = true; }

  /* ---------- Ações ---------- */

  function update(id, delta, focusId) {
    cart.change(id, delta);
    refreshCardActions(focusId);
    renderCart();
  }

  function addItem(id, fromMenu) {
    const item = findItem(id);
    if (!item) return;
    update(id, 1, fromMenu ? id : null);
    showToast(item.name + ' no carrinho');
    const badge = $('#cart-badge');
    badge.classList.remove('bump');
    void badge.offsetWidth; // reinicia a animação
    badge.classList.add('bump');
  }

  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-add],[data-inc],[data-dec],[data-remove],[data-cat],[data-open-cart],[data-close-cart],[data-view],#menu-toggle,#mobile-nav a');
    if (!t) return;
    const inMenu = !!t.closest('#menu-grid');

    if (t.dataset.add) return addItem(t.dataset.add, inMenu);
    if (t.dataset.inc) return update(t.dataset.inc, 1, inMenu ? t.dataset.inc : null);
    if (t.dataset.dec) return update(t.dataset.dec, -1, inMenu ? t.dataset.dec : null);
    if (t.dataset.remove) return update(t.dataset.remove, -cart.qty(t.dataset.remove));
    if (t.dataset.cat) {
      activeCat = t.dataset.cat;
      renderFilters();
      renderMenu();
      $(`[data-cat="${activeCat}"]`).focus();
      return;
    }
    if (t.dataset.view) {
      if (t.dataset.view === 'new') { setView('cart'); return closeCart(); }
      setView(t.dataset.view);
      const first = t.dataset.view === 'checkout' ? $('#nome') : $('#cart-close');
      if (first) first.focus();
      return;
    }
    if (t.hasAttribute('data-open-cart')) return openCart();
    if (t.hasAttribute('data-close-cart')) return closeCart();
    if (t.id === 'menu-toggle') return toggleMenu();
    if (t.closest('#mobile-nav')) return closeMenu();
  });

  document.addEventListener('keydown', (e) => {
    trapFocus(e);
    if (e.key !== 'Escape') return;
    if (!$('#cart').hidden) closeCart();
    else if (!$('#mobile-nav').hidden) { closeMenu(); $('#menu-toggle').focus(); }
  });

  /* ---------- Configuração aplicada à página ---------- */

  function applyConfig() {
    const general = waLink('Olá, BRASA Burger House! Gostaria de fazer um pedido.');
    $$('[data-wa]').forEach((a) => { a.href = general; });

    // Redes: sem perfil configurado, o ícone sai da página (nenhum link vazio).
    $$('[data-social]').forEach((a) => {
      const url = config.social[a.dataset.social];
      if (url) a.href = url;
      else if (a.dataset.fallback === 'text') a.replaceWith(Object.assign(document.createElement('span'), { className: a.className, textContent: a.textContent.replace('→', '').trim() }));
      else a.remove();
    });

    const phone = $('#contato-telefone');
    if (!config.phone.label) phone.remove();
    else if (config.phone.tel) phone.innerHTML = `<a href="tel:+${digits(config.phone.tel)}">${config.phone.label}</a>`;
    else phone.textContent = config.phone.label;

    const mail = $('#contato-email');
    if (config.email) mail.innerHTML = `<a href="mailto:${config.email}">${config.email}</a>`;
    else mail.remove();

    $$('[data-maps]').forEach((a) => {
      a.href = 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(config.mapsQuery);
    });

    $('#ano').textContent = new Date().getFullYear();
  }

  /* ---------- Efeitos ---------- */

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function createEmbers() {
    if (reduceMotion) return;
    const box = $('#embers');
    for (let i = 0; i < 14; i++) {
      const s = document.createElement('span');
      const size = 3 + Math.random() * 2.5;
      s.className = 'ember';
      s.style.left = 45 + Math.random() * 50 + '%';
      s.style.width = s.style.height = size + 'px';
      s.style.animationDelay = (Math.random() * 7).toFixed(2) + 's';
      s.style.animationDuration = (6 + Math.random() * 5).toFixed(2) + 's';
      box.appendChild(s);
    }
  }

  function setupReveal() {
    if (reduceMotion || !('IntersectionObserver' in window)) return;
    const targets = $$('.section__head, .best-grid, .steps, .gallery, .story__grid, .visit');
    targets.forEach((el) => el.classList.add('reveal'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    targets.forEach((el) => io.observe(el));
  }

  // Destaca no menu a seção que está na tela.
  function setupScrollSpy() {
    if (!('IntersectionObserver' in window)) return;
    const links = $$('.nav a');
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        links.forEach((a) => {
          const on = a.getAttribute('href') === '#' + entry.target.id;
          a.classList.toggle('is-active', on);
          if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach((a) => { const s = $(a.getAttribute('href')); if (s) io.observe(s); });
  }

  /* ---------- Início ---------- */

  function init() {
    applyConfig();
    renderFilters();
    renderMenu();
    renderCart();
    $('#checkout-form').addEventListener('submit', submitOrder);
    $$('input[name="modo"]').forEach((r) => r.addEventListener('change', toggleAddress));
    createEmbers();
    setupReveal();
    setupScrollSpy();
  }

  init();
})();
