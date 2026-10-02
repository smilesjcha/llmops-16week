import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';

const root=path.resolve(import.meta.dirname,'..');
const skill=process.env.PRESENTATIONS_SKILL_DIR, py=process.env.ARTIFACT_PYTHON;
if(!skill||!py)throw Error('PRESENTATIONS_SKILL_DIR and ARTIFACT_PYTHON required');
const target=path.join(root,'week08/templates/08_project_proposal_ppt_template.pptx');
const build=path.join(root,'week08/templates/build');
await fs.mkdir(build,{recursive:true});
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={ink:'#151719',black:'#08090B',white:'#FFFFFF',paper:'#F6F7F9',navy:'#102747',blue:'#2563EB',soft:'#E8F0FF',gray:'#536174',line:'#D4DAE3'};
P.theme.colorScheme={name:'BLACK WHITE BLUE',themeColors:{accent1:C.blue,accent2:C.navy,accent3:C.gray,accent4:C.soft,accent5:C.ink,accent6:C.line,bg1:C.white,bg2:C.black,tx1:C.ink,tx2:C.white,dk1:C.black,dk2:C.navy,lt1:C.white,lt2:C.paper,hlink:C.blue,folHlink:C.navy}};
const FONT='AppleGothic';
let n=0;
function rect(s,x,y,w,h,fill='none',stroke='none',sw=0){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill,line:{fill:stroke,width:sw,style:'solid'}})}
function text(s,value,x,y,w,h,pt=20,{bold=false,color=C.ink}={}){if(pt<14||x+w>1280||y+h>720)throw Error('Invalid text geometry');const b=rect(s,x,y,w,h);b.text=value;b.text.style={typeface:FONT,fontSize:pt*4/3,color,bold,alignment:'left',verticalAlignment:'top',wrap:'none',autoFit:'none',lineSpacing:1.12,insets:{top:0,bottom:0,left:0,right:0}};return b}
function shell(title){n++;const s=P.slides.add();s.background.fill=C.paper;text(s,'LLMOPS / PROJECT PROPOSAL',64,30,900,28,14,{color:C.gray});text(s,String(n).padStart(2,'0'),1140,30,75,28,14,{color:C.gray});text(s,title,64,88,1152,76,33,{bold:true});rect(s,64,660,1152,1,C.line);text(s,'2026-2 · 초안 0.1 → 피드백 → 수정본 0.2',64,679,1152,24,14,{color:C.gray});return s}
function card(s,x,y,w,h,label,body){rect(s,x,y,w,h,C.white,C.line,1);text(s,label,x+18,y+18,w-36,40,21,{bold:true,color:C.navy});rect(s,x+18,y+70,w-36,1,C.line);text(s,body,x+18,y+92,w-36,h-108,18,{color:C.gray})}
function notes(s,body){s.speakerNotes.textFrame.setText(body);s.speakerNotes.setVisible(true)}

