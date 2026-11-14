"""Transparent two-arm teaching analysis, at a pre-specified fixed horizon."""
from dataclasses import asdict
import math
from statistics import NormalDist

import numpy as np
import pandas as pd

from .experiment import DEFAULT, Experiment, assign

REQUIRED = {"visitor_id", "variant", "config_version", "experiment_id", "resolved", "feedback_received",
            "exposed", "error", "latency_ms", "source"}


def validate_units(frame: pd.DataFrame, config: Experiment = DEFAULT) -> list[str]:
    """Reject missing rows/contradictory outcomes instead of silently cleaning evidence."""
    issues = []
    missing = REQUIRED - set(frame.columns)
    if missing:
        return ["필수 열 누락: " + ", ".join(sorted(missing))]
    if frame.empty:
        return ["분석할 사용자가 없습니다."]
    if frame.visitor_id.isna().any() or frame.visitor_id.duplicated().any():
        issues.append("사용자 단위 누락·중복: 첫 요청 한 건으로 집계하세요.")
    if not frame.variant.isin(["A", "B"]).all():
        issues.append("A/B 이외의 배정값")
    if not frame.config_version.eq(config.version).all() or not frame.experiment_id.eq(config.experiment_id).all():
        issues.append("실험 설정 버전 불일치")
    for field in ["resolved", "feedback_received", "exposed", "error"]:
        if not frame[field].isin([0, 1, False, True]).all():
            issues.append(f"{field}: 0/1 이외의 값 또는 결측")
    latency = pd.to_numeric(frame.latency_ms, errors="coerce")
    if not np.isfinite(latency).all() or (latency < 0).any():
        issues.append("지연 시간 결측·음수·무한값")
    if ((frame.resolved == 1) & ((frame.feedback_received != 1) | (frame.exposed != 1) | (frame.error != 0))).any():
        issues.append("해결 확인과 노출·피드백·실패 기록 모순")
    try:
        expected = frame.visitor_id.map(lambda x: assign(x, config))
        if not expected.eq(frame.variant).all():
            issues.append("고정 배정과 실제 버전 불일치")
    except (ValueError, TypeError):
        issues.append("잘못된 실습 사용자 ID")
    if frame.source.isna().any() or frame.source.nunique() != 1:
        issues.append("데이터 출처 누락·혼합")
    return issues


def srm_test(n_a: int, n_b: int, allocation_b: float = 0.5):
    """Pearson goodness-of-fit, df=1; use only with expected counts >= 5."""
    if min(n_a, n_b) < 0 or not 0 < allocation_b < 1:
        raise ValueError("배정 수와 기대 비율 범위 오류")
    total = n_a + n_b
    expected = [total * (1-allocation_b), total * allocation_b]
    if min(expected) < 5:
        return {"chi2": None, "p_value": None, "sufficient": False}
    chi2 = sum((o-e)**2/e for o, e in zip([n_a, n_b], expected))
    return {"chi2": chi2, "p_value": math.erfc(math.sqrt(chi2/2)), "sufficient": True}


def wilson(success: int, n: int, confidence: float = 0.95):
    if n <= 0 or not 0 <= success <= n or not 0 < confidence < 1:
        raise ValueError("성공 수·분모·신뢰수준을 확인하세요.")
    z = NormalDist().inv_cdf((1+confidence)/2)
    p = success/n
    center = (p + z*z/(2*n))/(1+z*z/n)
    half = z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/(1+z*z/n)
    return [max(0.0, center-half), min(1.0, center+half)]


def difference_interval(s_a, n_a, s_b, n_b):
    """Newcombe (1998), independent proportions, Wilson-score combination, no CC."""
    p_a, p_b = s_a/n_a, s_b/n_b
    l_a, u_a = wilson(s_a, n_a)
    l_b, u_b = wilson(s_b, n_b)
    diff = p_b-p_a
    return {"difference": diff, "low": diff-math.sqrt((p_b-l_b)**2+(u_a-p_a)**2),
            "high": diff+math.sqrt((u_b-p_b)**2+(p_a-l_a)**2), "method": "Newcombe-Wilson 95% fixed-horizon"}


def sample_size(baseline=0.55, absolute_effect=0.05, alpha=0.05, power=0.8):
    """Approximate two-sided equal-allocation planning for a binary user metric."""
    p1, p2 = baseline, baseline+absolute_effect
    if not 0 < p1 < 1 or not 0 < p2 < 1 or absolute_effect == 0 or not 0 < alpha < 1 or not 0 < power < 1:
        raise ValueError("표본 계획 범위를 확인하세요.")
    z_a, z_b = NormalDist().inv_cdf(1-alpha/2), NormalDist().inv_cdf(power)
    mean = (p1+p2)/2
    return math.ceil((z_a*math.sqrt(2*mean*(1-mean))+z_b*math.sqrt(p1*(1-p1)+p2*(1-p2)))**2/(p2-p1)**2)


