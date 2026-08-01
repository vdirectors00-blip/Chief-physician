# -*- coding: utf-8 -*-
"""
사이트에 실제로 쓰인 글자만 남긴 Pretendard 서브셋을 만든다.

  실행:  python tools/make_font_subset.py
  결과:  assets/fonts/PretendardVariable.subset.woff2

화면 문구를 추가하거나 바꾼 뒤에는 반드시 다시 돌려야 한다.
돌리지 않으면 새로 넣은 글자만 시스템 기본 글꼴로 나온다.

필요 패키지: pip install fonttools brotli
"""
import re
import pathlib
import subprocess
import sys
import urllib.request

SITE = pathlib.Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "fonts" / "PretendardVariable.subset.woff2"
SRC = SITE / "tools" / "_PretendardVariable.woff2"          # 원본 (커밋하지 않음)
SRC_URL = (
    "https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9"
    "/packages/pretendard/dist/web/variable/woff2/PretendardVariable.woff2"
)

LATIN = set(chr(c) for c in range(0x20, 0x7F))
PUNCT = set("·—–…“”‘’「」『』〈〉《》㈜①②③④⑤⑥⑦⑧⑨⑩※→←↑↓©®™₩%‰°㎡㎏㎞")


def collect_chars() -> set:
    chars = set()
    for f in list(SITE.glob("*.html")) + list(SITE.glob("services/*.html")):
        s = f.read_text(encoding="utf-8")
        s = re.sub(r"<script.*?</script>", " ", s, flags=re.S)
        s = re.sub(r"<style.*?</style>", " ", s, flags=re.S)
        s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
        attrs = re.findall(
            r'(?:placeholder|alt|title|aria-label|value|content|data-pending)="([^"]*)"', s
        )
        text = re.sub(r"<[^>]+>", " ", s)
        for t in [text] + attrs:
            chars |= set(t)
    chars |= LATIN | PUNCT | set(" 0123456789")
    return {c for c in chars if c.isprintable()}


def main() -> None:
    if not SRC.exists():
        print("원본 폰트를 내려받습니다...")
        urllib.request.urlretrieve(SRC_URL, SRC)

    chars = collect_chars()
    txt = SITE / "tools" / "_chars.txt"
    txt.write_text("".join(sorted(chars)), encoding="utf-8")
    print(f"사이트에서 쓰는 글자 {len(chars)}자")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "-m", "fontTools.subset", str(SRC),
        f"--text-file={txt}",
        "--flavor=woff2",
        "--layout-features=kern,liga,calt,ccmp,locl,mark,mkmk",
        "--name-IDs=*",
        f"--output-file={OUT}",
    ]
    subprocess.run(cmd, check=True)
    print(f"완료: {OUT.relative_to(SITE)}  ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
