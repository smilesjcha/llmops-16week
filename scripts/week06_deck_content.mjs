const curriculum='repo:curriculum/2026-2/00_운영_커리큘럼.md';
const lab='repo:course_labs/adaptation.py';
const sft='https://huggingface.co/docs/trl/sft_trainer';
const lora='https://arxiv.org/abs/2106.09685';
const qlora='https://arxiv.org/abs/2305.14314';
const bits='https://huggingface.co/blog/4bit-transformers-bitsandbytes';
const peft='https://huggingface.co/docs/peft/developer_guides/lora';
const S=(title,kind,items,extra={})=>({title,kind,items,sources:[curriculum,lab],...extra});
const T=(title,items,extra={})=>S(title,'table',items,extra);
const F=(title,items,caption)=>S(title,'flow',items,{caption});
const E=(title,items,extra={})=>S(title,'case',items,extra);
const I=(title,file,items,extra={})=>S(title,'image',items,{image:'week06/lecture/assets/'+file,monochrome:true,...extra});
export const week06={week:6,name:'06_week6_sft_lora_reference',title:'지도 미세조정과 메모리 효율',subtitle:'SFT · LoRA · QLoRA · 데이터와 평가',slides:[
 S('지도 미세조정과\n메모리 효율','cover',['SFT · LoRA · QLoRA','6주차 학습 단원 보충 · 7주차 통합 강의 복습','차성재 · 무신사 Core AI PM × AI 대학원 겸임교수']),
 E('6–7주차 자료의 연결',['10월 9일 휴일에는 수업·녹화·신규 과제 없음','6주차 기술 내용은 10월 16일 7주차에서 함께 진행','통합 녹화 영상과 이번 시각 자료로 복습'],{caption:'기획서 마감: 10.22(목) 23:59 한국시간 · 10.23은 제출물 평가'}),
 S('오늘의 구분','steps',[['SFT','어떤 입력과 기대 답변으로 학습하는가'],['LoRA','어떤 파라미터를 갱신하는가'],['QLoRA','고정 모델을 어떤 정밀도로 저장하는가']],{caption:'SFT라는 학습 목적에 LoRA 또는 QLoRA를 결합할 수 있음',sources:[sft,lora,qlora]}),
 T('학습보다 먼저 확인할 문제',[['문제','첫 비교 대상','확인할 근거'],['최신 정책 오류','검색·문서 버전','적용일·출처·권한'],['출력 형식 오류','프롬프트·출력 검사','같은 입력의 반복 실패'],['반복 행동 불안정','SFT·Adapter','허가된 예시·보류 평가셋']]),
 S('지도 미세조정','section',['Supervised Fine-Tuning · SFT','업무 입력과 기대 답변으로 다음 토큰 예측 학습']),
 I('SFT의 토큰 예측과 손실','sft-trainer.png',[['입력','input_ids: 토큰 ID의 나열'],['예측','logits: 다음 토큰의 점수'],['비교','labels와 교차 엔트로피 손실']],{imageMode:'tall-explain',sources:[sft],caption:'Hugging Face TRL 공식 도식 · 원본 이미지의 흑백 표시',notes:'입력의 각 위치에서 다음 토큰을 예측한다. 마지막 예측 위치와 첫 label의 제외 구간을 원본 도식에서 확인한다. logits는 확률 변환 전 점수다. 실제 trainer 구현의 label shift와 loss mask를 별도로 확인한다.'}),
 S('학습 데이터 한 건','annotated',['instruction: 문의 상태 정리\ninput: 합성 사례 DEMO-01\nresponse:\n  status: review\n  source: DEMO-01','입력과 기대 출력의 경계','합성 사례만 사용','형식·정확성 별도 검토'],{caption:'상태·출처를 정리하는 설명용 예시 · 실제 정책 아님'}),
 F('자료 준비와 평가 분리',[['수집','사용 허가'],['검사','필드·중복'],['분할','사건·시간'],['보류','최종 평가셋']],'같은 사건의 표현을 train과 test에 나누면 평가가 낙관적으로 보일 수 있음'),
 I('답변 구간의 손실 마스킹','sft-assistant-mask.png',[['user','사용자 입력은 참고 문맥'],['assistant','선택한 답변 토큰에 학습 신호'],['빗금 구간','손실 계산에서 제외한 위치']],{imageMode:'wide-explain',sources:[sft],caption:'Hugging Face TRL · assistant-only loss · 모델별 템플릿 확인',notes:'그림은 여러 대화 턴 가운데 assistant 답변의 label만 남기는 구조다. assistant_only_loss의 실제 지원 여부와 마스크 생성은 사용 모델의 chat template에 달려 있다.'}),
 I('Prompt와 Completion의 분리','sft-completion-mask.png',[['prompt','질문·지시·참고 문맥'],['completion','기대 답변'],['확인','답변 경계·종료 토큰·잘림']],{imageMode:'wide-explain',sources:[sft],caption:'Hugging Face TRL · completion-only loss · assistant-only와 입력 형식 구분'}),
 S('마스킹의 최소 확인','code',['token_ids = [10, 11, 12, 20, 21, 22]','labels = [-100, -100, -100, 20, 21, 22]','assert sum(x != -100 for x in labels) == 3'],{caption:'가상 토큰 ID · 실제 모델 tokenizer 실행과 구분'}),
 E('길이 제한과 답변 누락',['긴 문맥이 답변 구간을 밀어내는 문제','문자 길이 대신 해당 모델의 토큰 길이 확인','긴 사례·짧은 사례·경계 사례를 따로 점검'],{sources:[sft],caption:'답변 정답이 잘린 데이터로 학습하지 않도록 사전 검사'}),
 S('LoRA의 구조','section',['Low-Rank Adaptation · 저차원 행렬 기반 모델 적응','기존 가중치는 고정하고 작은 두 행렬을 학습']),
 I('LoRA 원 논문의 두 경로','lora-paper-figure1.png',[['고정 경로 W','기존 모델의 계산 유지'],['학습 경로 A·B','작은 변화량을 학습'],['합산','두 경로의 출력 결합']],{imageMode:'side-explain',sources:[lora],caption:'Hu et al., 2021, Figure 1 · 원본 도식 발췌·흑백 렌더링',notes:'원 논문에서는 A를 무작위로, B를 0으로 초기화하므로 초기 변화량은 0이다. 그림의 좌우 경로를 차례로 읽는다. 고정 가중치도 순전파 계산에는 참여한다.'}),
 S('가중치 변화의 표현','formula',['W′ = W + (α/r) · BA','W: 고정 모델 가중치 · A와 B: 학습 행렬','r: rank · α: 변화량의 배율 설정'],{sources:[lora,peft],caption:'일반 LoRA scaling 기준 · rsLoRA 등 다른 변형은 설정을 구분'}),
 F('작은 행렬의 차원',[['입력','8차원'],['A','2 × 8'],['B','12 × 2'],['출력','12차원']],'예시 r=2 · BA는 12×8 · 7주차 Notebook 02와 연결'),
 S('rank별 학습 파라미터','chart',[],{chart:'adaptation-params',caption:'12×8 합성 행렬 · 전체 96개 · 두 행렬 r(12+8) · 실제 GPU 측정 아님'}),
 E('rank 선택의 조건',['작은 rank는 적은 파라미터로 변화량을 표현','큰 rank가 항상 더 좋은 업무 품질을 보장하지 않음','고정된 평가 입력과 비용으로 후보 비교'],{sources:[lora,peft],caption:'작은 12×8 예시에서는 rank 8의 두 행렬이 원본보다 큼'}),
 S('LoRA 설정의 역할','annotated',['r = 8\nlora_alpha = 16\ntarget_modules = ["q_proj", "v_proj"]\nseed = 42','설정과 실행 결과의 구분','rank·alpha: 용량과 배율','target_modules: 적용할 모듈','seed 외 환경도 함께 기록'],{sources:[lora,peft],caption:'설정 설명용 예시 · 모델 구조·구현 버전에 따라 재검증'}),
 S('QLoRA의 메모리 절약','section',['Quantized Low-Rank Adaptation · 양자화 기반 LoRA','고정 모델의 저장 비용까지 줄이는 접근']),
 I('전체 미세조정·LoRA·QLoRA','qlora-paper-figure1.png',[['전체 미세조정','모델 가중치와 optimizer 상태'],['LoRA','고정 모델과 학습 Adapter'],['QLoRA','4-bit 고정 모델과 Adapter']],{imageMode:'full-figure',sources:[qlora],caption:'QLoRA Figure 1 · CC BY 4.0 · 흑백 발췌',notes:'그림의 면적은 실측 메모리 막대가 아니다. 위쪽 optimizer state, 가운데 adapter, 아래 base model을 비교한다. paging 화살표는 CPU/GPU 메모리 이동이며, 고정 모델의 학습 갱신을 뜻하지 않는다.'}),
 S('저장 정밀도와 계산 정밀도','compare',[['저장','고정 모델의 주 가중치를 4-bit로 압축','블록별 스케일 등 추가 정보 보존'],['계산','필요한 연산에서 복원해 계산','Adapter는 높은 정밀도로 학습']],{sources:[qlora,bits],caption:'4-bit 저장은 모든 연산·활성값·optimizer가 4-bit라는 뜻이 아님'}),
 T('QLoRA의 세 가지 구성',[['기술','역할'],['NF4 · 4-bit NormalFloat','정규분포 가중치를 고려한 양자화 표현'],['Double Quantization','양자화 상수도 양자화해 부가 저장량 절약'],['Paged Optimizers','메모리 급증 시 CPU/GPU 메모리 관리']],{sources:[qlora],caption:'실제 지원 하드웨어·커널·학습 설정은 별도 확인'}),
 T('가중치 저장량의 계산',[['정밀도','7B × bit/8','읽는 방법'],['16-bit','14.0 GB','가중치 원시 저장량'],['8-bit','7.0 GB','추가 메타데이터 제외'],['4-bit','3.5 GB','총 학습 메모리가 아님']],{sources:[qlora],caption:'7B=70억 파라미터 가정 · 십진 GB · scale·Adapter·activation·optimizer 제외'}),
 E('총 학습 메모리의 구성',['압축한 모델 가중치 외의 추가 비용','Adapter·gradient·optimizer state·activation','입력 길이·batch·체크포인팅·버퍼도 영향'],{sources:[qlora,bits],caption:'같은 모델·길이·batch에서 최대 사용량을 측정해 판단'}),
 S('학습 환경의 사전 점검','steps',[['지원','하드웨어·정밀도·라이브러리 조합'],['작은 실행','짧은 길이·작은 batch로 점검'],['평가','정답·형식·비용의 기준선 확보']],{sources:[sft,peft],caption:'공통 Notebook은 GPU·모델 다운로드 없는 개념 실험으로 진행'}),
 S('Base와 Adapter의 비교','section',['동일 입력에서 답변 품질과 운영 비용을 확인','학습 손실과 실제 사용 품질의 구분']),
 T('평가 조건과 기록',[['검사','같게 유지할 조건','남길 결과'],['업무 품질','입력·근거·출력 규칙','통과·실패와 응답 원문'],['비용','기기·길이·반복·예열','시간·최대 메모리'],['재현','모델·토크나이저·Adapter','버전·설정·데이터 해시']]),
 E('손실 감소 이후의 실패',['출력 형식은 좋아졌지만 근거 없는 답변 증가','학습 사례에는 정확하지만 새 사건에는 실패','형식·근거·보류·일반화를 분리해서 검토']),
 F('Adapter의 보존과 복구',[['Base','모델 revision'],['Tokenizer','chat template'],['Adapter','가중치·설정'],['평가','입력·원문·결정']],'Adapter 파일만 저장하면 재현과 복구에 필요한 정보가 빠짐'),
 S('실습 연결과 확인 질문','steps',[['Notebook 01','동일 사건이 분할을 넘는 데이터 누출 탐지'],['Notebook 02','rank·행렬 오차·파라미터 수 비교'],['확인 질문','실제 모델 학습과 이번 수치 실험의 차이']],{caption:'7주차 lab/notebooks · 기존 실습 파일과 공통 requirements 유지'}),
 S('참고 자료와 복습 경로','citation',['Hugging Face TRL · SFT Trainer 공식 도식','LoRA 원 논문 · QLoRA 원 논문과 공식 해설','7주차 통합 녹화 · Notebook 01·02'],{sources:[sft,lora,qlora,bits,peft,lab],caption:'원본 이미지 출처·이용 범위: lecture/assets/SOURCES.md'})
]};
