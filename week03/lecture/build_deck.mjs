/** Week 03 editable lecture deck. Run through BUILD.md with the bundled runtime. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';
import {Presentation, PresentationFile} from '@oai/artifact-tool';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '../..');
const SKILL = process.env.PRESENTATIONS_SKILL_DIR;
const PYTHON = process.env.ARTIFACT_PYTHON;
if (!SKILL || !PYTHON) throw new Error('Set PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON.');
const revision = process.env.DECK_REVISION || 'v1';
const BUILD = path.join(HERE, 'build', revision);
await fs.mkdir(BUILD, {recursive: true});

const C = {black:'#050505', ink:'#191919', white:'#FFFFFF', paper:'#F7F8FA', navy:'#0B1F3A', blue:'#2563EB', soft:'#E0F0FE', gray:'#667085', line:'#D0D5DD', darkLine:'#314156', muted:'#AFB8C7'};
const FONT = 'AppleGothic', MONO = 'Menlo';
const p = Presentation.create({slideSize:{width:1280,height:720}});
p.theme.colorScheme = {name:'BLACK WHITE NAVY BLUE', themeColors:{accent1:C.blue,accent2:C.navy,accent3:C.gray,accent4:C.soft,accent5:C.ink,accent6:C.line,bg1:C.white,bg2:C.black,tx1:C.ink,tx2:C.white,dk1:C.black,dk2:C.navy,lt1:C.white,lt2:C.paper,hlink:C.blue,folHlink:C.navy}};

const source = ['repo:week03/lab/README.md', 'repo:week03/lab/data/cases.json', 'repo:curriculum/2026-2/00_운영_커리큘럼.md'];
const s = (n, section, title, layout, body = [], extra = {}) => ({n, section, title, layout, body, notes: extra.notes || `${title}의 핵심은 평가 결과를 수치 하나가 아니라 사례·기준·오류·다음 확인으로 읽는 것이다. 수강생에게 현재 사례에서 확인 가능한 것과 확인하지 못한 것을 분리해 말하도록 질문한다.`, sources: extra.sources || source, ...extra});
const slides = [
  s(1,'시작','프롬프트 평가와 오류 분류','cover',['WEEK 03 · 2026.09.18','합성 회의록 평가 작업대 EVAL/03','차성재 · 무신사 Core AI PM × AI 대학원 겸임교수'],{notes:'0:00–0:30. 오늘은 프롬프트를 고르는 기술보다, 고르기 전에 무엇을 확인할지 정하는 시간을 다룬다. 평가 결과가 좋아도 어떤 사례·기준인지 말할 수 없으면 다음 사람이 재현하거나 반박할 수 없다는 점으로 시작한다.'}),
  s(2,'시작','오늘의 완료 증거','steps',[],{steps:[['평가 기준','결과를 보기 전에 구조·사실·근거·실행 항목을 정의'],['개발·확인 분리','개선에 쓴 사례와 최종 확인 사례를 구분'],['결정 기록','후보·보류·제외와 다음 확인을 한 문장으로 남김']]}),
  s(3,'시작','16주 로드맵 · 현재 위치','roadmap',['W03 · 평가 기준과 오류 분류','전 과정 온라인 · 현재 주차만 파랑 표시'],{notes:'0:01:30–0:02:30. 전 과정은 온라인이다. 4주차와 6주차는 휴강이 아니라 실시간 강의 대신 녹화영상 업로드로 대체한다. 8주차에는 중간고사·실시간 수업 없이 기획서 온라인 제출·평가, 16주차에는 실시간 온라인 프로젝트 발표를 진행한다.'}),
  s(4,'시작','지난 주와 오늘의 연결','compare',[],{columns:[['2주차 · 비교','같은 입력과 조건에서 프롬프트 버전을 비교','변경한 규칙과 결과를 함께 기록'],['3주차 · 판정','무엇이 통과·실패인지 기준을 고정','오류 유형과 다음 확인을 함께 기록']]}),
  s(5,'시작','100분 수업 구성','timeline',[],{steps:[['00:00–00:10','질문·로드맵·완료 증거'],['00:10–00:32','평가 기준과 오류 분류'],['00:32–00:43','실습 구조와 사례 읽기'],['00:43–00:48','휴식·환경 준비'],['00:48–01:19','EVAL/03 실행과 기록'],['01:19–01:40','결과 해석·다음 확인']]}),
  s(6,'시작','평가의 출발점','statement',['“좋은 답변”이라는 말만으로는 결과를 다시 확인할 수 없다.','무엇을 보았는지, 어떤 사례에서 어긋났는지, 다음에 무엇을 확인할지를 남긴다.']),
  s(7,'시작','오늘의 실습 산출물','flow',[],{flow:['평가 실행','실패 상세','후보 판단','JSON 보관'],caption:'프롬프트 v0.1·v0.2 · 합성 회의 발췌 · 고정 응답 · 실제 모델 성능 측정 아님'}),
  s(8,'평가 기준','평가 기준과 오류 분류','section',['점수보다 먼저 판정 범위','사례보다 먼저 기대 기준','개선보다 먼저 실패 설명'],{notes:'0:10–0:11. 이 구간에서는 결과를 보기 전에 기준을 고정한다. 기준은 절대적인 정답이 아니라 이번 업무·사례·버전에 대한 합의라는 점을 분명히 한다.'}),
  s(9,'평가 기준','평가 대상의 구체화','statement',['평가 대상은 “모델” 하나가 아니라 입력·프롬프트·모델 설정·출력 검사로 이루어진 실행 단위다.','한 요소를 바꾸면 결과 차이의 원인을 분리해 기록한다.']),
  s(10,'평가 기준','결과와 판정의 분리','compare',[],{columns:[['결과','회의록 문장과 섹션','모델 또는 고정 응답이 만든 산출물'],['판정','통과·실패와 이유','사전에 정한 루브릭이 만든 해석']]}),
  s(11,'평가 기준','하나의 출력 · 네 가지 확인','checks',[],{checks:[['구조','필수 섹션 4개'],['핵심 사실','앵커 문구 누락'],['근거','원문 밖 단정'],['실행 항목','담당·기한·미정']]}),
  s(12,'평가 기준','평가 계약','table',[],{rows:[['항목','이번 실습의 결정'],['입력','합성 회의 발췌 6건'],['출력','결정·실행·위험·다음 단계 회의록'],['기준','구조·핵심 사실·근거·실행 항목'],['기록','프롬프트 원문·해시·결과·결정 이유']]}),
  s(13,'평가 기준','루브릭과 측정값','compare',[],{columns:[['루브릭','무엇을 통과로 볼지','사람이 읽을 수 있는 판단 문장'],['측정값','몇 건이 통과했는지','루브릭을 집계한 숫자']]}),
  s(14,'평가 기준','근거 없는 단정','case',['원문: “이번 달 예산은 아직 검토 중이다.”','출력: “예산 승인 완료 후 데이터 정제를 진행한다.”','판정: 구조가 맞아도 원문에 없는 확정 정보를 추가했으므로 근거 검사 실패']),
  s(15,'평가 기준','사실 앵커의 역할','flow',[],{flow:['원문 핵심','앵커 정의','출력 확인','누락 기록'],caption:'앵커는 완전한 의미 이해가 아니라, 이번 사례에서 반드시 남아야 하는 사실의 최소 확인점'}),
  s(16,'평가 기준','오류 분류의 언어','matrix',[],{matrix:[['오류 유형','질문','예시'],['누락','필요한 사실이 빠졌나','담당자·기한 없음'],['왜곡','원문 뜻이 달라졌나','검토 중 → 승인 완료'],['형식','약속한 구조가 있나','필수 섹션 없음'],['범위 밖','검사하지 않은 문제인가','문체·설득력']]}),
  s(17,'평가 기준','누락과 왜곡의 차이','compare',[],{columns:[['누락','말해야 할 사실을 말하지 않음','다음 확인에서 원문과 출력 대조'],['왜곡','원문에 없는 사실을 더함','근거·정책·책임 판단에 더 큰 위험']]}),
  s(18,'평가 기준','오류 위치','flow',[],{flow:['입력 사실','프롬프트 지시','생성 결과','평가 규칙','결정 기록'],caption:'같은 실패라도 원인은 데이터·지시·생성·검사·해석 중 다른 위치에 있을 수 있다'}),
  s(19,'평가 기준','개발 사례와 확인 사례','compare',[],{columns:[['개발 사례 · dev','규칙·프롬프트를 다듬는 데 사용','이번 실습 4건'],['확인 사례 · test','선택 후에 별도로 확인','이번 실습 2건']]}),
  s(20,'평가 기준','확인 사례 오염','statement',['확인 사례를 보며 프롬프트를 계속 고치면, 그 사례는 더 이상 독립적인 확인 근거가 아니다.','수정 전후의 데이터 묶음과 선택 시점을 함께 기록한다.']),
  s(21,'평가 기준','적은 사례의 해석','case',['2/4와 2/2는 각각 다른 질문에 대한 결과다.','dev 2/4: 개선에 쓴 작은 사례에서 네 기준을 모두 통과한 수','test 2/2: 선택 뒤 별도 사례에서 확인한 수','둘 다 일반 성능·운영 준비 완료를 보장하지 않는다.']),
  s(22,'평가 기준','결정 이전의 질문','steps',[],{steps:[['기준의 적합성','이 업무에서 이 네 검사가 충분한가'],['사례의 대표성','빠진 상황과 위험이 무엇인가'],['오류의 설명','실패를 다시 만들고 원인을 말할 수 있는가']]}),
  s(23,'실습 준비','EVAL/03 평가 작업대','section',['합성 회의 발췌 · 고정 응답','외부 모델·API 키 없이 재현','평가 규칙과 결정 기록 중심'],{notes:'0:32–0:33. 지금부터는 코드·화면을 실행한다. 이 실습은 실제 회의록을 쓰지 않고, 교육용 합성 문장과 고정 응답을 사용한다.'}),
  s(24,'실습 준비','실습 서비스 구성','flow',[],{flow:['합성 사례','고정 응답','루브릭 검사','브라우저 보고서'],caption:'EVAL/03은 FastAPI 기반의 로컬 수업 도구 · 주소 http://127.0.0.1:8003'}),
  s(25,'실습 준비','합성 회의 발췌','case',['M02 · 기한 미정','“검색 결과의 출처 표시는 필요하다. 담당자와 완료일은 정하지 못했다.”','실제 회의·학생 개인정보·외부 전송 없음']),
  s(26,'실습 준비','프롬프트 두 버전','compare',[],{columns:[['v0.1 · 짧은 요약','핵심 논의와 다음 작업을 한 문단으로 정리','필수 섹션 요구 없음'],['v0.2 · 구조화 회의록','결정·실행·위험·다음 단계 분리','원문 밖 사실 금지와 미정 표기 요구']]}),
  s(27,'실습 준비','네 가지 검사 규칙','checks',[],{checks:[['구조','4개 섹션'],['핵심 사실','필수 앵커'],['근거','금지 단정 없음'],['실행 항목','담당·기한·미정']]}),
  s(28,'실습 준비','사례 묶음','table',[],{rows:[['구분','사례','수업에서 쓰는 이유'],['dev','M01–M04 · 4건','구조·미정·근거·복합 위험을 읽고 개선'],['test','M05–M06 · 2건','선택 후 새 표현과 보류 결정을 확인']]}),
  s(29,'실습 준비','실행 보고서 구조','flow',[],{flow:['입력 세트 해시','프롬프트 스냅샷','검사 결과','판단 근거'],caption:'같은 실행을 찾기 위한 식별 정보 · 민감 원문을 익명화하는 기능은 아님'}),
  s(30,'실습 준비','브라우저 화면 읽기','statement',['STEP 01 평가 실행 → STEP 02 프롬프트·기준 → STEP 03 결과·오류 → STEP 04 후보 결정','수업 중에는 한 결과 행을 열어 원문·출력·실패 이유를 함께 읽는다.']),
  s(31,'실습 준비','실습 전 점검','code',['.venv/bin/python -m uvicorn eval03.main:app \\','  --app-dir week03/lab --host 127.0.0.1 --port 8003'],{caption:'VS Code → Terminal → Run Task → Week 03: Run EVAL/03 · 브라우저 http://127.0.0.1:8003'}),
  s(32,'휴식','환경 준비','section',['5분 · 서버 시작 · 브라우저 열기','수업 필수는 Demo · Ollama·API 키 없음','막히면 화면을 보며 기준과 실패 유형부터 기록'],{notes:'0:43–0:48. 휴식과 환경 준비. 실행이 늦은 수강생은 데모 화면에서 사례·기준·오류 기록을 먼저 완료한다. 로컬 환경 복구는 VS_CODE_GUIDE.md의 순서를 따른다.'}),
  s(33,'실습','STEP 01 · 서버 시작','code',['.venv/bin/python -m uvicorn eval03.main:app \\','  --app-dir week03/lab --host 127.0.0.1 --port 8003'],{caption:'예상 신호 · Uvicorn running on http://127.0.0.1:8003 · 종료는 서버 터미널에서 Ctrl+C'}),
  s(34,'실습','STEP 02 · 평가 실행','steps',[],{steps:[['사례 묶음 선택','dev · 개선에 쓰는 개발 사례 4건'],['두 버전 평가','v0.1과 v0.2를 같은 사례에서 실행'],['결과 행 확인','통과율보다 실패한 기준을 먼저 열기']]}),
  s(35,'실습','v0.1 · 구조 실패','case',['v0.1 출력: 한 문단 요약','루브릭: 결정 사항 · 실행 항목 · 위험·확인 필요 · 다음 단계','판정: 내용이 자연스러워도 섹션 계약을 지키지 않아 structure_ok = false']),
  s(36,'실습','M02 · 실행 항목 실패','case',['출력의 실행 항목: “디자인 작업은 담당자와 완료일을 정한 뒤 시작한다.”','원문: 담당자와 완료일은 정하지 못했다.','판정: 전체 사실은 남아도 실행 항목 안에 담당·기한·미정이 없어 action_ok = false']),
  s(37,'실습','M03 · 근거 실패','worksheet',['원문: 이번 달 예산은 아직 검토 중','출력: 예산 승인 완료 후 데이터 정제를 진행','판정: 금지 단정 “예산 승인 완료”가 있어 evidence_ok = false']),
  s(38,'실습','실패 상세의 읽는 순서','flow',[],{flow:['원문','출력','검사 값','오류 문장'],caption:'“실패했다”에서 멈추지 않고, 어느 기준이 어떤 근거로 실패했는지 읽는다'}),
  s(39,'실습','개발 사례 결과','table',[],{rows:[['버전','전체 통과','대표 실패'],['v0.1','0 / 4','필수 섹션 없음'],['v0.2','2 / 4','M02 실행 항목 · M03 근거']]}),
  s(40,'실습','통과율의 한계','statement',['v0.2의 2/4는 “이 고정 응답과 4개 개발 사례에서 네 조건을 모두 통과한 수”다.','실제 LLM 성능, 실제 사용자 만족, 다른 업무의 품질을 뜻하지 않는다.']),
  s(41,'실습','오류 기록 문장','worksheet',['사례: M03 / 버전: v0.2','기준: 근거 없는 단정 금지','관찰: “예산 승인 완료”가 원문에 없음','다음 확인: 승인·확정 표현의 부정문과 우회 표현 추가']),
  s(42,'실습','프롬프트 원문 확인','code',['# week03/lab/prompts/meeting_minutes_v0.2.md','- 결정 사항, 실행 항목, 위험·확인 필요, 다음 단계를 분리','- 원문에 없는 사실을 추가하지 않음','- 담당자·완료일이 없으면 “미정”으로 남김'],{caption:'Demo 응답은 고정이므로 프롬프트 파일을 수정해도 화면의 결과는 바뀌지 않는다'}),
  s(43,'실습','STEP 03 · 확인 사례 실행','steps',[],{steps:[['사례 묶음 변경','test · 최종 확인 사례 2건'],['같은 기준 실행','선택 뒤 새로운 사례에서 확인'],['해석 분리','2/2는 작은 확인 결과이지 일반 성능이 아님']]}),
  s(44,'실습','개발과 확인의 비교','compare',[],{columns:[['dev · 4건','개선에 사용','v0.2 전체 통과 2/4'],['test · 2건','선택 뒤 확인','v0.2 전체 통과 2/2']]}),
  s(45,'실습','후보 결정 기록','table',[],{rows:[['필드','기록 예시'],['후보 버전','v0.2 · 구조화 회의록'],['판단','보류'],['근거와 다음 확인','M02 미정 표기와 M03 단정 오류를 수정 기준으로 추가 사례 평가']]}),
  s(46,'실습','JSON 보고서 보관','flow',[],{flow:['실행 정보','결과 행','결정 기록','JSON 내보내기'],caption:'서버 메모리 기록은 재시작하면 초기화 · 수업 종료 전에 저장'}),
  s(47,'실습','자동 테스트','code',['PYTHONPATH=week03/lab .venv/bin/python -m eval03.smoke','PYTHONPATH=week03/lab .venv/bin/python -m pytest week03/lab/tests -q','.venv/bin/python -m ruff check week03'],{caption:'검증 범위 · 상태 확인, 4×2 개발 결과, 오류 규칙, 결정 기록, JSON 내보내기'}),
  s(48,'실습','실습 중 질의응답','worksheet',['어떤 기준이 실제 프로젝트에 가장 먼저 필요한가','현재 기준으로 놓치는 오류는 무엇인가','새 확인 사례를 어떤 업무 상황에서 만들 것인가','이 결과를 후보·보류·제외 중 무엇으로 기록할 것인가']),
  s(49,'결과 해석','결과 해석과 버전 결정','section',['작은 평가 세트의 결과를 과장하지 않기','통과율·실패 유형·남은 위험을 함께 읽기','기획서의 선택 근거로 누적하기'],{notes:'1:19–1:20. 실습 결과를 해석한다. 수치가 높다는 이유만으로 자동 채택하지 않고, 사례 수·오류 위험·검사 범위를 함께 이야기한다.'}),
  s(50,'결과 해석','결과 요약','matrix',[],{matrix:[['구분','v0.1','v0.2'],['dev 전체 통과','0 / 4','2 / 4'],['test 전체 통과','0 / 2','2 / 2'],['해석','필수 구조 불충족','구조 개선 · 근거·미정 오류 남음']]}),
  s(51,'결과 해석','오류와 대응','table',[],{rows:[['오류','현재 관찰','다음 대응'],['구조','v0.1에 필수 섹션 없음','출력 구조 요구와 검사 유지'],['실행 항목','M02에 미정 정보가 없음','미정 표기 사례 추가'],['근거','M03에 승인 완료 단정','확정 표현과 원문 근거 대조 확대']]}),
  s(52,'결과 해석','합계 점수만으로 부족한 이유','statement',['동일한 2/4라도 실패가 문체인지, 근거 없는 약속인지에 따라 다음 행동이 다르다.','업무 위험이 큰 오류는 같은 한 건이어도 별도 기준·사람 검토가 필요하다.']),
  s(53,'결과 해석','결정 상태','flow',[],{flow:['후보','보류','제외'],caption:'후보: 다음 확인 가능 · 보류: 근거 부족 또는 위험 남음 · 제외: 현재 기준에서 사용하지 않음'}),
  s(54,'결과 해석','보류 결정의 근거','case',['현재 기록: v0.2를 보류','이유: dev에서 M02 실행 항목, M03 근거 오류 확인','다음 확인: 미정·확정 표현의 변형 사례와 사람 검토 결과를 추가','범위: 교육용 고정 응답 · 실제 배포 없음']),
  s(55,'결과 해석','다음 확인 설계','steps',[],{steps:[['새 사례','미정·부정문·조건부 약속을 포함'],['같은 루브릭','바뀌지 않은 기준과 새 기준을 구분'],['사람 검토','자동 규칙이 놓친 의미·업무 위험 확인']]}),
  s(56,'결과 해석','프로젝트 기획서 연결','flow',[],{flow:['문제 정의','수용 기준','평가 사례','결정 근거'],caption:'8주차 온라인 기획서 제출·평가를 위해, 자신의 서비스에 필요한 평가 기준과 대표 실패를 누적'}),
  s(57,'결과 해석','오늘의 기록 양식','worksheet',['서비스에서 만들고 싶은 결과','결과가 맞다고 볼 최소 기준','대표 성공 사례 1건과 실패 사례 1건','후보·보류·제외 중 현재 판단과 다음 확인']),
  s(58,'결과 해석','다음 주 연결','statement',['다음 주에는 검색 증강 생성(Retrieval-Augmented Generation, RAG)의 근거와 인용을 다룬다.','검색 결과도 “찾았다”가 아니라 어떤 문서·근거를 답변에 사용했는지 평가 대상으로 만든다.']),
  s(59,'마무리','오늘의 핵심','steps',[],{steps:[['기준','결과보다 먼저 고정'],['사례','개발과 확인을 분리'],['오류','누락·왜곡·형식·범위를 구분'],['기록','결정과 다음 확인을 남김']]}),
  s(60,'마무리','수업 종료 확인','statement',['실습 화면에서 JSON을 저장했는가','대표 실패 1건을 기준·관찰·다음 확인으로 설명할 수 있는가','2주차 과제 01의 마감과 4주차 격주 과제를 분리해 확인했는가']),
  s(61,'참고','평가 필드 사전','table',[],{rows:[['필드','뜻'],['structure_ok','네 필수 섹션 존재'],['coverage_ok','사례별 핵심 앵커 누락 없음'],['evidence_ok','금지 단정 미포함'],['action_ok','실행 항목에 담당·기한 또는 미정'],['overall_ok','네 필드 모두 true']]}),
  s(62,'참고','형식 검사와 의미 검사','compare',[],{columns:[['형식 검사','제목·섹션·자료형처럼 비교적 명확한 계약','자동화하기 쉬우나 충분 조건은 아님'],['의미 검사','원문과의 일치·업무 위험·문맥','사람 검토·표본·추가 규칙이 필요']]}),
  s(63,'참고','자동 규칙의 오탐과 누락','matrix',[],{matrix:[['상태','의미','대응'],['오탐','문제 없는데 실패로 표시','규칙·사례·사람 검토 확인'],['누락','문제 있는데 통과로 표시','새 실패 사례와 보완 기준 추가'],['미평가','검사 범위 밖','통과로 해석하지 않음']]}),
  s(64,'참고','사람 검토의 역할','statement',['사람 검토는 자동 평가를 무효화하는 과정이 아니라, 자동 규칙이 다루지 못한 맥락·정책·위험을 보완하는 과정이다.','검토 결과도 사례·판단자·근거·불일치를 기록해야 비교 가능하다.']),
  s(65,'참고','루브릭 작성 예시','table',[],{rows:[['항목','나쁜 기준','확인 가능한 기준'],['근거','사실에 맞음','원문에 없는 확정·승인 표현 없음'],['실행','일이 명확함','실행 항목에 담당자·기한 또는 미정'],['구조','읽기 좋음','네 섹션을 제목으로 구분']]}),
  s(66,'참고','데이터 보호 기준','steps',[],{steps:[['합성 데이터 우선','실제 회의·고객·학생 자료를 실습에 넣지 않음'],['식별 정보 제외','이름·연락처·토큰·내부 문서 제거'],['해시의 한계','동일성 확인용 식별자이며 익명화가 아님']]}),
  s(67,'참고','코드 읽기 지도','flow',[],{flow:['cases.json','demo_outputs\n.json','core.py','experiments\n.py','main.py'],caption:'데이터 → 고정 결과 → 루브릭 → 실행 보고서 → 화면·API'}),
  s(68,'참고','실습 명령 모음','code',['# 서버',' .venv/bin/python -m uvicorn eval03.main:app --app-dir week03/lab --port 8003','','# 검증',' PYTHONPATH=week03/lab .venv/bin/python -m eval03.smoke'],{caption:'macOS/Linux 기준 · Windows는 week03/VS_CODE_GUIDE.md의 PowerShell 안내 사용'}),
  s(69,'참고','API 경로','table',[],{rows:[['메서드','경로','용도'],['GET','/health','서비스 상태'],['GET','/api/catalog','프롬프트·루브릭 목록'],['POST','/api/evaluations','dev 또는 test 평가 실행'],['POST','/api/decisions','후보·보류·제외 기록'],['GET','/api/evaluations/{run_id}/export','JSON 보고서 내보내기']]}),
  s(70,'참고','자료와 검증 범위','worksheet',['cases.json · 합성 사례·기대 앵커·금지 단정','demo_outputs.json · 수업용 고정 응답','tests · 규칙·API 테스트 10개','VS_CODE_GUIDE.md · 환경·실행·오류 복구']),
  s(71,'참고','용어 정리','table',[],{rows:[['용어','수업에서의 뜻'],['평가 세트','출력과 기준을 비교하는 사례 묶음'],['루브릭','통과·실패를 정하는 판단 기준'],['개발 사례','개선에 사용할 수 있는 사례'],['확인 사례','선택 뒤 별도로 확인할 사례'],['Retrieval-Augmented Generation, RAG','검색 문서를 근거로 답하는 생성 방식']]}),
  s(72,'참고','수업 자료 위치','statement',['PPT · week03/lecture/\n03_week3_prompt_evaluation_error_analysis.pptx','학생용 PDF · output/pdf/\n03_week3_prompt_evaluation_error_analysis.pdf','실습 안내 · week03/README.md · 실행 가이드 · week03/VS_CODE_GUIDE.md'])
];

if (slides.length !== 72) throw new Error(`Expected 72 slides, got ${slides.length}`);
const boxes = [], minSizes = [], layouts = [];
let current = 0;
const plain = value => String(value ?? '').replace(/\*\*/g, '').replace(/`/g, '');
const advance = (value, px, mono = false) => [...value].reduce((sum, char) => sum + (/[^\x00-\x7F]/.test(char) ? px : (mono ? px * .61 : /[MW@]/.test(char) ? px * .83 : /[il .,:'!|]/.test(char) ? px * .28 : px * .55)), 0);
function wrap(value, width, pt, mono = false) {
  return plain(value).split('\n').flatMap(line => {
    if (advance(line, pt * 4 / 3, mono) <= width) return [line];
    const words = line.split(/\s+/); const lines = []; let carry = '';
    for (const word of words) { const next = carry ? `${carry} ${word}` : word; if (carry && advance(next, pt * 4 / 3, mono) > width) { lines.push(carry); carry = word; } else carry = next; }
    if (carry) lines.push(carry); return lines;
  }).join('\n');
}
function rect(slide, left, top, width, height, fill, line = 'none', lineWidth = 0) { return slide.shapes.add({geometry:'rect', position:{left,top,width,height}, fill, line:{fill:line,width:lineWidth,style:'solid'}}); }
function rule(slide, left, top, width, color = C.line, height = 1) { return rect(slide,left,top,width,height,color); }
function txt(slide, value, left, top, width, height, pt = 20, opts = {}) {
  if (pt < 14) throw new Error(`Below 14pt on slide ${current}`);
  const text = opts.noWrap ? plain(value) : wrap(value,width,pt,opts.mono);
  const lines = text.split('\n'); const estimated = lines.length * pt * 4 / 3 * (opts.leading ?? 1.18);
  if (estimated > height + 4) throw new Error(`Text overflow ${current}: ${text}`);
  if (lines.some(line => advance(line,pt * 4 / 3,opts.mono) > width + 6)) throw new Error(`Text width overflow ${current}: ${text}`);
  const box = rect(slide,left,top,width,height,'none'); box.text = text;
  box.text.style = {fontSize:pt*4/3,typeface:opts.mono ? MONO : FONT,bold:opts.bold ?? false,color:opts.color ?? C.ink,alignment:opts.align ?? 'left',verticalAlignment:'top',lineSpacing:opts.leading ?? 1.18,autoFit:'none',wrap:'none',insets:{top:0,right:0,bottom:0,left:0}};
  boxes.push({slide:current,left,top,width,height,text,pt}); minSizes.push(pt); return box;
}
function height(value, width, pt = 20) { return wrap(value,width,pt).split('\n').length * pt * 4 / 3 * 1.18 + 4; }
function shell(slide, spec, dark = false) {
  const fg = dark ? C.white : C.ink, muted = dark ? C.muted : C.gray; slide.background.fill = dark ? C.black : C.paper;
  txt(slide,`W03 / ${spec.section}`,64,28,900,24,14,{color:muted}); txt(slide,String(current).padStart(2,'0'),1140,28,76,24,14,{mono:true,color:muted,align:'right'});
  txt(slide,spec.title,64,76,1152,68,38,{bold:true,color:fg}); rule(slide,64,666,1152,dark ? C.darkLine : C.line);
  txt(slide,'LLMOPS · 통합 강좌 · 프롬프트 평가와 오류 분류',64,680,1152,22,14,{color:muted}); return {fg,muted,dark};
}
function list(slide, items, left, top, width, pt = 20, opts = {}) { let y = top; for (const item of items) { const h = height(item,width,pt); txt(slide,item,left,y,width,h,pt,opts); y += h + (opts.gap ?? 18); } return y; }
function cover(slide, spec) { slide.background.fill=C.black; txt(slide,'W03 / INTEGRATED LLMOPS COURSE',64,42,1100,24,14,{color:C.muted}); txt(slide,'프롬프트 평가',64,150,1152,100,58,{bold:true,color:C.white}); txt(slide,'오류 분류',64,252,1152,100,58,{bold:true,color:C.white}); rule(slide,64,398,1152,C.darkLine); txt(slide,'평가 기준 · 개발·확인 사례 · 결정 기록',64,438,1152,42,24,{color:C.white}); list(slide,spec.body,64,520,1152,18,{color:C.muted,gap:8}); }
function section(slide,spec) { slide.background.fill=spec.n%2 ? C.navy : C.black; txt(slide,`W03 / ${spec.section}`,64,40,1000,24,14,{color:C.muted}); txt(slide,String(current).padStart(2,'0'),1140,40,76,24,14,{mono:true,color:C.muted,align:'right'}); txt(slide,spec.title,64,190,1152,70,46,{bold:true,color:C.white}); rule(slide,64,392,1152,C.darkLine); list(slide,spec.body,64,450,1100,22,{color:C.white,gap:16}); }
function statement(slide,spec) { const a=shell(slide,spec,current%4===0); const first=spec.body[0] || ''; const h=height(first,1120,30); txt(slide,first,64,205,1120,h,30,{bold:true,color:a.fg}); rule(slide,64,205+h+56,1152,a.dark?C.darkLine:C.line); list(slide,spec.body.slice(1),64,205+h+88,1100,20,{color:a.muted,gap:20}); }
function steps(slide,spec) { const a=shell(slide,spec); const steps=spec.steps || []; let y=185; for (let i=0;i<steps.length;i++) { const [name,detail]=steps[i]; const h=Math.max(height(name,290,23),height(detail,700,19)); txt(slide,String(i+1).padStart(2,'0'),64,y+3,60,32,18,{mono:true,color:C.gray}); txt(slide,name,152,y,310,h,23,{bold:true,color:a.fg}); txt(slide,detail,520,y,696,h,19,{color:a.muted}); rule(slide,152,y+h+19,1064,a.dark?C.darkLine:C.line); y+=h+40; } }
function flow(slide,spec) { const a=shell(slide,spec); const nodes=spec.flow || []; const count=nodes.length, gap=26, width=(1152-gap*(count-1))/count, y=300; const shapes=[]; nodes.forEach((node,i)=>{const x=64+i*(width+gap); const box=rect(slide,x,y,width,106,i===1?C.soft:C.white,i===1?C.blue:C.line,1); txt(slide,String(i+1).padStart(2,'0'),x+18,y+16,width-36,22,14,{mono:true,color:i===1?C.blue:C.gray}); const nodeHeight=height(node,width-36,20); txt(slide,node,x+18,y+50,width-36,nodeHeight,20,{bold:true,color:C.ink}); shapes.push(box);}); for(let i=1;i<shapes.length;i++) slide.shapes.connect(shapes[i-1],shapes[i],{kind:'straight',fromSide:'right',toSide:'left',line:{style:'solid',fill:C.gray,width:2},tail:{type:'triangle',width:'sm',length:'sm'}}); if(spec.caption) txt(slide,spec.caption,64,535,1152,46,17,{color:a.muted}); }
function compare(slide,spec) { const a=shell(slide,spec); const columns=spec.columns || []; const width=(1152-48*(columns.length-1))/columns.length; columns.forEach((column,i)=>{const [head,...items]=column; const x=64+i*(width+48); txt(slide,head,x,208,width,height(head,width,26),26,{bold:true,color:i===1?C.blue:a.fg}); rule(slide,x,278,width,i===1?C.blue:C.ink,2); list(slide,items,x,330,width,20,{color:a.muted,gap:26}); }); }
function checks(slide,spec) { const a=shell(slide,spec); const checks=spec.checks || []; const w=(1152-30*(checks.length-1))/checks.length; checks.forEach(([name,detail],i)=>{const x=64+i*(w+30); rect(slide,x,243,w,200,i===2?C.soft:C.white,i===2?C.blue:C.line,1); txt(slide,String(i+1).padStart(2,'0'),x+18,262,w-36,24,14,{mono:true,color:i===2?C.blue:C.gray}); txt(slide,name,x+18,316,w-36,35,22,{bold:true}); txt(slide,detail,x+18,376,w-36,42,18,{color:a.muted}); }); }
function table(slide,spec) { const a=shell(slide,spec); const rows=spec.rows; const cols=rows[0].length; const widths=cols===2?[330,822]:cols===3?[220,330,602]:[240,304,304,304]; const font=17; const values=rows.map(row=>row.map((cell,i)=>wrap(cell,widths[i]-30,font))); const heights=values.map(row=>Math.max(...row.map(cell=>cell.split('\n').length))*font*4/3*1.16+22); const total=heights.reduce((sum,value)=>sum+value,0); if(total>440) throw new Error(`Table too tall on slide ${current}`); const tbl=slide.tables.add({rows:rows.length,columns:cols,left:64,top:188,width:1152,height:total,columnWidths:widths,values}); tbl.styleOptions={headerRow:false,bandedRows:false}; tbl.borders.assign({fill:C.line,width:1,style:'solid'}); values.forEach((row,r)=>{tbl.rows[r].height=heights[r]; row.forEach((value,c)=>{const cell=tbl.getCell(r,c); cell.fill=r===0?C.ink:C.white; cell.text.style={fontSize:font*4/3,typeface:FONT,color:r===0?C.white:C.ink,bold:r===0,autoFit:'none',wrap:'none',verticalAlignment:'middle',insets:{left:15,right:15,top:11,bottom:11}}; });}); minSizes.push(font); if(a.dark) throw new Error('Dark table unsupported'); }
function matrix(slide,spec) { const a=shell(slide,spec); const rows=spec.matrix; const cols=rows[0].length; const widths=cols===3?[230,342,580]:[270,294,294,294]; const font=17; const values=rows.map(row=>row.map((cell,i)=>wrap(cell,widths[i]-30,font))); const heights=values.map(row=>Math.max(...row.map(cell=>cell.split('\n').length))*font*4/3*1.15+22); const total=heights.reduce((sum,value)=>sum+value,0); if(total>440) throw new Error(`Matrix too tall on slide ${current}`); const tbl=slide.tables.add({rows:rows.length,columns:cols,left:64,top:188,width:1152,height:total,columnWidths:widths,values}); tbl.styleOptions={headerRow:false,bandedRows:false};tbl.borders.assign({fill:C.line,width:1,style:'solid'}); values.forEach((row,r)=>{tbl.rows[r].height=heights[r];row.forEach((value,c)=>{const cell=tbl.getCell(r,c);const accent=r>0&&c===0;cell.fill=r===0?C.ink:accent?C.soft:C.white;cell.text.style={fontSize:font*4/3,typeface:FONT,color:r===0?C.white:accent?C.blue:C.ink,bold:r===0||accent,autoFit:'none',wrap:'none',verticalAlignment:'middle',insets:{left:15,right:15,top:11,bottom:11}};});}); minSizes.push(font); if(a.dark) throw new Error('Dark matrix unsupported'); }
function caseLayout(slide,spec) { const a=shell(slide,spec); let y=190; spec.body.forEach((line,i)=>{const pt=i===0?26:20; const h=height(line,1080,pt); if(i===0) rect(slide,64,y,1152,h+42,C.white,C.line,1); txt(slide,line,96,y+(i===0?21:0),1080,h,pt,{bold:i===0,color:i===0?a.fg:a.muted}); y+=h+(i===0?84:28);}); }
function worksheet(slide,spec) { const a=shell(slide,spec); let y=190; for(const [i,line] of spec.body.entries()) { const h=height(line,1030,21);txt(slide,String(i+1).padStart(2,'0'),64,y,60,28,18,{mono:true,color:C.gray});txt(slide,line,152,y,1040,h,21,{color:a.fg});rule(slide,152,y+h+20,1064);y+=h+48;} }
function code(slide,spec) { const a=shell(slide,spec);const code=spec.body.join('\n');const h=code.split('\n').length*16*4/3*1.42+52;rect(slide,64,201,1152,h,C.navy);txt(slide,code,90,226,1100,h-50,16,{mono:true,color:C.white,noWrap:true,leading:1.35});if(spec.caption)txt(slide,spec.caption,64,201+h+28,1152,50,16,{color:a.muted}); }
function roadmap(slide,spec) { const a=shell(slide,spec);const entries=[['01','09.04','실행 추적'],['02','09.11','프롬프트 비교'],['03','09.18','평가 기준'],['04','09.25','검색 근거 · 녹화'],['05','10.02','검색 품질'],['06','10.09','데이터 · 녹화'],['07','10.16','기술 대안'],['08','10.23','기획서 제출·평가'],['09–15','10.30–12.11','구현·운영·프로젝트'],['16','12.18','실시간 온라인 발표']]; entries.forEach((entry,i)=>{const col=Math.floor(i/5),row=i%5,x=64+col*584,y=181+row*84,active=entry[0]==='03';if(active)rect(slide,x,y,552,72,C.soft);txt(slide,entry[0],x+14,y+11,92,22,14,{mono:true,bold:active,color:active?C.blue:C.gray});txt(slide,entry[1],x+112,y+11,124,22,14,{color:active?C.blue:C.gray});txt(slide,entry[2],x+14,y+41,522,25,18,{bold:active,color:active?C.blue:C.ink});if(!active)rule(slide,x,y+73,552);});txt(slide,spec.body.join(' · '),64,620,1152,25,14,{color:a.muted}); }

for (const [index,spec] of slides.entries()) {
  current=index+1; if(spec.n!==current) throw new Error(`Slide order mismatch ${current}`); if(!spec.notes || !spec.sources?.length) throw new Error(`Missing notes or sources ${current}`); if(index>=2 && spec.layout===slides[index-1].layout && spec.layout===slides[index-2].layout) throw new Error(`Three repeated layouts ${current}`);
  const slide=p.slides.add(); layouts.push(spec.layout);
  ({cover,section,statement,steps,timeline:steps,flow,compare,checks,table,matrix,case:caseLayout,worksheet,code,roadmap}[spec.layout] || (()=>{throw new Error(`Unknown layout ${spec.layout}`);}))(slide,spec);
  slide.speakerNotes.textFrame.setText(`${spec.notes}\n\n[Sources]\n${spec.sources.map(item=>`- ${item}`).join('\n')}\n[/Sources]`); slide.speakerNotes.setVisible(true);
}
await fs.writeFile(path.join(BUILD,'geometry.json'),JSON.stringify(boxes,null,2));
await fs.writeFile(path.join(BUILD,'manifest.json'),JSON.stringify({slides:slides.length,minFontPt:Math.min(...minSizes),layouts,palette:C},null,2));
const candidate=path.join(BUILD,'candidate.pptx');
await (await PresentationFile.exportPptx(p)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const finalPath=path.join(BUILD,'final','03_week3_prompt_evaluation_error_analysis.pptx');
await fs.mkdir(path.dirname(finalPath),{recursive:true});
await finalizePresentation({workspaceDir:ROOT,candidatePath:candidate,finalPath,explicitTotalSlideCount:72,pythonExecutable:PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],fontPolicy:{basis:'design',families:[FONT,MONO]},verifyArtifactToolImport:true,receiptPath:path.join(BUILD,'validation.json')});
console.log(JSON.stringify({finalPath,slides:slides.length,minFontPt:Math.min(...minSizes),layouts:[...new Set(layouts)]}));
