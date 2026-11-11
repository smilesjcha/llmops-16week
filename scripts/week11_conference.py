"""Presentation-specific composition and authored diagram walkthroughs."""

import html
import json
import re

# Node indices refer to the editable SVG order, not visual position.
WALKS = {
    4: [
        ([0, 1], "정책 준비", "유효한 원문과 버전을 색인에 반영합니다."),
        (
            [2, 3],
            "질문과 검색",
            "사용자 질문으로 관련 문서를 찾습니다. 검색 성공은 답변 정확성과 다릅니다.",
        ),
        ([4, 5], "생성과 응답", "질문·근거·지시로 답변을 생성하고 출처와 기권을 처리합니다."),
        (
            [3, 4, 6],
            "검증과 원인 추적",
            "검색과 생성의 결과를 각각 평가하고 같은 요청의 기록으로 연결합니다.",
        ),
    ],
    5: [
        (
            [0, 1, 2],
            "동일 질문의 두 실행",
            "평가 세트의 질문을 기준선과 후보에 동일하게 전달합니다.",
        ),
        (
            [1, 2, 3],
            "실제 출력의 비교",
            "두 버전의 실제 출력을 코드·모델·사람 평가기로 비교합니다.",
        ),
        (
            [0, 3],
            "참고 기준의 별도 경로",
            "참고 정답은 평가기에만 전달합니다. 생성 입력에는 포함하지 않습니다.",
        ),
        (
            [3, 4],
            "판단 근거의 기록",
            "평균 지표와 개별 실패를 함께 보고 변경의 채택 여부를 검토합니다.",
        ),
    ],
    21: [
        (
            [0, 1],
            "검색 점수와 수락 조건",
            "최고 점수를 임계값과 비교합니다. 점수는 정답 확률이 아닙니다.",
        ),
        (
            [1, 2],
            "조건 충족",
            "검색 근거를 모델에 전달해 응답을 시도합니다. 내용 검사는 여전히 필요합니다.",
        ),
        ([1, 3], "조건 미충족", "확인 불가를 안내하거나 추가 질문으로 연결합니다."),
    ],
    44: [
        ([0, 1], "모델 호출 경로", "Python이 호스트의 Ollama에 요청하고 실제 응답을 받습니다."),
        (
            [0, 2],
            "추적과 점수 전송",
            "같은 Python 실행이 SDK로 Langfuse에 입력·출력·평가 점수를 보냅니다.",
        ),
        (
            [2, 3],
            "비동기 저장",
            "worker와 저장소가 기록을 처리합니다. flush 이후 API로 저장을 확인합니다.",
        ),
        (
            [0, 1, 2, 3],
            "독립적인 두 경로",
            "Langfuse가 모델을 호출하는 구조가 아닙니다. 모델 실행과 기록 전송의 장애를 나눠 봅니다.",
        ),
    ],
}


def enhance(slides):
    slides[0]["body"] = (
        """<div class="conference-cover"><p class="cover-question">이 변경을<br>배포해도 되는가?</p><div class="cover-route"><div><strong>실제 응답</strong><p>근거·조건·기권의 확인</p></div><div><strong>비교 실험</strong><p>같은 질문, 다른 버전</p></div><div><strong>배포 판단</strong><p>실패 증거와 다음 개선</p></div></div></div><p class="cover-author">차성재 · 무신사 Core AI PM × AI 대학원 겸임교수</p>"""
    )
    # These are changes of teaching mode, not decorative emphasis on the ending.
    slides[42]["dark"] = True
    slides[42]["kind"] = "mission-opening"
    for page, steps in WALKS.items():
        slide = slides[page - 1]
        encoded = html.escape(json.dumps(steps, ensure_ascii=False), quote=True)
        body = re.sub(r'<div class="architecture-text">.*?</div>', "", slide["body"], flags=re.S)
        reading = (
            '<ol class="architecture-text">'
            + "".join(
                f"<li><strong>{html.escape(title)}</strong><p>{html.escape(note)}</p></li>"
                for _, title, note in steps
            )
            + "</ol>"
        )
        slide["body"] = (
            f'<div class="diagram-walk" data-walk="{encoded}">{body}{reading}<div class="walk-controls"><button class="walk-back" disabled aria-label="이전 흐름 단계">이전 단계</button><p class="walk-caption" aria-live="polite">전체 구조 · 흐름 보기를 눌러 설명 시작</p><button class="walk-next">흐름 보기</button><button class="walk-reset" disabled>전체 보기</button></div></div>'
        )
    screen_notes = {
        46: [
            ("1 · 요청 전체", "질문 한 건 아래 네 작업의 연결"),
            ("2 · 생성 입력", "02-ollama-answer에서 실제 근거 확인"),
            ("3 · 원인 추적", "답변과 검색 문서의 조건 대조"),
        ],
        47: [
            ("1 · 코드 검사", "인용·기권의 규칙 확인"),
            ("2 · 모델 평가", "supported와 판정 이유 검토"),
            ("3 · 사람 검토", "점수 통과와 의미 정확성의 구분"),
        ],
        51: [
            ("1 · 비교 대상", "같은 데이터의 A와 C"),
            ("2 · 개별 지표", "false_accept와 structural_pass"),
            ("3 · 다음 확인", "Grid에서 실패 응답과 trace 확인"),
        ],
    }
    for page, notes in screen_notes.items():
        body = slides[page - 1]["body"]
        rows = (
            '<div class="rows">'
            + "".join(f'<div class="row"><strong>{a}</strong><p>{b}</p></div>' for a, b in notes)
            + "</div>"
        )
        slides[page - 1]["body"] = '<div class="screen-study">' + body + rows + "</div>"
    slides[51]["body"] = slides[51]["body"].replace("<table>", '<table class="decision-table">')
    slides[51]["body"] = (
        '<p class="decision-lead">기능 경계로 오답 차단.<br><span>배포 전에는 답변 내용 검토.</span></p>'
        + slides[51]["body"]
    )
    # Reading tables retain a labeled structure without compressing four columns.
    for slide in slides:
        slide["body"] = re.sub(
            r"<table(.*?)>(.*?)</table>", _label_table, slide["body"], flags=re.S
        )
    guide = "https://smilesjcha.github.io/llmops-16week/week11/lab/demo/"
    slides[53]["body"] += f'<p class="label"><a href="{guide}">화면별 시연 순서와 사전 점검</a></p>'
    slides[-1]["body"] += f'<p class="label"><a href="{guide}">교수·학생용 실습 화면 안내</a></p>'
    return slides


def _label_table(match):
    attrs, body = match.groups()
    head = re.search(r"<thead>(.*?)</thead>", body, re.S)
    if not head:
        return match.group(0)
    labels = [re.sub("<[^>]+>", "", t) for t in re.findall(r"<th[^>]*>(.*?)</th>", head[1], re.S)]

    def label_row(row):
        index = iter(labels)
        return (
            "<tr>"
            + re.sub(
                r"<td>(.*?)</td>",
                lambda cell: '<td data-label="'
                + html.escape(next(index, ""), quote=True)
                + '">'
                + cell[1]
                + "</td>",
                row[1],
                flags=re.S,
            )
            + "</tr>"
        )

    body = re.sub(
        r"<tbody>(.*?)</tbody>",
        lambda b: "<tbody>" + re.sub(r"<tr>(.*?)</tr>", label_row, b[1], flags=re.S) + "</tbody>",
        body,
        flags=re.S,
    )
    return f"<table{attrs}>{body}</table>"
