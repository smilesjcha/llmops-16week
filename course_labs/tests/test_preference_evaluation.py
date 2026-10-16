import numpy as np
import pytest
from course_labs.preference_evaluation import (
    DIMENSIONS, evaluation_fixtures, fixture_summary, fixture_verdict, sequence_logprob,
)


def test_sequence_logprob():
    assert sequence_logprob([.8,.5,.2]) == pytest.approx(np.log(.8*.5*.2))
    assert sequence_logprob([1.]) == 0
    assert np.isfinite(sequence_logprob([1e-200,1e-200]))


@pytest.mark.parametrize("values", [[], [0.], [-.1], [1.1], [float('nan')], [[.5,.6]]])
def test_invalid_probabilities(values):
    with pytest.raises(ValueError):
        sequence_logprob(values)


def test_fixture_contract():
    result = fixture_summary(evaluation_fixtures())
    assert result['counts'] == {'candidate':4,'baseline':4,'tie':3,'review':1}
    assert result['rates']['candidate']['format'] == pytest.approx(11/12)
    assert result['rates']['baseline']['format'] == pytest.approx(9/12)
    assert result['rates']['candidate']['evidence'] == pytest.approx(9/12)
    assert result['rates']['baseline']['evidence'] == pytest.approx(10/12)


def test_invalid_flags_and_tradeoff():
    flags = dict.fromkeys(DIMENSIONS, 1)
    with pytest.raises(ValueError):
        fixture_verdict({}, flags)
    with pytest.raises(ValueError):
        fixture_verdict(dict(flags, useful=2), flags)
    assert fixture_verdict(dict(flags,useful=0),dict(flags,no_excess_refusal=0)) == 'review'
    with pytest.raises(ValueError):
        fixture_summary([])
    rows = evaluation_fixtures()
    rows[0]['synthetic'] = False
    with pytest.raises(ValueError):
        fixture_summary(rows)
