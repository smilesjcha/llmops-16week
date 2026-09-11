# Week 02 강의안 제작·수정

## 기준

[공통 PPT 제작 가이드](../../week01/lecture/PPT_PRODUCTION_GUIDELINE.md)와 [Week 01 디자인 시스템](../../week01/lecture/DESIGN_SYSTEM.md)을 따른다.

- 72장: 60장 수업 진행 + 12장 선택 심화
- 16:9, 1280×720 작업 좌표
- 흑백·네이비·파랑만 사용, 현재 주차와 실험 근거에 한정한 강조
- 명사형 제목, 풀어 쓴 약어, 설명 없는 구호 금지
- 실제 PowerPoint 텍스트 크기 최소 14pt, 본문 18pt 이상, 코드16pt 이상
- AppleGothic / Menlo, 대체 폰트 사용 시 반드시 다시 렌더 검수
- 표·흐름은 편집 가능한 PowerPoint 객체, 실습 이미지는 실제 실행 화면
- 개인정보 없는 합성 데이터와 Demo 화면만 강의안에 포함
- 모든 장에 진행 노트와 출처 블록

`slide_content.json`이 내용의 단일 원본이다. `build_deck.mjs`는 편집 가능한 PowerPoint를 생성한다. 학생은 이 제작 환경을 설치할 필요가 없다. 실습의 Python 의존성과 PPT 제작 도구는 분리되어 있다.

캡처는 `assets/`의 실제 JPEG 원본이며, 표시 영역은 `assets/captures.json`에 기록한다. 이미지 자체를 변조하지 않고 PowerPoint의 사진 자르기 기능으로 필요한 영역을 확대한다. 현재 제작 런타임이 지정 영역을 중앙 자르기로 바꾸는 문제는 `repair_picture_crops.py`에서 사진 6개의 원본 영역·위치만 복원한 후 최종 구조 검증을 수행한다. 재생성 시 PDF에서 캡처 영역을 반드시 재확인한다.

## 제작 환경

JavaScript Artifact Tool이 제공되는 제작 환경에서 실행한다. 다음 환경 변수를 해당 환경의 설치 경로로 지정한다.

- `PRESENTATIONS_SKILL_DIR`: Presentations 스킬 디렉터리
- `ARTIFACT_PYTHON`: PPTX 검증용 Python 실행 파일
- `RUNTIME_NODE_MODULES`: 제작 환경의 Node.js 패키지 디렉터리(최종 재열기 검사에 사용)
- `DECK_REVISION`: 새 검수 리비전 이름(예: v2). 기존 최종 파일을 덮어쓰지 않는 새 이름 사용

`@oai/artifact-tool`이 Node.js 모듈 경로에서 해석되어야 한다. `node_modules`와 중간 `build/`는 Git에서 제외한다.

```bash
node week02/lecture/build_deck.mjs
```

제작 환경의 Presentation finalizer로 72장·파일 구조·글꼴·편집 가능한 표·화면 경계를 확인한 뒤 `build/<revision>/final/`에 최종 후보가 생성된다. 오류가 있으면 원본 JSON 또는 빌더를 수정하고 새 리비전으로 다시 제작한다.

## 배포 전 검수

1. 실제 실습 실행과 화면 캡처 갱신
2. 제목·본문·노트와 실습 UI/API 일치 확인
3. PPTX 구조 검증과 모든 슬라이드 렌더
4. 한 장씩 전수 검수: 글자 잘림, 어절 중간 개행, 겹침, 표 높이, 선·면과 간격
5. PPTX를 PDF로 변환하고 동일한 72장인지 확인
6. 최종 PPTX/PDF의 SHA-256과 검수 결과 기록
7. 검증된 PPTX는 이 폴더, 학생용 PDF는 `output/pdf/`에 반영

PDF는 PowerPoint와 같은 페이지 순서의 인쇄용이다. 저장된 노트북 출력·실험 결과에 실사용자 개인정보나 로컬 절대경로가 없는지도 함께 확인한다.

검증된 PPTX의 PDF 출력 예시(LibreOffice가 설치된 제작 환경):

```bash
soffice --headless --convert-to pdf --outdir week02/lecture/build/<revision>/final \
  week02/lecture/build/<revision>/final/02_week2_prompt_design_versioning.pptx
```

`<revision>`은 실제 리비전 이름으로 바꾼다. 배포 PDF의 줄바꿈·자르기는 해당 변환 결과를 기준으로 검수한다. 다른 컴퓨터의 PowerPoint에서 폰트가 바뀌면 PDF를 사용하거나 해당 환경에서 다시 확인한다.
