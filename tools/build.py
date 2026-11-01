"""폴 컴포넌트 코리아 사이트 빌드.

index.src.html(한국어 원본)에서
  1) 호환 표(브레이크, 레버)를 채워 index.html(한국어)을 만들고
  2) i18n/en.json, i18n/ja.json 번역으로 en/index.html, ja/index.html을 만들고
  3) sitemap.xml을 다시 씁니다.

사용법: python3 tools/build.py
문구를 고친 뒤에는 python3 i18n/extract.py 로 ko.json을 갱신하고,
새로 생긴 문장을 i18n/tr_source.py에 (한국어, 영어, 일본어)로 추가하고
python3 i18n/tr_source.py 로 en.json / ja.json을 만든 다음 빌드합니다.
"""
import json, re, sys, pathlib, datetime
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'i18n'))
from extract import HANGUL  # noqa: E402

SITE = 'https://paul.rubiworkshop.com/'

# ---------------------------------------------------------------- fit tables
# 폴 컴포넌트 공식 기술 정보(paulcomp.com, 2026-11 기준). 무게는 휠 하나 또는 레버 기준.
BRAKES = [
  # 모델, 종류, 마운트, 케이블 풀, 폴 레버, 다른 레버, 무게, 비고
  ('Klamper · Short Pull', '기계식 디스크', '포스트 · 플랫 마운트', '숏 풀', 'Canti Lever, Cross Lever, Reverse Lever', '시마노 · 스램 로드 레버, 브레이크 시프터', '211g', '로터 · 어댑터 별매'),
  ('Klamper · Long Pull', '기계식 디스크', '포스트 · 플랫 마운트', '롱 풀', 'Love Lever, Cross Lever, Reverse Lever', '케인크릭 드롭 V 등 롱 풀 레버', '211g', '로터 · 어댑터 별매'),
  ('Klamper · Campagnolo', '기계식 디스크', '포스트 · 플랫 마운트', '캄파놀로', '-', '캄파놀로 에르고파워', '211g', '캄파놀로 전용 암'),
  ('Neo-Retro', '캔틸레버', '캔티 보스', '숏 풀', 'Canti Lever, Cross Lever', '숏 풀 드롭바 레버', '100g', '넓은 폭, 넉넉한 진흙 틈새'),
  ('Touring Cantilever', '캔틸레버', '캔티 보스', '숏 풀', 'Canti Lever, Cross Lever', '숏 풀 드롭바 레버', '123g', '좁은 폭, 패니어 간섭 적음'),
  ('Racer', '센터풀', '브레이즈온 · 센터 마운트', '숏 풀', 'Canti Lever, Cross Lever', '숏 풀 드롭바 레버', '120g / 157g', '리치 57 ~ 72mm'),
  ('Racer Medium', '센터풀', '브레이즈온 · 센터 마운트', '숏 풀', 'Canti Lever, Cross Lever', '숏 풀 드롭바 레버', '113g / 154g', '리치 47 ~ 57mm, 타이어 32mm'),
  ('MiniMoto', '숏 풀 V 브레이크', '캔티 보스', '숏 풀', 'Canti Lever, Cross Lever', '시마노 · 스램 숏 풀 레버 (캄파놀로 제외)', '149g', '타이어 약 44mm'),
  ('Motolite', '리니어 풀 V 브레이크', '캔티 보스', '롱 풀', 'Love Lever, Cross Lever', 'V 브레이크용 플랫바 레버', '137g', '26인치 프레임에 650B · 700C 휠'),
]
LEVERS = [
  # 모델, 케이블 풀, 클램프, 무게, 형태, 맞는 브레이크
  ('Canti Lever', '숏 풀', '22.2mm', '134g (한 쌍)', '플랫바, 스탠다드 · 쇼트 리치', '캔틸레버, 센터풀, 사이드풀, 미니모토, 숏 풀 클램퍼'),
  ('Love Lever Compact', '롱 풀', '22.2mm', '125g', '두 손가락', '모토라이트, V 브레이크, 롱 풀 클램퍼'),
  ('Love Lever 2.5', '롱 풀', '22.2mm', '137g', '세 손가락', '모토라이트, V 브레이크, 롱 풀 클램퍼'),
  ('Duplex Lever', '숏 · 롱 풀', '22.2mm', '94g', '레버 하나로 케이블 두 개', '앞뒤 브레이크를 한 손으로'),
  ('Cross Lever', '숏 · 롱 풀 (피벗 선택)', '31.8mm', '140g', '드롭바 상단 보조 레버', '드롭바 레버와 함께 또는 단독'),
  ('Reverse Lever', '숏 · 롱 풀 (피벗 선택)', '바 안지름 19 ~ 25mm', '80g', '핸들 끝, 좌우 공용', '불혼 바 등 핸들 끝 제동'),
  ('E-Lever', '숏 풀', '22.2 / 23.8mm', '56g', '한 손가락', '보조 브레이크 (고정 기어, 코스터 브레이크와 함께)'),
]

def table(head, rows, left=()):
    h = '<table class="size fit"><thead><tr>' + ''.join(f'<th>{c}</th>' for c in head) + '</tr></thead><tbody>'
    for r in rows:
        h += f'<tr><th>{r[0]}</th>' + ''.join(f'<td class="l">{v}</td>' if i + 1 in left else f'<td>{v}</td>' for i, v in enumerate(r[1:])) + '</tr>'
    return h + '</tbody></table>'

def brake_table():
    return table(['모델', '종류', '마운트', '케이블 풀', '폴 레버', '다른 레버', '무게', '비고'], BRAKES, left=(4, 5, 7))

def lever_table():
    return table(['모델', '케이블 풀', '클램프', '무게', '형태', '맞는 브레이크'], LEVERS, left=(4, 5))

