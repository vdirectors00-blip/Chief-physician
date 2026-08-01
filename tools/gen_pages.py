# -*- coding: utf-8 -*-
"""서비스 상세 6페이지 생성. 요청서 6번 본문 + 공개자료 리서치 반영."""
import io, os
from formtpl import form, GA

import os as _os
OUT = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "services")

ICONS = {
 'policy-fund': '<ellipse cx="12" cy="6" rx="7.5" ry="3"/><path d="M4.5 6v5.5c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3V6"/><path d="M4.5 11.5V17c0 1.7 3.4 3 7.5 3s7.5-1.3 7.5-3v-5.5"/>',
 'gov-program': '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M8.5 14.5l2.2 2.2 4.3-4.3"/>',
 'certification': '<path d="M12 3l7 3v5.7c0 4.3-2.9 8-7 9.3-4.1-1.3-7-5-7-9.3V6z"/><path d="M9 12l2.2 2.2L15.5 10"/>',
 'incorporation': '<path d="M3.5 8.5h13.5l-3.2-3.2"/><path d="M20.5 15.5H7l3.2 3.2"/>',
 'export': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.6 2.8 3.9 5.8 3.9 9s-1.3 6.2-3.9 9c-2.6-2.8-3.9-5.8-3.9-9S9.4 5.8 12 3z"/>',
 'asset': '<path d="M3 21h18"/><path d="M5.5 21V7.2L11 4.5V21"/><path d="M11 11.5l7.5-2.8V21"/><path d="M8 10h.01M8 14h.01M14.5 13h.01M14.5 17h.01"/>',
}

PRESET = {'policy-fund':'정책자금','gov-program':'정부지원사업','certification':'기업인증',
          'incorporation':'법인전환','export':'수출 바이어 매칭','asset':'사옥 공장 매입'}

# 상단 배경 사진. 랜딩 6대 서비스 카드와 같은 파일을 다시 써서 용량이 늘지 않는다.
PHOTO = {'policy-fund':'svc-fund','gov-program':'svc-gov','certification':'svc-cert',
         'incorporation':'svc-inc','export':'svc-export','asset':'svc-asset'}

NOTE = ('이 페이지의 내용은 공개된 제도 안내를 기준으로 정리한 것입니다. '
        '지원 요건과 금리, 한도, 일정은 사업별 공고와 기관 심사에 따라 달라집니다. '
        '세무, 법률, 감정평가 등 자격이 필요한 업무는 해당 분야 전문가와 협업하여 진행합니다.')

