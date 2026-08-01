# -*- coding: utf-8 -*-
"""랜딩과 서비스 상세가 함께 쓰는 신청 폼 / 계측 스니펫."""

# GA4: 측정 ID 가 비어 있으면 스크립트를 아예 불러오지 않는다 (오류도 전송도 없음)
GA = '''<!-- ============================================================
     TODO:GA4  구글 애널리틱스 측정 ID (G- 로 시작) 를 아래 따옴표 안에 넣으면
     수집이 시작됩니다. 비워두면 아무것도 불러오지 않고 전송하지도 않습니다.
     TODO:WEBHOOK  신청 접수를 문자·알림톡으로 받으려면 중계 주소를 넣습니다.
     (정적 사이트라 알리고를 직접 호출할 수 없어 중계가 하나 필요합니다)
     ============================================================ -->
<script>
  window.GA_ID = "";
  window.LEAD_WEBHOOK = "";
</script>
<script>
  (function () {
    var id = window.GA_ID;
    if (!id || id.indexOf("G-") !== 0) return;
    var s = document.createElement("script");
    s.async = 1; s.src = "https://www.googletagmanager.com/gtag/js?id=" + id;
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { dataLayer.push(arguments); };
    gtag("js", new Date());
    gtag("config", id);
  })();
</script>'''

FIELDS = [
    ('기업명', '기업명', 'text', True),
    ('대표자_담당자명', '대표자 · 담당자명', 'text', True),
    ('연락처', '연락처', 'tel', True),
    ('소재지', '소재지', 'text', False),
    ('연매출', '연 매출', 'text', False),
    ('세금완납여부', '세금 완납 여부', 'text', False),
]

PICKS = ['정책자금', '정부지원사업', '기업인증', '법인전환', '수출 바이어 매칭', '사옥 공장 매입', '기타']


def form(prefix='', preset='', form_id='applyForm', title=None, desc=None):
    """prefix: 하위 페이지면 '../'. preset: 미리 체크할 상담분야."""
    t = title or '기업 성장 가능성 사전진단 신청'
    d = desc or ('기업 현황을 남겨주시면 내용을 확인한 후 1차 상담을 통해 '
                 '현재 가장 먼저 검토해야 할 과제를 함께 살펴보겠습니다.')
    h = []
    h.append('    <div class="formbox reveal">\n')
    h.append('      <div class="formbox__body" id="%sBody">\n' % form_id)
    h.append('        <h3 class="formbox__title">%s</h3>\n' % t)
    h.append('        <p class="formbox__desc">%s</p>\n' % d)
    h.append('\n        <!-- TODO:FORM  Formspree 가입 후 아래 action 을 발급받은 주소로 교체하면 메일로 접수됩니다. -->\n')
    h.append('        <form class="form" id="%s" action="https://formspree.io/f/YOUR_FORM_ID" method="POST" novalidate%s>\n'
             % (form_id, (' data-preset="%s"' % preset) if preset else ''))
    h.append('          <input type="hidden" name="_subject" value="[경영주치의] 기업 현황 1차 진단 신청">\n')
    h.append('          <input type="hidden" name="유입경로" value="">\n')
    # 스팸 미끼: 사람 눈에는 안 보이고 봇만 채운다
    h.append('          <div class="hp" aria-hidden="true">\n')
    h.append('            <label>이 칸은 비워두세요<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>\n')
    h.append('          </div>\n')
    h.append('          <div class="form__grid">\n')
    for name, label, typ, req in FIELDS:
        ph = label if req else label + ' (선택)'
        h.append('            <label class="field"><span class="field__label">%s</span>'
                 '<input type="%s" name="%s" placeholder="%s"%s></label>\n'
                 % (label, typ, name, ph, ' required' if req else ''))
    h.append('          </div>\n\n')
    h.append('          <p class="form__legend">상담 분야 (중복 선택 가능)</p>\n')
    h.append('          <div class="form__chips">\n')
    for p in PICKS:
        h.append('            <label class="pick"><input type="checkbox" name="상담분야" value="%s"><span>%s</span></label>\n' % (p, p))
    h.append('          </div>\n\n')
    h.append('          <label class="agree">\n')
    h.append('            <input type="checkbox" name="개인정보동의" value="동의" required>\n')
    h.append('            <span>상담 진행을 위한 <a href="%sprivacy.html" target="_blank" rel="noopener">개인정보 수집·이용</a>에 동의합니다.</span>\n' % prefix)
    h.append('          </label>\n\n')
    h.append('          <button type="submit" class="btn btn--primary btn--block">기업 현황 1차 진단 신청</button>\n')
    h.append('          <p class="form__msg" id="%sMsg" role="status"></p>\n' % form_id)
    h.append('        </form>\n')
    h.append('      </div>\n\n')
    # 완료 화면
    h.append('      <div class="formdone" id="%sDone" hidden>\n' % form_id)
    h.append('        <div class="formdone__mark" aria-hidden="true"><svg viewBox="0 0 24 24">'
             '<path d="M4 12.5l5 5L20 6.5" fill="none" stroke="currentColor" stroke-width="2.2" '
             'stroke-linecap="round" stroke-linejoin="round"/></svg></div>\n')
    h.append('        <p class="formdone__title">신청이 접수되었습니다.</p>\n')
    h.append('        <p class="formdone__txt">남겨주신 기업 현황을 확인한 뒤 연락드리겠습니다.<br>'
             '먼저 확인이 필요하시면 전화로 문의해 주셔도 됩니다.</p>\n')
    h.append('      </div>\n')
    h.append('    </div>\n')
    return ''.join(h)
