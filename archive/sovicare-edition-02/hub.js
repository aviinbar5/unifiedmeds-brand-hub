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
