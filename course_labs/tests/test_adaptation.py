import numpy as np
import pytest
from course_labs.adaptation import (examples, audit, split_groups, leakage, rank_approximation,
                                    dpo_loss, toy_preference_training, preference_audit,
                                    proposal_check, proposal_html)


def test_data_audit_and_group_split():
    data = examples()
    assert not audit(data)["issues"]
    split = split_groups(data)
    assert [len(split[k]) for k in ("train", "dev", "test")] == [32, 8, 8]
    assert split == split_groups(data)
    assert len({r["id"] for rows in split.values() for r in rows}) == len(data)
    assert not leakage(split)
    split["test"].append(split["train"][0])
    assert leakage(split)


def test_invalid_data():
    data = examples()
    data += [dict(data[0])]
    data[1]["response"] = "not json"
    data[2]["synthetic"] = False
    result = audit(data)
    assert result["duplicate_content"] == 1
    assert result["duplicate_ids"]
    assert {i["kind"] for i in result["issues"]} == {"invalid_output", "permission_review"}
    with pytest.raises(ValueError):
        split_groups(data[:2])


def test_low_rank():
    matrix = np.random.default_rng(42).normal(size=(12, 8))
    errors = [rank_approximation(matrix, r)["relative_error"] for r in (1, 2, 4, 8)]
    assert all(a >= b for a, b in zip(errors, errors[1:]))
    assert errors[-1] < 1e-12
    assert rank_approximation(matrix, 2)["factor_params"] == 40
    assert rank_approximation(np.zeros((3, 3)), 1)["relative_error"] == 0
    with pytest.raises(ValueError):
        rank_approximation(matrix, 9)


def test_dpo_stability_and_gradient():
    assert dpo_loss(-3, -3, -3, -3) == pytest.approx(np.log(2))
    assert dpo_loss(-2, -5, -3, -3) < dpo_loss(-5, -2, -3, -3)
    assert np.isfinite(dpo_loss(-10000, 0, 0, 0))
    with pytest.raises(ValueError):
        dpo_loss(-3, -3, -3, -3, beta=0)
    result = toy_preference_training()
    assert result[-1]["loss"] < result[0]["loss"]
    assert result[-1]["chosen_probability"] > .5
    eps, theta, beta = 1e-5, .3, .5
    numeric = (np.logaddexp(0, -beta*(theta+eps)) - np.logaddexp(0, -beta*(theta-eps))) / (2*eps)
    assert numeric == pytest.approx(-beta/(1+np.exp(beta*theta)))


def test_preference_and_proposal_boundaries():
    assert preference_audit([{"prompt": "x", "chosen": "a", "rejected": "b", "reason": "근거"}]) == []
    assert preference_audit([{"prompt": "x", "chosen": "a", "rejected": "a"}])
    assert "evaluation" in proposal_check({})
    html = proposal_html({"problem": "<script>alert(1)</script>"})
    assert "&lt;script&gt;" in html and "<script>" not in html