PAGES = [
{
 'slug':'policy-fund','no':'01','title':'정책자금 조달',
 'lead':'필요한 자금을 더 좋은 조건으로 확보할 수 있도록 조달 전략을 설계합니다.',
 'sub':'기업의 재무상태, 업력, 매출, 신용도, 자금용도를 분석하여 시설자금과 운전자금 등 적합한 정책자금 조달 방향을 검토합니다.',
 'need':['자금이 필요한데 어떤 정책자금을 받을 수 있는지 모르겠습니다.',
         '매출은 늘고 있는데 담보가 부족해 은행에서 한도가 안 나옵니다.',
         '공장이나 설비에 투자해야 하는데 목돈을 마련하기 어렵습니다.',
         '예전에 신청했다가 떨어졌는데 무엇이 문제였는지 모르겠습니다.'],
 'do':[('자금 진단','재무제표, 업력, 매출 추이, 신용 상태, 기존 대출 현황을 함께 봅니다. 지금 받을 수 있는 자금과 아직 이른 자금을 먼저 나눕니다.'),
       ('자금 용도 정리','정책자금은 시설자금과 운전자금으로 나뉘고 심사 기준과 상환 조건이 다릅니다. 무엇에 쓸 자금인지부터 명확히 정리합니다.'),
       ('조달 순서 설계','한 기관만 보지 않습니다. 중소벤처기업진흥공단, 소상공인시장진흥공단, 신용보증기금과 기술보증기금, 지역 신용보증재단 등 기업 상황에 맞는 창구와 순서를 검토합니다.'),
       ('신청 준비와 대응','사업계획서, 자금 소요 근거, 상환 계획을 정리하고 현장 실사와 심사 질의에 대비합니다.')],
 'check':[('자금 용도','시설자금은 상환 기간이 길게, 운전자금은 짧게 설계됩니다. 용도와 맞지 않으면 한도부터 줄어듭니다.'),
          ('기업 요건','업력, 업종, 고용, 보유 인증에 따라 지원 가능한 사업이 달라집니다.'),
          ('상환 능력','매출과 현금흐름으로 갚을 수 있다는 근거가 있어야 심사를 통과합니다.')],
 'faq':[('정책자금은 안 갚아도 되는 돈인가요?','아닙니다. 대부분 갚아야 하는 융자입니다. 다만 시중 대출보다 금리와 상환 조건이 유리하게 설계되어 있습니다. 갚지 않아도 되는 지원은 정부지원사업 쪽에서 따로 봅니다.'),
        ('한도와 금리는 얼마인가요?','사업별 공고와 기업 상황에 따라 다르고 해마다 바뀝니다. 특정 숫자를 미리 말씀드리기보다 대표님 회사 기준으로 가능한 범위를 함께 확인해 드립니다.'),
        ('세금이 밀려 있어도 되나요?','대부분의 정책자금은 세금 완납 여부를 확인합니다. 정리 순서부터 같이 잡는 편이 빠릅니다.'),
        ('얼마나 걸리나요?','신청 후 서류 검토, 현장 실사, 심의를 거칩니다. 기관과 시기에 따라 달라 일정은 착수 시점에 안내드립니다.')],
},
{
 'slug':'gov-program','no':'02','title':'정부지원사업',
 'lead':'기업에 적합한 무상환 지원사업을 찾고 선정 가능성을 높이는 준비를 지원합니다.',
 'sub':'기업의 사업모델과 성장단계에 맞는 정부지원사업과 R&amp;D 사업을 검토하고 사업계획서의 완성도를 높이는 방향을 제안합니다.',
 'need':['공고가 너무 많아 무엇을 봐야 할지 모르겠습니다.',
         '사업계획서를 제대로 써 본 적이 없습니다.',
         '냈다가 서면에서 떨어졌는데 이유를 모르겠습니다.',
         'R&amp;D 과제를 해보고 싶은데 무엇을 준비해야 하는지 모르겠습니다.'],
 'do':[('지원 가능 사업 선별','업종, 업력, 매출, 고용, 보유 인증을 기준으로 자격이 되는 공고부터 추립니다. 자격이 안 되는 곳에 시간을 쓰지 않는 것이 먼저입니다.'),
       ('과제 방향 정리','회사가 실제로 하려는 일과 공고가 요구하는 목적을 맞춥니다. 여기가 어긋나면 글을 아무리 잘 써도 점수가 나오지 않습니다.'),
       ('사업계획서 고도화','기술의 차별점, 시장 규모와 고객, 수행 역량을 심사자가 확인할 수 있는 형태로 정리합니다. 선행 연구나 특허, 이전 수행 실적이 있으면 근거로 붙입니다.'),
       ('평가 대응','서면 평가를 통과하면 발표 평가가 이어집니다. 예상 질의와 답변, 발표 자료를 함께 준비합니다.')],
 'check':[('기술성','기존 기술과 무엇이 다른지 숫자로 말할 수 있어야 합니다. 선행 연구와 특허 현황이 근거가 됩니다.'),
          ('사업성','시장 규모를 단계적으로 제시하고 구체적인 고객군과 도입 시나리오를 보여줄수록 유리합니다.'),
          ('수행 역량','참여 인력의 실적과 유사 과제 수행 경험이 계획을 감당할 수 있는지를 보여줍니다.')],
 'faq':[('정말 안 갚아도 되나요?','사업 유형에 따라 다릅니다. 무상 지원인 사업도 있고 일부 기술료 납부나 정산 의무가 따르는 사업도 있습니다. 공고문 기준으로 확인해 드립니다.'),
        ('기업부설연구소가 있어야 하나요?','필수는 아닙니다. 다만 R&amp;D 과제에서는 수행 역량 항목에 유리하게 작용하는 경우가 많습니다.'),
        ('매년 같은 사업이 나오나요?','큰 틀은 이어지지만 세부 요건과 예산은 해마다 바뀝니다. 그래서 지난해 자료가 아니라 그해 공고를 기준으로 봅니다.')],
},
{
 'slug':'certification','no':'03','title':'기업인증',
 'lead':'기업인증을 단순한 인증 취득이 아니라 기업 성장 전략과 연결합니다.',
 'sub':'기업부설연구소, 연구개발전담부서, 벤처기업, 이노비즈, 메인비즈 등 기업 상황에 적합한 인증을 검토하고, 인증을 정책자금과 정부지원사업, 연구개발, 세제 혜택 등 기업 성장 전략과 연결합니다.',
 'need':['인증이 여러 가지인데 우리 회사에 무엇이 맞는지 모르겠습니다.',
         '인증을 받긴 했는데 실제로 쓰는 곳이 없습니다.',
         '연구 인력이 한두 명뿐인데 연구소를 만들 수 있는지 궁금합니다.',
         '정책자금이나 지원사업에서 가점을 받고 싶습니다.'],
 'do':[('보유 자원 확인','연구 인력, 연구 공간, 매출과 업력, 기술 자료를 먼저 확인합니다. 지금 되는 인증과 준비가 더 필요한 인증을 나눕니다.'),
       ('인증 순서 설계','연구개발전담부서는 연구전담요원 1명부터 가능하고, 기업부설연구소는 기업 규모에 따라 인원 요건이 올라갑니다. 가벼운 것부터 밟아 올라가는 순서를 잡습니다.'),
       ('요건 정비','연구 공간은 고정 벽체와 별도 출입문으로 다른 부서와 구분되어야 합니다. 소기업이나 지식기반서비스 업종은 일정 면적 이하일 때 칸막이 구분도 인정됩니다. 실제 사무실 구조까지 보고 정리합니다.'),
       ('성장 전략과 연결','인증 자체가 목적이 아닙니다. 정책자금 가점, 지원사업 자격, 연구개발 세액공제, 연구소용 부동산 취득세와 재산세 감면처럼 인증이 실제로 쓰이는 자리에 붙입니다.')],
 'check':[('이노비즈','기술혁신형입니다. 연구개발 역량과 기술 경쟁력, 사업화 가능성을 봅니다. 기술 증빙 정리가 관건입니다.'),
          ('메인비즈','경영혁신형입니다. 마케팅, 조직, 생산 등 경영 전반의 혁신 역량을 봅니다. 이노비즈와 동시 보유가 가능합니다.'),
          ('벤처기업','기술평가로 기술력을 입증하는 방식입니다. 기업부설연구소가 반드시 있어야 하는 것은 아닙니다.')],
 'faq':[('연구소와 전담부서 중 무엇이 낫나요?','지방세 감면은 기업부설연구소에만 적용됩니다. 다만 인원 요건이 더 높으니 지금 인력으로 가능한 쪽부터 시작하는 편이 낫습니다.'),
        ('인증 세 개를 다 받을 수 있나요?','벤처, 이노비즈, 메인비즈는 평가 초점이 달라 동시 보유가 가능합니다. 다만 다 받는 것보다 쓸 곳이 있는 것을 먼저 받는 편이 낫습니다.'),
        ('한 번 받으면 끝인가요?','유효기간이 있어 갱신이 필요합니다. 갱신 시점을 놓치면 인증으로 받던 가점도 함께 사라집니다.')],
},
{
 'slug':'incorporation','no':'04','title':'법인전환',
 'lead':'단순한 법인설립이 아니라 기업의 미래 구조를 함께 검토합니다.',
 'sub':'개인사업자의 매출, 소득, 자산, 부채, 향후 투자계획 등을 분석하여 법인전환 시기를 검토합니다. 필요한 경우 세무사, 법무 전문가 등과 협업하여 자본금, 지분구조, 세무 리스크 등을 종합적으로 검토합니다.',
 'need':['소득세 부담이 커져서 법인이 나은지 궁금합니다.',
         '거래처에서 법인이면 좋겠다는 말을 듣습니다.',
         '사업장에 부동산이 있어 전환이 복잡할 것 같습니다.',
         '지금 받고 있는 세액감면을 잃을까 걱정됩니다.'],
 'do':[('전환 시점 판단','매출과 소득, 부채, 향후 투자 계획을 놓고 지금이 맞는 시점인지부터 봅니다. 전환이 항상 유리한 것은 아닙니다.'),
       ('전환 방식 검토','포괄양수도, 세감면 포괄양수도, 현물출자 중 무엇이 맞는지 봅니다. 부동산이 있거나 남은 세액감면을 승계해야 하면 선택지가 달라집니다.'),
       ('구조 설계','자본금 규모, 지분 구성, 대표자 급여와 배당 구조를 미리 잡습니다. 나중에 바꾸려면 비용이 훨씬 커집니다.'),
       ('전문가 협업 진행','세무 신고와 등기 실무는 세무사, 법무 전문가와 협업하여 진행합니다. 경영주치의는 전체 순서를 잡고 일정을 조율하는 역할을 맡습니다.')],
 'check':[('포괄양수도','자산과 부채, 권리와 의무를 함께 넘기는 방식입니다. 같은 대표가 개인에서 법인으로 전환할 때 주로 활용합니다.'),
          ('세감면 포괄양수도','남은 세액감면을 이어받을 때 사용합니다. 순자산 이상 자본금 납입 같은 세법에서 정한 요건을 지켜야 합니다.'),
          ('현물출자','사업용 자산을 감정평가 받아 자본금으로 넣습니다. 현금 부담은 적지만 감정과 감사, 법원 인가 절차가 따라 시간과 비용이 듭니다.')],
 'faq':[('법인으로 바꾸면 세금이 무조건 줄어드나요?','아닙니다. 소득 규모와 대표자 급여, 배당 계획에 따라 달라집니다. 숫자로 먼저 비교해 보고 정하는 것이 맞습니다.'),
        ('사업장 건물이 있어도 전환되나요?','됩니다. 다만 부동산이 있으면 취득세와 자본금 부담이 커질 수 있어 방식 선택이 특히 중요해집니다.'),
        ('기존 거래처 계약은 어떻게 되나요?','포괄적으로 승계하는 것이 일반적이지만 계약서에 따라 개별 동의가 필요한 경우가 있습니다. 전환 전에 확인해 둡니다.')],
},
{
 'slug':'export','no':'05','title':'수출 바이어 매칭',
 'lead':'수출 준비에서 끝나지 않고 실제 해외 거래 가능성을 만드는 것을 목표로 합니다.',
 'sub':'기업의 제품과 경쟁력을 분석하고 목표 국가와 시장을 설정한 후 해외 바이어 발굴과 비즈니스 매칭을 지원합니다.',
 'need':['수출을 해보고 싶은데 어디부터 손대야 할지 모르겠습니다.',
         '전시회는 나가 봤는데 실제 계약으로 이어지지 않았습니다.',
         '바이어 목록은 받았지만 연락이 닿지 않습니다.',
         '해외 인증이나 물류를 어떻게 해야 할지 모르겠습니다.'],
 'do':[('수출 준비도 점검','제품 경쟁력, 생산 여력, 가격 구조, 필요한 해외 규격 인증을 먼저 봅니다. 준비가 안 된 상태로 나가면 상담이 계약으로 이어지지 않습니다.'),
       ('목표 시장 설정','팔릴 만한 나라를 좁힙니다. 수요와 경쟁 상황, 진입 장벽, 물류 비용을 함께 봅니다.'),
       ('지원사업 연계','KOTRA 지사화사업은 현지 무역관이 지사 역할을 대행하여 바이어 발굴과 상담 주선, 계약 협상 지원까지 단계별로 돕는 사업입니다. 수출바우처는 전시회, 해외규격인증, 통번역, 국제 운송 같은 항목을 골라 쓰는 방식입니다. 회사 상황에 맞는 쪽을 검토합니다.'),
       ('상담에서 거래까지','바이어를 만난 다음이 진짜입니다. 견적과 계약 조건, 결제와 물류, 사후 대응까지 이어지도록 준비합니다.')],
 'check':[('제품 준비','해외 규격 인증과 포장, 표기, 매뉴얼이 갖춰져야 상담이 진행됩니다.'),
          ('가격 구조','운송비와 관세, 현지 유통 마진을 넣고도 경쟁력이 남는지 확인합니다.'),
          ('대응 체계','영문 응대와 납기 관리가 되지 않으면 첫 거래에서 끊깁니다.')],
 'faq':[('지사화사업과 수출바우처 중 무엇이 낫나요?','목적이 다릅니다. 지사화는 특정 시장에서 바이어를 계속 파고들 때, 바우처는 필요한 서비스를 골라 쓸 때 맞습니다. 함께 활용하기도 합니다.'),
        ('바이어를 소개받으면 바로 수출되나요?','아닙니다. 접촉은 시작이고 샘플과 조건 협의, 초도 물량으로 이어져야 거래입니다. 그 과정을 함께 봅니다.'),
        ('지원 규모와 자부담은 얼마인가요?','사업과 연도에 따라 달라집니다. 그해 공고 기준으로 확인해 드립니다.')],
},
{
 'slug':'asset','no':'06','title':'사옥·공장 매입 컨설팅',
 'lead':'기업의 현금흐름과 금융 가능성을 분석하여 무리하지 않는 자산 취득 전략을 설계합니다.',
 'sub':'기업의 재무상태와 자금조달 가능성을 분석하고 지식산업센터, 사옥, 토지, 공장 등 기업에 적합한 자산 취득 방향을 검토합니다. 입지, 금융조건, 세금과 관련된 사항은 필요한 분야의 전문가와 협업하여 진행합니다.',
 'need':['매월 나가는 임대료가 아깝습니다.',
         '공장을 넓혀야 하는데 자금이 부담됩니다.',
         '지식산업센터를 보고 있는데 우리 업종이 들어갈 수 있는지 모르겠습니다.',
         '사려면 얼마를 준비해야 하는지 감이 오지 않습니다.'],
 'do':[('감당 가능한 규모 산정','매출과 현금흐름, 기존 부채를 놓고 무리 없는 취득 규모부터 잡습니다. 물건을 먼저 보면 순서가 뒤집힙니다.'),
       ('자금 조달 경로 검토','시설자금은 공장과 사무소처럼 영업의 기초가 되는 고정시설에 투자하는 자금입니다. 정책자금 시설자금과 금융권 대출을 함께 놓고 조합을 검토합니다.'),
       ('입지와 물건 검토','업종이 입주 가능한지, 지식산업센터라면 입주 요건은 맞는지, 인허가와 용도에 문제가 없는지 확인합니다.'),
       ('취득 실행','감정평가와 등기, 세금 부분은 해당 분야 전문가와 협업하여 진행하고 경영주치의가 전체 일정을 조율합니다.')],
 'check':[('입주 자격','지식산업센터는 제조업과 지식산업, 정보통신산업 등 입주 가능 업종이 정해져 있습니다.'),
          ('자금 구조','시설자금은 운전자금보다 상환 기간이 길게 설계됩니다. 자기자금과 대출 비율을 먼저 정합니다.'),
          ('취득 이후','취득세와 재산세, 유지비까지 넣고 임대료와 비교해야 실제 이득이 보입니다.')],
 'faq':[('임대보다 매입이 항상 유리한가요?','아닙니다. 이자와 세금, 유지비를 넣고 임대료와 비교해야 합니다. 사업이 빠르게 커지는 중이라면 유연성이 더 중요할 수도 있습니다.'),
        ('정책자금으로 부동산을 살 수 있나요?','사업에 직접 쓰는 시설이라면 시설자금 범위에서 검토할 수 있습니다. 투자 목적 취득은 대상이 아닙니다.'),
        ('자기자금은 얼마나 필요한가요?','물건과 담보 평가, 기업 신용에 따라 달라집니다. 회사 기준으로 계산해 드립니다.')],
},
]