def build_ko():
    s = (ROOT / 'index.src.html').read_text()
    s = s.replace('{{BRAKE_TABLE}}', brake_table()).replace('{{LEVER_TABLE}}', lever_table())
    assert '{{' not in s
    assert '\u2014' not in re.sub(r'<!--.*?-->', '', s, flags=re.S), 'em dash in Korean page'
    (ROOT / 'index.html').write_text(s)
    return s

# ---------------------------------------------------------------- translate
LANG = {
 'en': {'locale': 'en_US', 'path': 'en/'},
 'ja': {'locale': 'ja_JP', 'path': 'ja/'},
}

def translate(ko_html, lang):
    tr = json.loads((ROOT / f'i18n/{lang}.json').read_text())
    missing = set()
    def t(s):
        k = s.strip()
        if not HANGUL.search(k):
            return s
        if k in tr:
            return s.replace(k, tr[k])
        missing.add(k)
        return s

    soup = BeautifulSoup(ko_html, 'html.parser')
    soup.html['lang'] = lang
    if soup.title:
        soup.title.string = t(soup.title.string)
    for m in soup.find_all('meta'):
        if m.has_attr('content'):
            m['content'] = t(m['content'])
    for sc in soup.find_all('script', type='application/ld+json'):
        data = json.loads(sc.string)
        def walk(o):
            if isinstance(o, dict):
                return {k: walk(v) for k, v in o.items()}
            if isinstance(o, list):
                return [walk(v) for v in o]
            if isinstance(o, str):
                return t(o)
            return o
        data = walk(data)
        for node in data.get('@graph', []):
            if node.get('@type') == 'WebSite':
                node['url'] = SITE + LANG[lang]['path']
                node['inLanguage'] = lang
        sc.string = '\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    for el in soup.body.find_all(True):
        for a in ('alt', 'aria-label', 'title'):
            if el.has_attr(a):
                el[a] = t(el[a])

    def visit(el):
        if el.name in ('script', 'style'):
            return
        direct = any(isinstance(c, NavigableString) and not isinstance(c, Comment) and HANGUL.search(c) for c in el.children)
        if direct:
            k = el.decode_contents().strip()
            if k in tr:
                el.clear()
                frag = BeautifulSoup(tr[k], 'html.parser')
                for c in list(frag.contents):
                    el.append(c)
            else:
                missing.add(k)
            return
        for c in list(el.children):
            if getattr(c, 'name', None):
                visit(c)
    visit(soup.body)

    # canonical, og, hreflang self, language switcher
    soup.find('link', rel='canonical')['href'] = SITE + LANG[lang]['path']
    soup.find('meta', property='og:url')['content'] = SITE + LANG[lang]['path']
    soup.find('meta', property='og:locale')['content'] = LANG[lang]['locale']
    for a in soup.select('nav.lang a'):
        code = a['hreflang']
        a['href'] = '../' if code == 'ko' else ('./' if code == lang else f'../{code}/')
        if code == lang:
            a['class'] = ['on']; a['aria-current'] = 'page'
        else:
            a.attrs.pop('class', None); a.attrs.pop('aria-current', None)
    if lang == 'ja':
        # 일본어는 한글 서체(에스코어 드림) 대신 Noto Sans JP로 통일 (영문·숫자는 Pretendard 유지)
        style = soup.find('style')
        for tag in BeautifulSoup('<link rel="preconnect" href="https://fonts.googleapis.com">'
                                 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
                                 '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400&display=swap" rel="stylesheet">'
                                 '<style>:root{--font:"RubiLatin","Noto Sans JP","Hiragino Sans","Yu Gothic",system-ui,sans-serif}</style>',
                                 'html.parser').contents[:]:
            style.insert_after(tag) if tag.name == 'style' else style.insert_before(tag)

    out = str(soup)
    # 하위 폴더에서 이미지 경로 보정
    out = out.replace('src="images/', 'src="../images/').replace('url(images/', 'url(../images/').replace('href="images/', 'href="../images/')
    left = [k for k in missing]
    return out, left

def sitemap(html):
    imgs = sorted(set(re.findall(r'images/[\w/.-]+\.(?:jpg|png|webp)', html)))
    imgs = [i for i in imgs if not re.search(r'logo|favicon|apple-touch', i)]
    today = datetime.date.today().isoformat()
    alts = ''.join(f'\n    <xhtml:link rel="alternate" hreflang="{h}" href="{SITE}{p}"/>' for h, p in [('ko', ''), ('en', 'en/'), ('ja', 'ja/'), ('x-default', '')])
    urls = []
    for p in ['', 'en/', 'ja/']:
        u = f'  <url>\n    <loc>{SITE}{p}</loc>{alts}\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>{"1.0" if not p else "0.8"}</priority>'
        if not p:
            u += ''.join(f'\n    <image:image><image:loc>{SITE}{i}</image:loc></image:image>' for i in imgs)
        urls.append(u + '\n  </url>')
    x = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
         'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
         + '\n'.join(urls) + '\n</urlset>\n')
    (ROOT / 'sitemap.xml').write_text(x)

if __name__ == '__main__':
    ko = build_ko()
    print('ko  index.html', len(ko))
    for lang in LANG:
        if not (ROOT / f'i18n/{lang}.json').exists():
            print(lang, 'skipped (no translation file)'); continue
        out, left = translate(ko, lang)
        d = ROOT / LANG[lang]['path']; d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(out)
        hangul = len(HANGUL.findall(re.sub(r'<script(?![^>]*ld\+json).*?</script>', '', out, flags=re.S)))
        print(lang, f'{d.name}/index.html', len(out), 'untranslated units:', len(left), 'hangul chars left:', hangul)
        for k in left[:20]:
            print('   -', k[:90])
    sitemap(ko)
