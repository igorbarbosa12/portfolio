/* VÉRTICE Residencial — site demonstrativo. Sem dependências. */
(function () {
  'use strict';
  /* avisa o <head> que o script carregou (se não carregar, o site mostra tudo sem animação) */
  window.VERTICE_OK = true;

  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var EMPREENDIMENTOS = { aurora: 'Aurora', jardins: 'Jardins do Vale', atelier: 'Atelier 85' };

  /* ---------- entrada da página (um único momento orquestrado) ---------- */
  function markLoaded() { requestAnimationFrame(function () { doc.classList.add('loaded'); }); }
  var heroImg = $('.hero-media img');
  if (heroImg && !heroImg.complete) {
    heroImg.addEventListener('load', markLoaded, { once: true });
    heroImg.addEventListener('error', markLoaded, { once: true });
    setTimeout(markLoaded, 1500);
  } else { markLoaded(); }

  /* ---------- cabeçalho ---------- */
  var header = $('.site-header');
  var nav = $('#nav');
  var toggle = $('.menu-toggle');
  var lastY = window.scrollY;
  function onScroll() {
    var y = window.scrollY;
    if (!header) return;
    header.classList.toggle('scrolled', y > 8);
    var menuOpen = nav && nav.classList.contains('open');
    if (!menuOpen && y > 320 && y > lastY + 4) header.classList.add('hidden');
    else if (y < lastY - 4 || y < 320) header.classList.remove('hidden');
    lastY = y;
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (header) header.addEventListener('focusin', function () { header.classList.remove('hidden'); });

  function menuIsOpen() { return nav && nav.classList.contains('open'); }
  function setMenu(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Fechar menu' : 'Abrir menu');
    document.body.classList.toggle('menu-open', open);
    if (open) { var first = $('a', nav); if (first) first.focus(); }
  }
  if (toggle) {
    toggle.addEventListener('click', function () { setMenu(toggle.getAttribute('aria-expanded') !== 'true'); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (!menuIsOpen()) return;
      if (e.key === 'Escape') { setMenu(false); toggle.focus(); return; }
      /* mantém o foco dentro do menu aberto: botão de fechar + links */
      if (e.key === 'Tab') {
        var items = [toggle].concat($$('a', nav));
        var i = items.indexOf(document.activeElement);
        if (e.shiftKey && (i <= 0)) { e.preventDefault(); items[items.length - 1].focus(); }
        else if (!e.shiftKey && (i === items.length - 1 || i === -1)) { e.preventDefault(); items[0].focus(); }
      }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 860 && menuIsOpen()) setMenu(false); });
  }

  /* destaque da seção atual no menu (só na home) */
  var navLinks = $$('#nav a[href^="#"]');
  if (navLinks.length && 'IntersectionObserver' in window) {
    var map = {};
    navLinks.forEach(function (a) { var t = $(a.getAttribute('href')); if (t) map[t.id] = a; });
    var secObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && map[en.target.id]) {
          navLinks.forEach(function (a) { a.classList.remove('active'); });
          map[en.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { secObs.observe(document.getElementById(id)); });
  }

  /* "Pular para o conteúdo": leva o foco junto */
  var skip = $('.skip');
  if (skip) skip.addEventListener('click', function () {
    var main = document.getElementById('conteudo');
    if (main) setTimeout(function () { main.focus({ preventScroll: true }); }, 0);
  });

  /* ---------- revelações discretas ---------- */
  var revealEls = $$('.reveal, .img-reveal');
  if (!reduce.matches && 'IntersectionObserver' in window) {
    var rObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); rObs.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    revealEls.forEach(function (el) { rObs.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in'); });
  }

  /* ---------- galeria: filtros ---------- */
  var grid = $('.gallery-grid');
  var tiles = $$('.tile');
  var filters = $$('.filter');
  var countEl = $('.gallery-count');
  function visibleTiles() { return tiles.filter(function (t) { return !t.hidden; }); }
  filters.forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.getAttribute('data-filter');
      filters.forEach(function (b) { b.setAttribute('aria-pressed', String(b === btn)); });
      tiles.forEach(function (t) { t.hidden = !(f === 'todas' || t.getAttribute('data-cat') === f); });
      if (grid) grid.classList.toggle('filtered', f !== 'todas');
      if (countEl) {
        var n = visibleTiles().length;
        countEl.textContent = n + (n === 1 ? ' imagem' : ' imagens');
      }
    });
  });

  /* ---------- galeria: imagem ampliada ---------- */
  var lb = $('#lightbox');
  if (lb && tiles.length) {
    var stage = $('.lb-stage', lb);
    var lbImg = null; /* criada na primeira abertura, já com a imagem certa */
    var lbCap = $('.lb-caption', lb);
    var lbCredit = $('.lb-credit', lb);
    var lbCount = $('.lb-count', lb);
    var list = [], idx = 0, opener = null;

    function show(i) {
      idx = (i + list.length) % list.length;
      var t = list[idx];
      if (!lbImg) {
        lbImg = document.createElement('img');
        lbImg.className = 'lb-img'; lbImg.alt = '';
        stage.insertBefore(lbImg, stage.firstChild);
      }
      lbImg.style.opacity = '0';
      var src = t.getAttribute('data-full');
      var pre = new Image();
      pre.onload = pre.onerror = function () {
        lbImg.src = src;
        lbImg.alt = t.querySelector('img').alt;
        lbImg.style.opacity = '1';
      };
      pre.src = src;
      lbCap.textContent = t.getAttribute('data-caption');
      lbCredit.textContent = '';
      var a = document.createElement('a');
      a.href = t.getAttribute('data-link');
      a.target = '_blank'; a.rel = 'noopener';
      a.textContent = 'Foto: ' + t.getAttribute('data-author') + ' / Unsplash';
      lbCredit.appendChild(a);
      lbCount.textContent = (idx + 1) + ' de ' + list.length;
    }
    function open(tile) {
      list = visibleTiles();
      opener = tile;
      show(list.indexOf(tile));
      lb.removeAttribute('inert');
      lb.classList.add('open');
      document.body.style.overflow = 'hidden';
      $('.lb-close', lb).focus();
    }
    function close() {
      lb.classList.remove('open');
      lb.setAttribute('inert', '');
      document.body.style.overflow = '';
      if (opener) opener.focus();
    }
    tiles.forEach(function (t) { t.addEventListener('click', function () { open(t); }); });
    $('.lb-close', lb).addEventListener('click', close);
    $('.lb-prev', lb).addEventListener('click', function () { show(idx - 1); });
    $('.lb-next', lb).addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === stage) close(); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('open')) return;
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight') show(idx + 1);
      else if (e.key === 'ArrowLeft') show(idx - 1);
      else if (e.key === 'Tab') {
        var f = $$('button, a[href]', lb);
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    var sx = null;
    lb.addEventListener('touchstart', function (e) { sx = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener('touchend', function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx;
      if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1));
      sx = null;
    });
  }

  /* ---------- mapa ilustrativo ---------- */
  var pins = $$('.map-pin');
  var poiBtns = $$('.poi-list button');
  function selectPoi(id) {
    pins.forEach(function (p) {
      var on = p.getAttribute('data-poi') === id;
      p.classList.toggle('active', on);
      p.setAttribute('aria-pressed', String(on));
    });
    poiBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-poi') === id)); });
  }
  poiBtns.forEach(function (b) { b.addEventListener('click', function () { selectPoi(b.getAttribute('data-poi')); }); });
  pins.forEach(function (p) {
    p.addEventListener('click', function () { selectPoi(p.getAttribute('data-poi')); });
    p.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); selectPoi(p.getAttribute('data-poi')); }
    });
  });

  /* ---------- abas acessíveis ---------- */
  $$('[role="tablist"]').forEach(function (tl) {
    var tabs = $$('[role="tab"]', tl);
    function activate(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute('aria-controls'));
        if (panel) panel.hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { activate(t); });
      t.addEventListener('keydown', function (e) {
        var n = null;
        if (e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
        if (e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === 'Home') n = tabs[0];
        if (e.key === 'End') n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); activate(n, true); }
      });
    });
  });

  /* ---------- Aurora: corte da torre ---------- */
  var floors = $$('.tower-svg .floor');
  var floorBtns = $$('.floor-steps button');
  var floorData = window.AURORA_FLOORS;
  if (floors.length && floorData) {
    var fTitle = $('#floor-title'), fText = $('#floor-text'), fImg = $('#floor-img'), fCredit = $('#floor-credit');
    var pickFloor = function (key) {
      var d = floorData[key]; if (!d) return;
      floors.forEach(function (f) {
        var on = f.getAttribute('data-floor') === key;
        f.classList.toggle('active', on);
        f.setAttribute('aria-pressed', String(on));
      });
      floorBtns.forEach(function (b) { b.setAttribute('aria-pressed', String(b.getAttribute('data-floor') === key)); });
      fTitle.textContent = d.title;
      fText.textContent = d.text;
      if (d.srcset) { fImg.srcset = d.srcset; fImg.sizes = d.sizes; }
      fImg.src = d.img; fImg.alt = d.alt;
      fImg.width = d.w; fImg.height = d.h;
      fCredit.textContent = '';
      var tag = document.createElement('span'); tag.className = 'persp'; tag.textContent = 'Perspectiva ilustrada';
      var a = document.createElement('a');
      a.href = d.link; a.target = '_blank'; a.rel = 'noopener';
      a.textContent = 'Imagem: ' + d.author + ' / Unsplash';
      fCredit.appendChild(tag); fCredit.appendChild(a);
    };
    floors.forEach(function (f) {
      f.addEventListener('click', function () { pickFloor(f.getAttribute('data-floor')); });
      f.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pickFloor(f.getAttribute('data-floor')); }
      });
    });
    floorBtns.forEach(function (b) { b.addEventListener('click', function () { pickFloor(b.getAttribute('data-floor')); }); });
  }

  /* ---------- Jardins: implantação ---------- */
  var lots = $$('.lot');
  var lotData = window.JARDINS_LOTS;
  if (lots.length && lotData) {
    var card = $('#lot-card');
    var statusLabel = { free: 'Disponível', reserved: 'Reservada', sold: 'Vendida' };
    var pickLot = function (el) {
      var d = lotData[el.getAttribute('data-lot')]; if (!d) return;
      lots.forEach(function (l) {
        var on = l === el;
        l.classList.toggle('active', on);
        l.setAttribute('aria-pressed', String(on));
      });
      card.textContent = '';
      var h = document.createElement('h3'); h.className = 'h3'; h.textContent = 'Casa ' + el.getAttribute('data-lot');
      var dl = document.createElement('dl'); dl.className = 'spec';
      [['Situação', statusLabel[d.s]], ['Terreno', d.t + ' m²'], ['Área construída', d.a + ' m²'], ['Suítes', d.q], ['Jardim voltado para', d.o]].forEach(function (r) {
        var dt = document.createElement('dt'); dt.textContent = r[0];
        var dd = document.createElement('dd'); dd.textContent = r[1];
        dl.appendChild(dt); dl.appendChild(dd);
      });
      var p = document.createElement('p'); p.className = 'small'; p.textContent = 'Dados demonstrativos.';
      card.appendChild(h); card.appendChild(dl); card.appendChild(p);
    };
    lots.forEach(function (l) {
      l.addEventListener('click', function () { pickLot(l); });
      l.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); pickLot(l); }
      });
    });
  }

  /* ---------- faixa horizontal: controles só quando há o que rolar ---------- */
  $$('.jd-strip-wrap').forEach(function (w) {
    var strip = $('.jd-strip', w);
    function check() { w.classList.toggle('static', strip.scrollWidth <= strip.clientWidth + 4); }
    $$('[data-dir]', w).forEach(function (b) {
      b.addEventListener('click', function () {
        strip.scrollBy({ left: Number(b.getAttribute('data-dir')) * strip.clientWidth * 0.8, behavior: reduce.matches ? 'auto' : 'smooth' });
      });
    });
    window.addEventListener('resize', check);
    window.addEventListener('load', check);
    check();
  });

  /* ---------- formulário de interesse (sem envio real) ---------- */
  var form = $('#interest-form');
  if (form) {
    /* empreendimento e objetivo vindos do link (ex.: index.html?empreendimento=aurora&objetivo=visita#contato) */
    var params = new URLSearchParams(window.location.search);
    var origem = params.get('empreendimento');
    if (origem && EMPREENDIMENTOS[origem]) form.elements.project.value = origem;
    if (params.get('objetivo') === 'visita') { var rv = $('#f-goal-visit', form); if (rv) rv.checked = true; }

    var phone = $('#f-phone', form);
    phone.addEventListener('input', function () {
      var d = phone.value.replace(/\D/g, '').slice(0, 11);
      var out = d;
      if (d.length > 2) out = '(' + d.slice(0, 2) + ') ' + d.slice(2);
      if (d.length > 7) out = '(' + d.slice(0, 2) + ') ' + d.slice(2, d.length - 4) + '-' + d.slice(d.length - 4);
      phone.value = out;
    });
    var rules = {
      name: function (v) { return v.trim().length >= 3 && /\s/.test(v.trim()) ? '' : 'Informe nome e sobrenome.'; },
      email: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : 'Informe um e-mail válido, como nome@exemplo.com.'; },
      phone: function (v) { var d = v.replace(/\D/g, ''); return (d.length === 10 || d.length === 11) ? '' : 'Informe o telefone com DDD, 10 ou 11 dígitos.'; },
      project: function (v) { return v ? '' : 'Escolha um empreendimento.'; },
      consent: function (v, el) { return el.checked ? '' : 'Marque para confirmar que leu o aviso.'; }
    };
    var check = function (el) {
      var rule = rules[el.name]; if (!rule) return true;
      var msg = rule(el.value, el);
      var field = el.closest('.field');
      var err = document.getElementById('err-' + el.name);
      if (field) field.classList.toggle('invalid', !!msg);
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (err) err.textContent = msg;
      return !msg;
    };
    $$('input, select, textarea', form).forEach(function (el) {
      el.addEventListener('blur', function () { if (el.value || el.type === 'checkbox') check(el); });
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
      el.addEventListener('change', function () { if (el.getAttribute('aria-invalid') === 'true') check(el); });
    });
    function goalText() { var g = form.elements.goal.value; return g === 'visita' ? 'agendar uma visita' : 'receber informações'; }
    function projectName() { var v = form.elements.project.value; return EMPREENDIMENTOS[v] || (v === 'indefinido' ? 'os empreendimentos' : ''); }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      Object.keys(rules).forEach(function (n) {
        var el = form.elements[n];
        if (!check(el) && !firstBad) firstBad = el;
      });
      var status = $('#form-status');
      if (firstBad) { status.hidden = true; firstBad.focus(); return; }
      var nome = form.elements.name.value.trim().split(/\s+/)[0];
      status.textContent = '';
      var b = document.createElement('b');
      b.textContent = 'Obrigado, ' + nome + '. Pedido para ' + goalText() + ' sobre ' + projectName() + ' validado.';
      var p = document.createElement('span');
      p.textContent = 'Este é um site demonstrativo: nada foi enviado nem armazenado, e ninguém vai entrar em contato. Em um projeto real, este pedido chegaria ao time comercial.';
      status.appendChild(b); status.appendChild(p);
      status.hidden = false;
      status.focus();
      form.reset();
      $$('[aria-invalid]', form).forEach(function (el) { el.removeAttribute('aria-invalid'); });
    });

    /* WhatsApp: com número configurado em data-whatsapp abre a conversa; sem número, mostra a mensagem pronta */
    var waBtn = $('#wa-btn'), waPanel = $('#wa-panel');
    if (waBtn && waPanel) {
      waBtn.addEventListener('click', function () {
        var nome = form.elements.name.value.trim();
        var msg = 'Olá! ' + (nome ? 'Sou ' + nome + ' e ' : '') + 'gostaria de ' + goalText() +
          (projectName() ? ' sobre ' + projectName() : ' sobre os empreendimentos da VÉRTICE') + '.';
        var numero = (form.getAttribute('data-whatsapp') || '').replace(/\D/g, '');
        if (numero) { window.location.href = 'https://wa.me/' + numero + '?text=' + encodeURIComponent(msg); return; }
        $('.wa-msg', waPanel).textContent = msg;
        waPanel.hidden = false;
        $('.wa-copy', waPanel).focus();
      });
      $('.wa-copy', waPanel).addEventListener('click', function () {
        var txt = $('.wa-msg', waPanel).textContent;
        var done = $('.wa-done', waPanel);
        function ok() { done.textContent = 'Mensagem copiada.'; }
        function fail() {
          var r = document.createRange(); r.selectNodeContents($('.wa-msg', waPanel));
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          done.textContent = 'Texto selecionado. Use Ctrl+C para copiar.';
        }
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(ok, fail); else fail();
      });
    }
  }

  /* ano no rodapé */
  $$('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });
})();
