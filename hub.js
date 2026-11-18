/* Brand hub chrome — mobile menu toggle. Navigation itself is static HTML in every page. */
(function () {
  var hub = document.querySelector('.hub');
  var btn = document.querySelector('.hub-toggle');
  if (!hub || !btn) return;
  btn.addEventListener('click', function () {
    var open = hub.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', String(open));
    document.body.style.overflow = open ? 'hidden' : '';
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && hub.classList.contains('is-open')) {
      hub.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
      btn.focus();
    }
  });
})();

/* Asset actions (16.11.2026): "View in Figma" and "Download" (SVG, or PNG at 1x, 2x or 4x), on any
   <div class="asset-actions" data-figma="8-23" data-files="assets/brand/logo-seal.svg|Primary seal;..."></div>
   data-figma: a node id in our Figma file. data-files: path|label pairs; SVG files also offer PNG. */
(function () {
  var FIGMA = 'https://www.figma.com/design/VqxGNn81aTddK6TOSeum3W?node-id=';
  var EXT = '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M16.2 8.8V3.8H11.2M16.2 3.8L9.6 10.4M14.2 12V15C14.2 15.8 13.5 16.5 12.7 16.5H5.3C4.5 16.5 3.8 15.8 3.8 15V7.6C3.8 6.8 4.5 6.1 5.3 6.1H8.2"/></svg>';
  var DOWN = '<svg viewBox="0 0 20 20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3.5V12.5M14 8.5L10 12.5L6 8.5M4 16.25H16"/></svg>';
  function save(href, name) { var a = document.createElement('a'); a.href = href; a.download = name; document.body.appendChild(a); a.click(); a.remove(); }
  function svgSize(text) {
    var d = new DOMParser().parseFromString(text, 'image/svg+xml').documentElement;
    var w = parseFloat(d.getAttribute('width')), h = parseFloat(d.getAttribute('height'));
    var vb = (d.getAttribute('viewBox') || '').split(/[\s,]+/).map(Number);
    if (!(w > 0 && h > 0) && vb.length === 4) { w = vb[2]; h = vb[3]; }
    return { w: w || 512, h: h || 512 };
  }
  function png(url, scale, name) {
    fetch(url).then(function (r) { return r.text(); }).then(function (text) {
      var s = svgSize(text), img = new Image();
      img.onload = function () {
        var c = document.createElement('canvas'); c.width = Math.round(s.w * scale); c.height = Math.round(s.h * scale);
        c.getContext('2d').drawImage(img, 0, 0, c.width, c.height);
        c.toBlob(function (b) { var u = URL.createObjectURL(b); save(u, name); setTimeout(function () { URL.revokeObjectURL(u); }, 1000); }, 'image/png');
      };
      img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(text)));
    });
  }
  document.querySelectorAll('.asset-actions').forEach(function (box) {
    var html = '';
    if (box.dataset.figma) html += '<a class="btn btn--outline btn--icon btn--header" href="' + FIGMA + box.dataset.figma + '" target="_blank" rel="noopener">View in Figma' + EXT.replace('<svg', '<svg class="btn-icon" data-dir="out"') + '</a>';
    var files = (box.dataset.files || '').split(';').filter(Boolean).map(function (f) { var p = f.split('|'); return { path: p[0], label: p[1] || p[0].split('/').pop() }; });
    if (files.length) {
      html += '<span class="asset-dl">';
      if (files.length > 1) html += '<select class="asset-file" aria-label="File">' + files.map(function (f, i) { return '<option value="' + i + '">' + f.label + '</option>'; }).join('') + '</select>';
      html += '<select class="asset-format" aria-label="Format"></select>';
      html += '<button class="btn btn--icon btn--header" type="button">Download' + DOWN.replace('<svg', '<svg class="btn-icon" data-dir="down"') + '</button></span>';
    }
    box.innerHTML = html;
    if (!files.length) return;
    var fileSel = box.querySelector('.asset-file'), fmt = box.querySelector('.asset-format');
    function current() { return files[fileSel ? +fileSel.value : 0]; }
    function formats() {
      var f = current(), ext = f.path.split('.').pop().toLowerCase();
      fmt.innerHTML = ext === 'svg' ? '<option value="svg">SVG</option><option value="1">PNG 1x</option><option value="2">PNG 2x</option><option value="4">PNG 4x</option>' : '<option value="file">' + ext.toUpperCase() + '</option>';
    }
    formats(); if (fileSel) fileSel.addEventListener('change', formats);
    box.querySelector('button').addEventListener('click', function () {
      var f = current(), base = f.path.split('/').pop().replace(/\.[^.]+$/, ''), v = fmt.value;
      if (v === 'svg' || v === 'file') save(f.path, f.path.split('/').pop());
      else png(f.path, +v, base + (v === '1' ? '' : '@' + v + 'x') + '.png');
    });
  });
})();

/* Search (Edition 04, 18.11.2026): one dialog over window.HUB_INDEX (pages, sections, rules, colours, files).
   Open with the search button, Cmd/Ctrl+K or "/". Arrow keys move, Enter opens, Esc closes. Hebrew words match pages. */
