
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.shot-frame img, .showcase-frame img'))
    .filter(function (i) { return i.getAttribute('src').indexOf('shot-sync') === -1; });
  if (!imgs.length) return;

  imgs.forEach(function (img, idx) {
    img.setAttribute('data-zoom', idx);
    img.setAttribute('tabindex', '0');
    img.setAttribute('role', 'button');
    img.setAttribute('aria-label', 'Enlarge screenshot: ' + (img.alt || ''));
    var frame = img.closest('.shot-frame, .showcase-frame');
    if (frame) frame.classList.add('has-zoom');
    img.addEventListener('click', function () { openAt(idx, img); });
    img.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openAt(idx, img); }
    });
  });

  var ICON = {
    close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
  };
  var lb = document.createElement('div');
  lb.className = 'lb';
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', 'Screenshot viewer');
  lb.innerHTML =
    '<div class="lb-bar"><span class="lb-count" aria-live="polite"></span>' +
    '<button type="button" class="lb-btn lb-close" aria-label="Close (Esc)">' + ICON.close + '</button></div>' +
    '<div class="lb-stage">' +
      '<button type="button" class="lb-btn lb-nav lb-prev" aria-label="Previous screenshot">' + ICON.prev + '</button>' +
      '<div class="lb-scroll"><img class="lb-img" alt=""></div>' +
      '<button type="button" class="lb-btn lb-nav lb-next" aria-label="Next screenshot">' + ICON.next + '</button>' +
    '</div>' +
    '<div class="lb-cap"></div>';
  document.body.appendChild(lb);

  var elCount = lb.querySelector('.lb-count'), elImg = lb.querySelector('.lb-img'),
      elScroll = lb.querySelector('.lb-scroll'), elCap = lb.querySelector('.lb-cap'),
      btnClose = lb.querySelector('.lb-close'), btnPrev = lb.querySelector('.lb-prev'),
      btnNext = lb.querySelector('.lb-next');
  var cur = 0, opener = null;

  function show(i) {
    cur = (i + imgs.length) % imgs.length;
    var src = imgs[cur];
    elScroll.classList.remove('actual');
    elScroll.scrollTo(0, 0);
    elImg.src = src.currentSrc || src.src;
    elImg.alt = src.alt;
    elCount.textContent = (cur + 1) + ' / ' + imgs.length;
    elCap.innerHTML = '<b>' + escapeHtml(src.alt) + '</b><br>Tap or click the image to switch between fit and full size. Use the arrows to move between screens.';
  }
  function escapeHtml(t) { return String(t).replace(/[&<>"]/g, function (c) { return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function openAt(i, from) {
    opener = from || null;
    show(i);
    lb.classList.add('open');
    document.body.classList.add('lb-lock');
    btnClose.focus();
  }
  function close() {
    lb.classList.remove('open');
    document.body.classList.remove('lb-lock');
    if (opener) opener.focus();
  }

  btnClose.addEventListener('click', close);
  btnPrev.addEventListener('click', function () { show(cur - 1); });
  btnNext.addEventListener('click', function () { show(cur + 1); });
  elImg.addEventListener('click', function () { elScroll.classList.toggle('actual'); });
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target === elScroll || e.target.classList.contains('lb-stage')) close(); });

  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') { close(); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(cur - 1); }
    else if (e.key === 'ArrowRight') { e.preventDefault(); show(cur + 1); }
    else if (e.key === 'Tab') {
      var f = [btnClose, btnPrev, btnNext], i = f.indexOf(document.activeElement);
      e.preventDefault();
      f[(i + (e.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });

  // swipe on touch screens (only when fitted, so scrolling a full-size image still works)
  var sx = null, sy = null;
  lb.addEventListener('touchstart', function (e) { if (e.touches.length === 1) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; } else { sx = null; } }, { passive: true });
  lb.addEventListener('touchend', function (e) {
    if (sx === null || elScroll.classList.contains('actual')) return;
    var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
    if (Math.abs(dx) > 60 && Math.abs(dx) > Math.abs(dy) * 1.5) show(cur + (dx < 0 ? 1 : -1));
    sx = null;
  }, { passive: true });
})();
