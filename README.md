# Paul Component Korea

paul.rubiworkshop.com 원페이지 정적 사이트. thm.rubiworkshop.com과 같은 구조와 디자인(레이아웃, 서체, 빌드 방식)입니다.

- `index.html` 한국어 원페이지 (Paul · Range · Klamper · Brakes · Levers · Cockpit · Hubs · Fit · Story · Showroom)
- 디자인은 THM · QUOC 사이트와 같은 rubi.kr 체계: 영문 Pretendard · 한글 에스코어 드림, 웨이트 400, 흑백과 얇은 라인, 각진 버튼, 라이트/다크 자동. 일본어 페이지는 빌드 시 Noto Sans JP로 바뀝니다.
- THM과 다른 점
  - 폴 공식 제품 사진은 흰 배경 정사각형 컷이라 제품 사진은 1:1 흰 바탕에 잘리지 않게(contain) 놓고, 라이프스타일 사진은 3:2로 맞췄습니다.
  - 히어로의 제품 슬라이드는 `light` 클래스로 흰 무대가 되고, 글자와 컨트롤 색이 함께 바뀝니다. 첫 슬라이드만 어두운 사진입니다.
  - 포인트 컬러는 폴 퍼플(#6b4ea2)로 포커스 표시에만 씁니다. 브랜드 섹션에 아노다이징 컬러 칩이 있습니다.
  - 호환 표는 브레이크 · 레버 케이블 풀 표 두 개입니다 (`tools/build.py` 안의 BRAKES, LEVERS).
  - 자바스크립트가 꺼져 있어도 본문이 보이도록 등장 모션은 `html.js`일 때만 적용합니다.
- `en/index.html`, `ja/index.html` 영어 · 일본어 페이지 (빌드로 생성, 직접 수정하지 않음)
- `index.src.html` 편집용 한국어 원본. 호환 표는 `{{BRAKE_TABLE}}`, `{{LEVER_TABLE}}` 자리에 빌드 시 채워집니다.
- `i18n/` 번역 (`tr_source.py`에 한국어 · 영어 · 일본어를 한 줄씩 묶어 둠, `en.json` · `ja.json`은 여기서 생성, `ko.json`은 원문 목록)
- `tools/build.py` 한국어 페이지, 번역 페이지, sitemap.xml을 한 번에 생성
- `404.html` 하위 주소(/klamper, /racer, /love-lever, /boxcar, /word, /fit, /dealers 등)를 섹션으로 연결
- `.github/image-manifest.txt` + `fetch-images.yml` 폴 공식 사이트(paulcomp.com) 이미지 이전용 워크플로

## 처음 올릴 때
1. 저장소 `sereno-kwon/paul`을 만들고 이 폴더를 main에 푸시합니다.
2. 푸시하면 `fetch-images.yml`이 매니페스트의 이미지 47개를 paulcomp.com에서 받아 `images/`에 커밋합니다. Actions → Fetch images from Paul에서 FAIL이 있으면 해당 줄의 URL을 바꿔 다시 푸시합니다.
3. 배포: Cloudflare Pages(저장소 연결, 빌드 명령 없음, 출력 폴더 `/`) 또는 GitHub Pages(Settings → Pages → main / root).
4. 도메인 DNS에 `paul` CNAME 레코드를 추가합니다 (Cloudflare Pages는 `<프로젝트>.pages.dev`, GitHub Pages는 `sereno-kwon.github.io`). CNAME 파일은 이미 들어 있습니다.
5. 파비콘은 별도로 넣어야 합니다: `images/favicon-48.png`, `images/favicon-96.png`, `images/apple-touch-icon.png`(180px), `images/logo-512.png`.
6. 로고(`images/logo.svg`)는 paulcomp.com의 SVG 로고를 받아 옵니다. CSS에서 헤더는 검정, 다크모드는 흰색으로 칠해집니다.

## 이미지
- 제품 컷은 paulcomp.com 공식 이미지입니다. 라다비스트(The Radavist) 사진은 저작권 때문에 쓰지 않았고, 기사는 Story 섹션에서 링크로만 소개합니다.
- 라이프스타일 사진이 부족합니다. `images/hero/01.jpg`(선반 배너), `images/brand/01~03.jpg`는 루비에서 직접 찍은 사진(rubi- 파일명)으로 같은 경로에 덮어쓰는 것을 권합니다. brand/02, 03은 1024px 크기라 큰 화면에서는 조금 부드럽게 보입니다.
- 매니페스트를 고쳐 main에 푸시하면 Actions가 다시 받습니다. 이미 받은 파일은 건너뛰므로, 교체할 때는 파일을 지우거나 새 파일명으로 추가합니다.

## 문구 수정과 번역
1. `index.src.html`의 한국어 문구를 고칩니다.
2. `python3 tools/build.py` → `python3 i18n/extract.py` 로 `ko.json`을 갱신합니다.
3. 바뀐 문장을 `i18n/tr_source.py`에서 같은 한국어 키로 고치거나 (한국어, 영어, 일본어)로 추가하고 `python3 i18n/tr_source.py`.
4. 다시 `python3 tools/build.py`. 번역되지 않은 문장이 있으면 목록으로 알려줍니다.

빌드에는 `beautifulsoup4`가 필요합니다 (`pip install beautifulsoup4`).

## 링크
- 헤더 Shop, "루비워크샵에서 보기" 버튼: `https://rubiworkshop.com/paul`
- 거래처 문의: 루비서플라이 02-516-8465, 카카오톡 채널 `https://pf.kakao.com/_NFnBj/chat`
- 푸터 Instagram: `https://www.instagram.com/rubi.workshop`
- 쇼룸 운영시간: 월~금 12:00~19:00, 토 10:00~15:30

## 한글 표기
폴 컴포넌트(Paul Component Engineering), 폴 프라이스(Paul Price), 치코(Chico), 클램퍼(Klamper), 네오레트로(Neo-Retro), 투어링 캔틸레버(Touring Cantilever), 레이서(Racer), 레이서 미디엄(Racer Medium), 미니모토(MiniMoto), 모토라이트(Motolite), 캔티 레버(Canti Lever), 러브 레버(Love Lever), 듀플렉스 레버(Duplex Lever), 크로스 레버(Cross Lever), 리버스 레버(Reverse Lever), 이레버(E-Lever), 박스카(Boxcar), 톨 앤 핸섬(Tall and Handsome), 톨 앤 엘레강트(Tall and Elegant), 워드(Word), 에프허브(FHub), 썸비(Thumbies), 멜빈(Melvin), 마운틴 고트(Mountain Goat), 제프 린지(Jeff Lindsay), 비드웰 파크(Bidwell Park), 마팍(Mafac), 쿨스톱(Kool Stop)

## 출처
- 수치: paulcomp.com 제품별 Technical Info (2026-11 확인)
- 브랜드 스토리: The Radavist 「An Afternoon with Paul Component in Chico」(2015), 「The Eleven Bikes of the 2017 Paul Camp Builder Fleet」(2017), 「John's 1984 Mountain Goat Whiskeytown Racer」(2022), 「Paul's Kearney & Trecker Collection」(2024), 「The Cascade Cougar」(2026), paulcomp.com Story
