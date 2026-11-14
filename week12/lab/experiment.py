"""Immutable experiment contract and deterministic user allocation."""
from dataclasses import asdict, dataclass
import hashlib
import json
import re


@dataclass(frozen=True)
class Experiment:
    experiment_id: str = "w12-help-v1"
    allocation_b: float = 0.5
    min_per_arm: int = 1000
    planned_days: int = 14
    srm_alpha: float = 0.001
    max_p95_ms: float = 1800.0
    max_error_rate: float = 0.03
    practical_lift: float = 0.03
    metric: str = "first_request_confirmed_resolution"
    observation_minutes: int = 30

    def __post_init__(self):
        if not re.fullmatch(r"[a-zA-Z0-9_-]{1,64}", self.experiment_id):
            raise ValueError("experiment_id는 1–64자 영문·숫자·-·_입니다.")
        if not 0 < self.allocation_b < 1:
            raise ValueError("두 버전 모두에 사용자를 배정해야 합니다.")
        if self.min_per_arm < 5 or self.planned_days < 1 or self.observation_minutes < 1:
            raise ValueError("표본·기간·관찰 창을 사전에 정하세요.")
        if not 0 < self.srm_alpha < 1 or not 0 <= self.max_error_rate < 1:
            raise ValueError("확률 기준 범위 오류")
        if not 0 < self.max_p95_ms < float("inf") or not 0 <= self.practical_lift <= 1:
            raise ValueError("지연·개선 기준 범위 오류")

    @property
    def version(self):
        raw = json.dumps(asdict(self), sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()[:12]


DEFAULT = Experiment()


def bucket(visitor_id: str, experiment_id: str = DEFAULT.experiment_id) -> float:
    if not re.fullmatch(r"u-[a-zA-Z0-9_-]{1,48}", visitor_id):
        raise ValueError("실습용 u- 식별자만 사용하세요. 이름·이메일은 입력하지 않습니다.")
    digest = hashlib.sha256(f"{experiment_id}:{visitor_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def assign(visitor_id: str, config: Experiment = DEFAULT) -> str:
    """Stable within a frozen experiment. Changing allocation/config starts a new analysis."""
    return "B" if bucket(visitor_id, config.experiment_id) < config.allocation_b else "A"


POLICIES = {
    "exchange": "가상 정책: 수령 후 7일 이내 교환 접수. 재고가 있어야 하며 왕복 배송비 6000원.",
    "return": "가상 정책: 수령 후 7일 이내 반품 접수. 단순 변심 반품 배송비 3000원.",
    "stock": "가상 정책 문서에는 실시간 재고가 없습니다. 재고 조회 도구도 연결되지 않았습니다.",
}
PROMPTS = {
    "A": "정책에 있는 사실만 사용해 한국어 두 문장으로 답하세요. 짧은 직접 답변을 먼저 제시하세요.",
    "B": "정책에 있는 사실만 사용해 한국어로 답하세요. 1. 가능 조건 2. 비용 3. 다음 행동의 세 항목으로 짧게 설명하세요.",
}


def template_answer(topic: str, variant: str) -> str:
    """Explicit policy templates for fast plumbing practice; not a mock LLM output."""
    text = POLICIES[topic].replace("가상 정책: ", "")
    if topic == "stock":
        return "실시간 재고는 확인할 수 없습니다. 고객센터 또는 상품 페이지에서 확인해 주세요."
    return text if variant == "A" else text + "\n다음 행동: 주문 내역에서 접수하고 재고·배송비를 확인해 주세요."