HEAD = '''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | 경영주치의</title>
<meta name="description" content="{lead}">
<meta name="robots" content="noindex, nofollow">
<meta property="og:type" content="article">
<meta property="og:title" content="{title} | 경영주치의">
<meta property="og:description" content="{lead}">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="../assets/css/style.css">
{ga}
</head>
<body class="is-sub">

<a class="skip" href="#main">본문 바로가기</a>

<header class="header" id="header">
  <div class="container header__inner">
    <!-- TODO:LOGO 로고 파일 받으면 이미지로 교체 -->
    <a class="logo" href="../index.html"><img class="logo__mark" src="../assets/img/logo.svg" alt="" aria-hidden="true" width="32" height="32"><span>비즈밸류 기업성장연구소</span></a>
    <nav class="nav" id="nav">
      <a href="../index.html" class="nav__link">HOME</a>
      <a href="../index.html#worries" class="nav__link">기업 대표의 고민</a>
      <a href="../index.html#approach" class="nav__link">접근 방식</a>
      <a href="../index.html#services" class="nav__link is-active">솔루션</a>
      <a href="../index.html#consultant" class="nav__link">컨설턴트 소개</a>
      <a href="../index.html#process" class="nav__link">프로세스</a>
      <a href="../index.html#cases" class="nav__link">컨설팅 사례</a>
    </nav>
    <button class="burger" id="burger" aria-label="메뉴 열기" aria-expanded="false" aria-controls="nav">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>

<main id="main">
'''