{
 const s=P.slides.add();n++;s.background.fill=C.black;
 text(s,'LLMOPS / 2026-2',64,42,1100,26,14,{color:C.gray});
 text(s,'[프로젝트명]\n서비스 기획 요약',64,170,1150,195,52,{bold:true,color:C.white});
 rect(s,64,430,1152,1,'#384456');
 text(s,'[대상 사용자 · 해결할 문제 · 한 문장 제안]',64,469,1152,50,23,{color:C.white});
 text(s,'[개인 또는 팀명]  ·  [0.1 초안 / 0.2 수정본]',64,552,1152,36,18,{color:C.gray});
 notes(s,'제목은 서비스명 또는 해결할 문제를 명사형으로 쓴다. 아직 검증 전인 주장을 성과처럼 쓰지 않는다.');
}
{
 const s=shell('문제와 제안 가치');
 card(s,64,209,548,274,'현재 사용자 경험','[누가 · 어떤 상황에서 · 무엇이 불편한가]\n[현재 대안과 해결되지 않는 부분]');
 card(s,636,209,580,274,'제안과 확인할 근거','[서비스의 핵심 제안]\n[조사 출처와 아직 검증할 가설]');
 text(s,'구분: 관찰한 사실 / 팀의 가정 / 앞으로 검증할 가설',64,545,1152,42,20,{color:C.navy});
 notes(s,'사용자 불편과 해결 가치를 두괄식으로 제시한다. 조사 출처·날짜를 부록에 적고 추측은 가설로 표시한다.');
}
{
 const s=shell('사용자 흐름과 실패 대응');
 const xs=[64,357,650,943];const heads=['01 입력','02 처리','03 결과','04 수정'];const bodies=['[사용자 입력·권한]','[검색·모델·도구]','[근거·출력·보류]','[재질문·수정]'];
 xs.forEach((x,i)=>{rect(s,x,239,267,186,C.white,C.line,1);text(s,heads[i],x+18,261,230,44,21,{bold:true,color:C.navy});text(s,bodies[i],x+18,338,230,60,18,{color:C.gray})});
 text(s,'대기 · 오류 · 근거 부족 · 권한 부족일 때 사용자가 취할 다음 행동',64,510,1152,72,21,{color:C.gray});
 notes(s,'정상 흐름만 제시하지 않는다. 실패와 답변 보류를 사용자 경험의 일부로 설계한다.');
}
{
 const s=shell('데이터와 기술 구조');
 card(s,64,203,361,304,'데이터','[출처 · 사용 권한 · 버전]\n[민감정보 · 보관 · 삭제]');
 card(s,459,203,361,304,'처리','[검색 / 모델 / 도구]\n[입력·출력·권한 경계]');
 card(s,854,203,361,304,'운영','[로그 · 보류 · 사람 검토]\n[실패 복구 · 비용]');
 text(s,'선택 이유: [가장 단순한 기준선 대비 어떤 가치를 기대하는가]',64,552,1152,50,20,{color:C.navy});
 notes(s,'비용·보안·운영 조건을 포함한 구현 가능한 선택을 설명한다. 실제 고객 자료의 업로드 권한을 가정하지 않는다.');
}
{
 const s=shell('평가 계획과 판단 기준');
 const rows=[['기준선','[현재 방식 또는 단순한 검색·모델]'],['대표 입력','[답 있음 · 답 없음 · 표현 차이 · 권한/날짜]'],['성공·실패','[품질 지표 · 실패 분석 · 답변 보류 기준]'],['운영','[응답 시간 · 비용 · 오류의 측정 조건]']];
 rows.forEach(([a,b],i)=>{const y=203+i*91;rect(s,64,y,1152,79,i%2?C.white:C.soft);text(s,a,83,y+17,234,45,20,{bold:true,color:C.navy});text(s,b,336,y+17,860,51,18,{color:C.ink})});
 notes(s,'개발 질의와 최종 확인 질의를 분리한다. 측정하지 않은 성능 수치를 기입하지 않는다.');
}
{
 const s=shell('초안 · 피드백 · 수정본');
 const rows=[['10.16 / 7주차','초안 0.1 제출 · 교수의 질문과 피드백 기록'],['10.23 / 8주차','피드백 반영 수정본 0.2 제출 · 온라인 평가'],['제출 경로','아주대AI대학원 팀: LMS · 다른 학교 개인: 공지된 교수 이메일'],['허용 형식','PPT · Word · Word 기반 PDF · HTML / 한글(HWP) 제외']];
 rows.forEach(([a,b],i)=>{const y=199+i*94;rect(s,64,y,1152,1,C.line);text(s,a,64,y+18,300,56,20,{bold:true,color:C.navy});text(s,b,390,y+18,822,61,18,{color:C.gray})});
 notes(s,'7주차 초안 피드백을 받은 뒤 수정 이유를 기록해 8주차 수정본에 반영한다. 정확한 제출 시각과 이메일은 소속별 공지를 확인한다.');
}

const candidate=path.join(build,'candidate.pptx');await(await PresentationFile.exportPptx(P)).save(candidate);
const {finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:target,explicitTotalSlideCount:6,pythonExecutable:py,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit'],fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:path.join(root,'output/validation/proposal-ppt-validation.json')});
console.log(target);
