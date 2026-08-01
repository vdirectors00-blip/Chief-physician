/* 경영주치의 — 랜딩 + 서비스 상세 공통 */
(function () {
  'use strict';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  var header = $('#header');
  var burger = $('#burger');
  var nav = $('#nav');
  var floatBox = $('#float');

  /* ---------- 계측 (측정 ID 없으면 조용히 무시) ---------- */
  function track(name, params) {
    if (typeof window.gtag === 'function') window.gtag('event', name, params || {});
  }

  /* ---------- 스크롤에 따른 헤더 / 플로팅 버튼 ---------- */
  function onScroll() {
    var y = window.pageYOffset;
    if (header) header.classList.toggle('is-solid', y > 40);
    if (floatBox) floatBox.classList.toggle('is-on', y > 520);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  if (document.body.classList.contains('is-sub') && header) header.classList.add('is-solid');

  /* ---------- 모바일 메뉴 ---------- */
  if (burger && nav) {
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
  }

  /* ---------- 등장 애니메이션 + 현재 섹션 표시 ---------- */
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    $$('.reveal').forEach(function (el) { io.observe(el); });

    var links = $$('.nav__link').filter(function (a) {
      return (a.getAttribute('href') || '').charAt(0) === '#';
    });
    var sections = links.map(function (a) { return $(a.getAttribute('href')); }).filter(Boolean);

    if (sections.length) {
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          links.forEach(function (a) {
            a.classList.toggle('is-active', a.getAttribute('href') === '#' + en.target.id);
          });
        });
      }, { rootMargin: '-45% 0px -50% 0px' });
      sections.forEach(function (s) { spy.observe(s); });
    }
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- 사례 탭 ---------- */
  var tabs = $$('.case__tab');
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        var key = tab.getAttribute('data-case');
        tabs.forEach(function (t) {
          var on = t === tab;
          t.classList.toggle('is-active', on);
          t.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        $$('.case__rows').forEach(function (rows) {
          rows.classList.toggle('is-hidden', rows.getAttribute('data-case') !== key);
        });
        track('case_tab', { case_no: key });
      });
    });
  }

  /* ---------- 아직 값이 없는 연락 버튼 ---------- */
  $$('[data-pending]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      alert(el.getAttribute('data-pending'));
    });
  });

  /* ---------- 신청 버튼 클릭 계측 ---------- */
  $$('[data-cta]').forEach(function (el) {
    el.addEventListener('click', function () {
      track('cta_click', { position: el.getAttribute('data-cta') });
    });
  });

  /* ---------- 신청 폼 ---------- */
  var form = $('#applyForm');

  if (form) {
    var msg = $('#applyFormMsg');
    var body = $('#applyFormBody');
    var done = $('#applyFormDone');
    var source = $('input[name="유입경로"]', form);

    /* 어느 페이지에서 신청했는지 남긴다 */
    var pageName = (document.title || '').split('|')[0].trim();
    if (source) source.value = pageName + ' (' + location.pathname + ')';

    /* 상세페이지에서 왔으면 해당 상담분야를 미리 체크 */
    var preset = form.getAttribute('data-preset');
    if (preset) {
      var box = $('input[name="상담분야"][value="' + preset + '"]', form);
      if (box) box.checked = true;
    }

    function fail(text, field) {
      msg.textContent = text;
      msg.className = 'form__msg is-err';
      if (field) field.focus();
    }

    form.addEventListener('submit', function (e) {
      msg.textContent = '';
      msg.className = 'form__msg';

      var required = form.querySelectorAll('[required]');
      for (var i = 0; i < required.length; i++) {
        var f = required[i];
        var empty = f.type === 'checkbox' ? !f.checked : !f.value.trim();
        if (empty) {
          e.preventDefault();
          fail(f.type === 'checkbox'
            ? '개인정보 수집·이용에 동의해 주세요.'
            : '기업명, 대표자 · 담당자명, 연락처를 입력해 주세요.', f);
          return;
        }
      }

      /* 접수 주소가 아직 없으면 전송하지 않고 안내만 */
      var action = form.getAttribute('action') || '';
      if (action.indexOf('YOUR_FORM_ID') !== -1) {
        e.preventDefault();
        msg.textContent = '지금은 디자인 확인용 화면입니다. 접수 주소를 연결하면 실제로 전송됩니다.';
        return;
      }

      /* fetch 를 못 쓰는 환경이면 기본 전송에 맡긴다 */
      if (!window.fetch || !window.FormData) return;

      e.preventDefault();
      var data = new FormData(form);
      form.classList.add('is-sending');
      msg.textContent = '전송 중입니다.';

      fetch(action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
        .then(function (res) {
          form.classList.remove('is-sending');
          if (!res.ok) throw new Error('bad status ' + res.status);

          track('generate_lead', {
            page: pageName,
            fields: (data.getAll('상담분야') || []).join(', ')
          });

          /* 알림 중계 주소가 있으면 함께 알린다 (없으면 건너뜀) */
          var hook = window.LEAD_WEBHOOK;
          if (hook) {
            var payload = {};
            data.forEach(function (v, k) { payload[k] = payload[k] ? payload[k] + ', ' + v : v; });
            fetch(hook, {
              method: 'POST',
              mode: 'no-cors',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            }).catch(function () { /* 알림 실패가 접수를 막지는 않는다 */ });
          }

          if (body && done) {
            body.hidden = true;
            done.hidden = false;
            done.scrollIntoView({ behavior: 'smooth', block: 'center' });
          } else {
            msg.textContent = '신청이 접수되었습니다. 확인 후 연락드리겠습니다.';
          }
        })
        .catch(function () {
          form.classList.remove('is-sending');
          fail('전송에 실패했습니다. 잠시 후 다시 시도하시거나 전화로 문의해 주세요.');
        });
    });
  }
})();
