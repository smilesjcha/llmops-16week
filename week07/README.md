# Week 07 · 모델 적응과 서비스 기획

2026년 10월 16일 온라인 실시간 수업. 6주차 휴일에 진행하지 않은 기술 내용을 연결하고, 기말 프로젝트 기획서 초안 0.1을 검토한다. 수정본 0.2 제출 마감은 **10월 22일(목) 23:59 한국시간**이다. 8주차 10월 23일은 시험·실시간 강의 없이 제출물로 평가한다.

- [학생용 PDF · 77쪽](../output/pdf/07_week7_model_adaptation_project.pdf)
- [발표용 PowerPoint · 77장](lecture/07_week7_model_adaptation_project.pptx)
- [6주차 SFT·LoRA·QLoRA 확장 강의안 · 76장](../week06/README.md)
- [6–7주차 통합 강의 영상 · Drive](resources/README.md)
- [장표별 내용·출처](lecture/lecture-notes.md)
- [교수용 100분 진행안](lecture/TEACHING_GUIDE.md)
- [4개 Notebook 실습·VS Code 가이드](lab/README.md)
- [초안 제출 안내 · 독립 HTML](assignment/project-draft.html)
- [8주차 제출 안내와 기존 양식](../week08/README.md)

## 학습 범위

1. 프롬프트·검색·모델 학습의 개선 대상과 선택 근거
2. SFT(Supervised Fine-Tuning, 지도 미세조정)의 데이터·분할·손실 마스킹
3. LoRA(Low-Rank Adaptation, 저차원 행렬 기반 모델 적응)의 구조와 비용
4. DPO(Direct Preference Optimization, 직접 선호 최적화)의 선호쌍·reference·손실
5. 고정 평가 입력, 실패·복구 계획과 기획서 초안

기본 실습은 Python 3.11과 기존 `requirements.txt`로 실행한다. 실제 LLM 학습, 모델 다운로드, 유료 API는 필수가 아니다. 행렬 근사와 장난감 정책 학습은 실제 LLM 학습 성공이나 업무 품질 향상의 증거가 아니다.

## 제출과 개인정보

7주차의 제출 준비는 **기획서 초안**이다. 6주차 신규 과제는 없으며, 별도 미세조정 결과를 필수 과제로 추가하지 않는다. 아주대AI대학원은 2–4인 자율 팀을 원칙으로 LMS에 제출하며 개인 예외는 교수 승인 여부를 확인한다. 군산대·국립창원대 등 타교 수강생은 개인 진행이 가능하고 공지된 교수 이메일을 이용한다. 소속별 평가 적용 여부·정확한 시각은 담당 공지가 우선한다.

팀 신청 폼은 기획서 제출함이 아니다. 학생 명단·연락처·설문 응답·메일 내용·학생 제출물은 제한 공유 관리 문서에서만 관리하고 공개 GitHub에 넣지 않는다.