FOOT = '''</main>

<footer class="footer">
  <div class="container footer__inner">
    <div class="footer__cols">
      <div class="footer__brand">
        <p class="footer__logo"><img src="../assets/img/logo.svg" alt="" aria-hidden="true" width="30" height="30"><span>비즈밸류 기업성장연구소</span></p>
        <!-- TODO:BIZ 상호 · 대표자 · 사업자등록번호 · 주소 · 연락처 -->
        <p class="footer__biz">상호 · 대표자 · 사업자등록번호 · 주소 · 연락처 (확정 후 기재)</p>
      </div>

      <nav class="footer__nav" aria-label="컨설팅 분야">
        <p class="footer__navtitle">컨설팅 분야</p>
        <ul>
          <li><a href="policy-fund.html">정책자금 조달</a></li>
          <li><a href="gov-program.html">정부지원사업</a></li>
          <li><a href="certification.html">기업인증</a></li>
          <li><a href="incorporation.html">법인전환</a></li>
          <li><a href="export.html">수출 바이어 매칭</a></li>
          <li><a href="asset.html">사옥·공장 매입</a></li>
        </ul>
      </nav>
    </div>

    <div class="footer__bottom">
      <p class="footer__copy">&copy; 비즈밸류. All rights reserved.</p>
      <a class="footer__policy" href="../privacy.html">개인정보 처리방침</a>
    </div>
  </div>
</footer>

<div class="bottombar" id="bottombar">
  <!-- TODO:TEL -->
  <a class="bottombar__btn bottombar__btn--tel" href="#" data-pending="전화번호 준비중">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.2.4 2.4.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1C10.6 21 3 13.4 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1l-2.3 2.2z"/></svg>
    전화 상담
  </a>
  <a class="bottombar__btn bottombar__btn--apply" href="../index.html#apply">기업 현황 1차 진단 신청</a>
</div>

<div class="float" id="float">
  <!-- TODO:KAKAO -->
  <a class="float__btn float__btn--kakao" href="#" data-pending="카카오톡 채널 준비중" aria-label="카카오톡 상담">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3C6.5 3 2 6.5 2 10.8c0 2.8 1.9 5.2 4.7 6.6-.2.7-.7 2.7-.8 3.1-.1.6.2.6.5.4.2-.1 2.7-1.8 3.8-2.5.6.1 1.2.1 1.8.1 5.5 0 10-3.5 10-7.7S17.5 3 12 3z"/></svg>
    <span class="float__tip">카카오톡 상담</span>
  </a>
  <!-- TODO:INSTA -->
  <a class="float__btn float__btn--insta" href="#" data-pending="인스타그램 준비중" aria-label="인스타그램">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C8.74 0 8.333.015 7.053.072 5.775.132 4.905.333 4.14.63c-.789.306-1.459.717-2.126 1.384S.935 3.35.63 4.14C.333 4.905.131 5.775.072 7.053.012 8.333 0 8.74 0 12s.015 3.667.072 4.947c.06 1.277.261 2.148.558 2.913.306.788.717 1.459 1.384 2.126.667.666 1.336 1.079 2.126 1.384.766.296 1.636.499 2.913.558C8.333 23.988 8.74 24 12 24s3.667-.015 4.947-.072c1.277-.06 2.148-.262 2.913-.558.788-.306 1.459-.718 2.126-1.384.666-.667 1.079-1.335 1.384-2.126.296-.765.499-1.636.558-2.913.06-1.28.072-1.687.072-4.947s-.015-3.667-.072-4.947c-.06-1.277-.262-2.149-.558-2.913-.306-.789-.718-1.459-1.384-2.126C21.319 1.347 20.651.935 19.86.63c-.765-.297-1.636-.499-2.913-.558C15.667.012 15.26 0 12 0zm0 2.16c3.203 0 3.585.016 4.85.071 1.17.055 1.805.249 2.227.415.562.217.96.477 1.382.896.419.42.679.819.896 1.381.164.422.36 1.057.413 2.227.057 1.266.07 1.646.07 4.85s-.015 3.585-.074 4.85c-.061 1.17-.256 1.805-.421 2.227-.224.562-.479.96-.899 1.382-.419.419-.824.679-1.38.896-.42.164-1.065.36-2.235.413-1.274.057-1.649.07-4.859.07-3.211 0-3.586-.015-4.859-.074-1.171-.061-1.816-.256-2.236-.421-.569-.224-.96-.479-1.379-.899-.421-.419-.69-.824-.9-1.38-.165-.42-.359-1.065-.42-2.235-.045-1.26-.061-1.649-.061-4.844 0-3.196.016-3.586.061-4.861.061-1.17.255-1.814.42-2.234.21-.57.479-.96.9-1.381.419-.419.81-.689 1.379-.898.42-.166 1.051-.361 2.221-.421 1.275-.045 1.65-.06 4.859-.06l.045.03zm0 3.678a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 1 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm7.846-10.405a1.441 1.441 0 0 1-2.88 0 1.44 1.44 0 0 1 2.88 0z"/></svg>
    <span class="float__tip">인스타그램</span>
  </a>
  <a class="float__btn float__btn--apply" href="../index.html#apply" aria-label="1차 진단 신청">
    <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h11l4 4v14a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1zm2 7h10v2H7v-2zm0 4h10v2H7v-2zm0 4h6v2H7v-2z"/></svg>
    <span class="float__tip">1차 진단 신청</span>
  </a>
</div>

<script src="../assets/js/main.js"></script>
</body>
</html>
'''


