/* 경영주치의 랜딩 초안 */
(function () {
  'use strict';

  var header = document.getElementById('header');
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  var float = document.getElementById('float');

  /* ---------- 스크롤에 따른 헤더 / 플로팅 버튼 ---------- */
  function onScroll() {
    var y = window.pageYOffset;
    header.classList.toggle('is-solid', y > 40);
    float.classList.toggle('is-on', y > 520);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* ---------- 모바일 메뉴 ---------- */
  burger.addEventListener('click', function () {
    var open = nav.classList.toggle('is-open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.closest('.nav__link')) {
      nav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    }
  });

  /* ---------- 현재 섹션 메뉴 표시 ---------- */
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav__link'));
  var sections = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(function (s) { spy.observe(s); });

    /* ---------- 등장 애니메이션 ---------- */
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- 아직 값이 없는 플로팅 버튼 ---------- */
  document.querySelectorAll('[data-pending]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      alert(el.getAttribute('data-pending'));
    });
  });

  /* ---------- 신청 폼 ---------- */
  var form = document.getElementById('applyForm');
  var msg = document.getElementById('formMsg');

  form.addEventListener('submit', function (e) {
    msg.className = 'form__msg';

    var required = form.querySelectorAll('[required]');
    for (var i = 0; i < required.length; i++) {
      var f = required[i];
      var empty = f.type === 'checkbox' ? !f.checked : !f.value.trim();
      if (empty) {
        e.preventDefault();
        msg.textContent = f.type === 'checkbox'
          ? '개인정보 수집·이용에 동의해 주세요.'
          : '기업명, 대표자 · 담당자명, 연락처를 입력해 주세요.';
        msg.classList.add('is-err');
        f.focus();
        return;
      }
    }

    /* Formspree 주소가 아직 없으면 전송하지 않고 안내만 한다 */
    if (form.getAttribute('action').indexOf('YOUR_FORM_ID') !== -1) {
      e.preventDefault();
      msg.textContent = '지금은 디자인 확인용 화면입니다. 접수 주소를 연결하면 실제로 전송됩니다.';
    }
  });
})();
