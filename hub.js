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
