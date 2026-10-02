# 2026년 2학기 프로젝트 HTML 문서

## 문서

- `course-roadmap.html`: 16주 일정, 현재 주차, 실시간 온라인 수업과 예외 운영, 프로젝트 구간
- `project-proposal-2pager.html`: 화면과 인쇄에서 사용하는 2페이지 제안서
- `project-prd.html`: 제품 요구사항 문서(Product Requirements Document, PRD) 기획서
- `project-submission.html`: 팀 신청·제출 경로·평가 기준·도구·체크리스트
- `examples/`: 글쓰기 코치의 2Pager와 PRD 예시

모든 페이지는 검정·흰색·네이비·파랑만 사용한다. 새 페이지는 CSS와 JavaScript를 파일 안에 포함하므로 HTML 하나를 내려받아 바로 공유·실행할 수 있다. 로드맵은 기본적으로 4주차를 강조하며 주소의 `week` 값으로 현재 주차를 바꿀 수 있다.

```text
course-roadmap.html?week=1
course-roadmap.html?week=4
course-roadmap.html?week=16
```

## 로컬 확인

저장소 루트에서 다음 명령을 실행한다.

```bash
python -m http.server 4173 --directory curriculum/2026-2/web
```

브라우저에서 <http://127.0.0.1:4173/course-roadmap.html>을 연다. HTML을 직접 열어도 동작한다. 양식은 화면에서 편집한 뒤 작성본 HTML 저장 또는 인쇄 → PDF로 보관한다. GitHub 파일 화면은 웹페이지를 실행하지 않으므로 Download raw file로 내려받아 브라우저에서 연다. 내용이 긴 2Pager는 인쇄 미리보기에서 분량을 줄여 두 페이지로 맞춘다.

## 운영 기준

- 대면 수업 없이 정규 주차를 실시간 온라인 강의로 운영한다.
- 9월 25일 추석에는 녹화영상을 업로드했다. 10월 9일 한글날에는 실시간 수업·녹화영상·신규 과제가 없다.
- 7주차 10월 16일 강의를 재개하고 팀 또는 개인 기획서 초안 0.1을 제출받아 피드백한다.
- 별도의 중간고사 없이 8주차에는 실시간 수업도 진행하지 않으며, 피드백 반영 수정본 0.2를 온라인 제출·평가한다.
- 제출 형식은 PPT·Word·PDF·HTML 중 자유롭게 선택하지만 한글(HWP) 파일은 제외한다.
- 16주차 기말 프로젝트 발표는 실시간 온라인으로 진행한다.
- 4주차 영상 위치·시청 기한, 제출 범위와 시각은 소속별 공지를 따른다. 아주대AI대학원은 LMS, 다른 학교는 공지된 이메일을 사용한다.