def build(p, others):
    h = [HEAD.format(title=p['title'], lead=p['lead'], ga=GA)]

    h.append('<section class="subhero subhero--photo">\n')
    h.append('  <div class="subhero__bg" aria-hidden="true"><picture>'
             '<source srcset="../assets/img/%s.webp" type="image/webp">'
             '<img src="../assets/img/%s.jpg" alt="" width="920" height="518"></picture></div>\n'
             % (PHOTO[p['slug']], PHOTO[p['slug']]))
    h.append('  <div class="container">\n')
    h.append('    <p class="crumb"><a href="../index.html">HOME</a> <span aria-hidden="true">&rsaquo;</span> '
             '<a href="../index.html#services">6대 핵심 서비스</a> <span aria-hidden="true">&rsaquo;</span> %s</p>\n' % p['title'])
    h.append('    <div class="subhero__icon" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></div>\n' % ICONS[p['slug']])
    h.append('    <p class="subhero__no">SERVICE %s</p>\n' % p['no'])
    h.append('    <h1 class="subhero__title">%s</h1>\n' % p['title'])
    h.append('    <p class="subhero__lead">%s</p>\n' % p['lead'])
    h.append('    <p class="subhero__lead">%s</p>\n' % p['sub'])
    h.append('  </div>\n</section>\n\n')

    h.append('<section class="sec sec--light">\n  <div class="container">\n')
    h.append('    <h2 class="h2 h2--dark h2--left reveal">이런 기업에 필요합니다.</h2>\n')
    h.append('    <ul class="need reveal">\n')
    for n in p['need']:
        h.append('      <li>%s</li>\n' % n)
    h.append('    </ul>\n  </div>\n</section>\n\n')

    h.append('<section class="sec sec--navy">\n  <div class="container">\n')
    h.append('    <h2 class="h2 h2--left reveal">무엇을 하는가</h2>\n')
    h.append('    <div class="dolist">\n')
    for i, (t, d) in enumerate(p['do'], 1):
        h.append('      <div class="do reveal">\n')
        h.append('        <p class="do__title"><b>%02d</b>%s</p>\n' % (i, t))
        h.append('        <p class="do__txt">%s</p>\n' % d)
        h.append('      </div>\n')
    h.append('    </div>\n  </div>\n</section>\n\n')

    h.append('<section class="sec sec--light">\n  <div class="container">\n')
    h.append('    <h2 class="h2 h2--dark h2--left reveal">무엇을 기준으로 판단하는가</h2>\n')
    h.append('    <div class="checks">\n')
    for t, d in p['check']:
        h.append('      <div class="check reveal">\n        <p class="check__title">%s</p>\n        <p class="check__txt">%s</p>\n      </div>\n' % (t, d))
    h.append('    </div>\n  </div>\n</section>\n\n')

    h.append('<section class="sec sec--navy2">\n  <div class="container">\n')
    h.append('    <h2 class="h2 h2--left reveal">자주 묻는 질문</h2>\n')
    h.append('    <div class="faq reveal">\n')
    for q, a in p['faq']:
        h.append('      <details>\n        <summary>%s</summary>\n        <p>%s</p>\n      </details>\n' % (q, a))
    h.append('    </div>\n  </div>\n</section>\n\n')

    h.append('<section class="sec sec--ink">\n  <div class="container endcta">\n')
    h.append('    <h2 class="h2 h2--center reveal">%s, 우리 회사도 될까요?</h2>\n' % p['title'])
    h.append('    <p class="body body--center reveal">기업 현황을 남겨주시면 내용을 확인한 후 1차 상담을 통해 '
             '현재 가장 먼저 검토해야 할 과제를 함께 살펴보겠습니다.</p>\n')
    h.append(form(prefix='../', preset=PRESET[p['slug']], form_id='applyForm'))
    h.append('    <div class="siblings reveal">\n')
    for o in others:
        h.append('      <a href="%s.html">%s</a>\n' % (o['slug'], o['title']))
    h.append('    </div>\n')
    h.append('    <p class="note">%s</p>\n' % NOTE)
    h.append('  </div>\n</section>\n\n')

    h.append(FOOT)
    return ''.join(h)


if not os.path.isdir(OUT):
    os.makedirs(OUT)

for p in PAGES:
    others = [o for o in PAGES if o['slug'] != p['slug']]
    io.open(os.path.join(OUT, p['slug'] + '.html'), 'w', encoding='utf-8', newline='').write(build(p, others))

print('generated', len(PAGES), 'pages ->', OUT)