def analyze(frame: pd.DataFrame, config: Experiment = DEFAULT, *, elapsed_days=14, outcomes_mature=True):
    issues = validate_units(frame, config)
    report = {"contract": asdict(config), "config_version": config.version, "source": "" if frame.empty else str(frame.get("source", pd.Series([""])).iloc[0]),
              "decision": "INVALID", "reasons": issues, "arms": {}, "effect": None, "srm": None,
              "elapsed_days": elapsed_days, "outcomes_mature": outcomes_mature}
    if issues:
        return report
    if not math.isfinite(elapsed_days) or elapsed_days < 0 or not isinstance(outcomes_mature, bool):
        report["reasons"] = ["관찰 기간·완료 상태 오류"]
        return report
    for variant in ["A", "B"]:
        g = frame[frame.variant == variant]
        n = len(g)
        report["arms"][variant] = {"n": n, "resolved": int(g.resolved.sum()), "rate": float(g.resolved.mean()) if n else None,
                                  "feedback_rate": float(g.feedback_received.mean()) if n else None,
                                  "exposure_rate": float(g.exposed.mean()) if n else None,
                                  "error_rate": float(g.error.mean()) if n else None,
                                  "p95_ms": float(np.quantile(g.latency_ms, .95)) if n else None}
    a, b = report["arms"]["A"], report["arms"]["B"]
    report["srm"] = srm_test(a["n"], b["n"], config.allocation_b)
    if report["srm"]["p_value"] is not None and report["srm"]["p_value"] < config.srm_alpha:
        report["reasons"] = ["SRM: 배정·수집·필터를 진단하기 전 효과 해석 중단"]
        return report
    if min(a["n"], b["n"]) == 0:
        report.update(decision="WAIT", reasons=["한 버전의 사용자가 없습니다."])
        return report
    report["effect"] = difference_interval(a["resolved"], a["n"], b["resolved"], b["n"])
    # Safety monitoring does not wait for a statistically significant primary benefit.
    guardrails = []
    for label, arm in [("A", a), ("B", b)]:
        if arm["p95_ms"] > config.max_p95_ms:
            guardrails.append(f"{label} p95 {arm['p95_ms']:.0f}ms > {config.max_p95_ms:.0f}ms")
        if arm["error_rate"] > config.max_error_rate:
            guardrails.append(f"{label} 오류율 {arm['error_rate']:.1%} > {config.max_error_rate:.1%}")
    if guardrails:
        report.update(decision="HOLD", reasons=guardrails)
    elif min(a["n"], b["n"]) < config.min_per_arm or elapsed_days < config.planned_days or not outcomes_mature:
        report.update(decision="WAIT", reasons=["계획 표본·기간·30분 결과 관찰 창 충족 전: 중간 효과는 설명용"])
    elif report["effect"]["low"] <= 0 or report["effect"]["difference"] < config.practical_lift:
        report.update(decision="INCONCLUSIVE", reasons=["양의 효과 근거 또는 사전 실용 개선 폭 부족. 동등하다는 뜻은 아님."])
    else:
        report.update(decision="REVIEW", reasons=["고정 시점 개선 근거·운영 기준 통과. 사람 검토 후 제한 배포 여부 결정."])
    return report


def peeking_demo(seed=12, repeats=500, looks=14, per_look=100):
    """Null-world simulation. Conventional daily p<.05 stopping is not a valid test."""
    rng = np.random.default_rng(seed)
    a = rng.binomial(per_look, .5, (repeats, looks)).cumsum(axis=1)
    b = rng.binomial(per_look, .5, (repeats, looks)).cumsum(axis=1)
    n = np.arange(1, looks+1)*per_look
    pooled = (a+b)/(2*n)
    se = np.sqrt(2*pooled*(1-pooled)/n)
    z = np.divide((b-a)/n, se, out=np.zeros_like(se), where=se>0)
    reject = np.abs(z) > NormalDist().inv_cdf(.975)
    return {"seed": seed, "repeats": repeats, "fixed_end_false_positive_rate": float(reject[:, -1].mean()),
            "any_day_false_positive_rate": float(reject.any(axis=1).mean()), "source": "null_simulation"}