(function () {
  var dlg = document.querySelector('dialog.hub-search');
  if (!dlg) return;
  var input = dlg.querySelector('input'), list = dlg.querySelector('.hub-search-list'), hint = dlg.querySelector('.hub-search-hint');
  var KIND = { page: 'Page', section: 'Section', rule: 'Rule', decision: 'Decision', colour: 'Colour', file: 'File' };
  var WEIGHT = { page: 6, rule: 5, decision: 4, section: 3, colour: 3, file: 1 };
  var sel = 0, results = [];
  function norm(s) { return String(s || '').toLowerCase().replace(/[֑-ׇ]/g, '').replace(/\s+/g, ' ').trim(); }
  function score(item, terms, q) {
    var t = norm(item.t), d = norm(item.d), h = norm(item.h), s = 0;
    for (var i = 0; i < terms.length; i++) {
      var w = terms[i], hit = 0;
      if (t === w) hit = 40; else if (t.indexOf(w) === 0) hit = 25; else if (t.indexOf(w) > -1) hit = 15;
      else if (h.indexOf(w) > -1) hit = 14; else if (d.indexOf(w) > -1) hit = 6;
      if (!hit) return 0;
      s += hit;
    }
    if (t.indexOf(q) > -1) s += 10;
    return s + (WEIGHT[item.k] || 0);
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function render() {
    var q = norm(input.value), idx = window.HUB_INDEX || [];
    hint.hidden = !!q;
    if (!q) { list.innerHTML = ''; results = []; return; }
    var terms = q.split(' ');
    results = idx.map(function (it) { return { it: it, s: score(it, terms, q) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; }).slice(0, 40).map(function (r) { return r.it; });
    sel = 0;
    if (!results.length) { list.innerHTML = '<li class="empty">Nothing found for “' + esc(input.value) + '”. Try another word, a rule number or a colour.</li>'; return; }
    list.innerHTML = results.map(function (it, i) {
      return '<li><a role="option" id="sr-' + i + '" href="' + esc(it.u) + '"' + (i === 0 ? ' aria-selected="true"' : '') + '><b>' + esc(it.t) + '</b><span>' + esc(it.d || it.g || '') + '</span><em>' + (KIND[it.k] || '') + '</em></a></li>';
    }).join('');
  }
  function move(n) {
    var opts = list.querySelectorAll('a[role="option"]');
    if (!opts.length) return;
    opts[sel].removeAttribute('aria-selected');
    sel = (sel + n + opts.length) % opts.length;
    opts[sel].setAttribute('aria-selected', 'true');
    opts[sel].scrollIntoView({ block: 'nearest' });
  }
  function open() {
    var hub = document.querySelector('.hub'), btn = document.querySelector('.hub-toggle');
    if (hub && hub.classList.contains('is-open')) { hub.classList.remove('is-open'); document.body.style.overflow = ''; if (btn) btn.setAttribute('aria-expanded', 'false'); }
    if (!dlg.open) dlg.showModal();
    input.select(); render();
  }
  document.querySelectorAll('[data-search-open]').forEach(function (b) { b.addEventListener('click', open); });
  dlg.querySelector('.hub-search-close').addEventListener('click', function () { dlg.close(); });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  input.addEventListener('input', render);
  input.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowDown') { e.preventDefault(); move(1); }
    else if (e.key === 'ArrowUp') { e.preventDefault(); move(-1); }
    else if (e.key === 'Enter') { var a = list.querySelector('a[aria-selected="true"]'); if (a) { e.preventDefault(); dlg.close(); location.href = a.getAttribute('href'); } }
  });
  list.addEventListener('click', function (e) { if (e.target.closest('a')) dlg.close(); });
  document.addEventListener('keydown', function (e) {
    var typing = /^(INPUT|TEXTAREA|SELECT)$/.test((e.target && e.target.tagName) || '') || (e.target && e.target.isContentEditable);
    if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) { e.preventDefault(); open(); }
    else if (e.key === '/' && !typing && !dlg.open) { e.preventDefault(); open(); }
  });
  if (!/Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent)) document.querySelectorAll('.hub-search-btn kbd').forEach(function (k) { k.textContent = 'Ctrl K'; });
})();

/* Menu groups: the group of the current page opens; the open or closed state of the others is remembered per viewer. */
(function () {
  var KEY = 'um-hub-groups';
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}'); } catch (e) { saved = {}; }
  document.querySelectorAll('details.hub-group').forEach(function (d) {
    var g = d.getAttribute('data-group');
    var current = !!d.querySelector('[aria-current="page"]');
    if (!current && saved[g] === true) d.open = true;
    var sum = d.querySelector('summary');
    if (sum) sum.addEventListener('click', function () {
      setTimeout(function () {  /* only a viewer's click is remembered, never the initial open state */
        saved[g] = d.open;
        try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) { /* storage blocked: state is not kept */ }
      }, 0);
    });
  });
  var cur = document.querySelector('.hub-nav [aria-current="page"]');
  if (cur && cur.scrollIntoView) { var nav = document.querySelector('.hub-nav'); if (nav && cur.offsetTop > nav.clientHeight - 80) nav.scrollTop = cur.offsetTop - nav.clientHeight / 2; }
})();
