# 2026년 2학기 프로젝트 HTML 문서

## 문서

- `course-roadmap.html`: 16주 일정, 현재 주차, 온라인 영상 대체 주차, 프로젝트 구간
- `project-proposal-2pager.html`: 화면과 인쇄에서 사용하는 2페이지 제안서
- `project-prd.html`: 제품 요구사항 문서(Product Requirements Document, PRD) 기획서

모든 페이지는 검정·흰색·네이비·파랑만 사용하고, 한글 어절의 임의 분리를 막는 공통 스타일을 사용한다. 과정 로드맵은 기본적으로 1주차를 강조하며 주소의 `week` 값으로 현재 주차를 바꿀 수 있다.

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

브라우저에서 <http://127.0.0.1:4173/course-roadmap.html>을 연다. `project-proposal-2pager.html`은 브라우저의 인쇄 기능에서 A4 두 페이지로 저장할 수 있다.

## 운영 기준

- 별도의 중간고사 없이 8주차에 기말 프로젝트 기획서 0.1을 제출한다.
- 9월 25일 추석과 10월 9일 한글날 주차는 휴강이 아니라 온라인 강의 영상으로 진행한다.
- 영상 위치, 시청 기한, 제출 범위와 시각은 학습관리시스템(Learning Management System, LMS) 공지를 따른다.
