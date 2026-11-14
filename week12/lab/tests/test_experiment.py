from dataclasses import replace
import pytest
from fastapi.testclient import TestClient
from scipy.stats import chi2
from week12.lab.experiment import DEFAULT, assign
from week12.lab.analysis import analyze, srm_test, difference_interval, sample_size, wilson, peeking_demo
from week12.lab.simulate import load_units
from week12.lab.service import create_app


def test_stable_assignment_and_version():
    assert {assign("u-repeat") for _ in range(20)} == {assign("u-repeat")}
    assert DEFAULT.version != replace(DEFAULT, max_p95_ms=2000).version
    with pytest.raises(ValueError):
        assign("student@example.com")


@pytest.mark.parametrize("a,b", [(1000,1000),(1200,800),(12,18)])
def test_srm_against_scipy(a,b):
    result=srm_test(a,b)
    assert result["p_value"] == pytest.approx(chi2.sf(result["chi2"],1))


def test_small_srm_is_not_claimed_valid():
    assert srm_test(1,1)["p_value"] is None


def test_interval_symmetry_and_boundaries():
    positive=difference_interval(50,100,70,100)
    negative=difference_interval(70,100,50,100)
    assert positive["low"]>0
    assert positive["low"] == pytest.approx(-negative["high"])
    assert wilson(0,100)[0] == pytest.approx(0)
    assert wilson(100,100)[1] == pytest.approx(1)
    assert sample_size(absolute_effect=.025)>sample_size(absolute_effect=.05)


@pytest.mark.parametrize("case,decision", [("healthy","REVIEW"),("slow","HOLD"),("srm","INVALID")])
def test_case_decisions(case,decision):
    r=analyze(load_units(case))
    assert r["decision"]==decision
    if case=="srm": assert r["effect"] is None


@pytest.mark.parametrize("mutation", ["duplicate","nan","negative","version","variant","outcome","source"])
def test_invalid_evidence_cannot_win(mutation):
    data=load_units("healthy")
    if mutation=="duplicate": data.loc[1,"visitor_id"]=data.loc[0,"visitor_id"]
    if mutation=="nan": data.loc[0,"latency_ms"]=float("nan")
    if mutation=="negative": data.loc[0,"latency_ms"]=-1
    if mutation=="version": data.loc[0,"config_version"]="changed"
    if mutation=="variant": data.loc[0,"variant"]="C"
    if mutation=="outcome": data.loc[0,["resolved","error"]]=[1,1]
    if mutation=="source": data.loc[0,"source"]="real_customer"
    assert analyze(data)["decision"]=="INVALID"


def test_stopping_contract():
    data=load_units("healthy")
    assert analyze(data,elapsed_days=2)["decision"]=="WAIT"
    assert analyze(data,outcomes_mature=False)["decision"]=="WAIT"
    assert analyze(data,elapsed_days=float("nan"))["decision"]=="INVALID"
    assert analyze(load_units("slow"),elapsed_days=2)["decision"]=="HOLD"


def test_null_peeking_demonstration():
    r=peeking_demo()
    assert r["any_day_false_positive_rate"]>r["fixed_end_false_positive_rate"]


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path/"lab.sqlite3")) as c:
        yield c


def payload(request_id="r-01",visitor_id="u-example",provider="template"):
    return dict(request_id=request_id,visitor_id=visitor_id,topic="exchange",provider=provider)


def test_real_routes_idempotency_feedback_and_metrics(client):
    first=client.post('/api/answer',json=payload()).json()
    assert first['variant']==assign('u-example') and first['model'] is None
    replay=client.post('/api/answer',json=payload()).json()
    assert replay['replayed'] and len(client.get('/api/events').json())==1
    assert client.post('/api/answer',json=payload(visitor_id='u-other')).status_code==409
    fb={'request_id':'r-01','resolved':True}
    assert client.post('/api/feedback',json=fb).status_code==200
    assert client.post('/api/feedback',json=fb).status_code==200
    assert client.post('/api/feedback',json={**fb,'resolved':False}).status_code==409
    assert 'w12_requests_total' in client.get('/metrics').text
    assert client.get('/api/summary').json()['decision']=='WAIT'


def test_failed_model_recorded_no_synthetic_fallback(tmp_path):
    def broken(*args): raise RuntimeError('model unavailable')
    with TestClient(create_app(tmp_path/'failure.sqlite3',generator=broken)) as c:
        assert c.post('/api/answer',json=payload(provider='ollama')).status_code==503
        row=c.get('/api/events').json()[0]
        assert row['status']=='error' and row['latency_ms']>=0
        assert c.post('/api/feedback',json={'request_id':'r-01','resolved':True}).status_code==409
        assert c.post('/api/answer',json=payload(provider='ollama')).status_code==503
        assert len(c.get('/api/events').json())==1


def test_rollback_and_first_user_unit(client):
    client.post('/api/answer',json=payload())
    client.post('/api/answer',json=payload('r-02'))
    assert client.get('/api/summary').json()['users']==1
    client.post('/api/control',json={'enabled':False})
    data=client.post('/api/answer',json=payload('r-03','u-next')).json()
    assert data['variant']=='A' and not data['experiment_enabled']
    assert client.get('/api/summary').json()['decision']=='INVALID'


def test_request_contract(client):
    assert client.post('/api/answer',json={**payload(),'visitor_id':'name@example.com'}).status_code==422
    assert client.post('/api/answer',json={**payload(),'variant':'B'}).status_code==422
    assert client.post('/api/feedback',json={'request_id':'missing','resolved':True}).status_code==404


def test_mixed_providers_are_not_an_experiment(tmp_path):
    def fake_for_contract_test(*args): return {'answer':'test fixture','provider':'ollama','model':'fixture'}
    with TestClient(create_app(tmp_path/'mixed.sqlite3',generator=fake_for_contract_test)) as c:
        c.post('/api/answer',json=payload())
        c.post('/api/answer',json=payload('r-02','u-two','ollama'))
        assert c.get('/api/summary').json()['decision']=='INVALID'


def test_pending_metrics_and_control_snapshot(tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Event
    entered, finish = Event(), Event()

    def delayed(*args):
        entered.set()
        assert finish.wait(5)
        return {'answer': 'contract fixture', 'provider': 'ollama'}

    with TestClient(create_app(tmp_path/'pending.sqlite3', generator=delayed)) as c:
        with ThreadPoolExecutor() as pool:
            response = pool.submit(c.post, '/api/answer', json=payload(provider='ollama'))
            try:
                assert entered.wait(5)
                variant = assign('u-example')
                pending = c.get('/metrics').text
                assert '# TYPE w12_requests_by_status gauge' in pending
                assert f'w12_requests_total{{variant="{variant}"}} 1' in pending
                assert f'w12_requests_by_status{{variant="{variant}",status="pending"}} 1' in pending
                assert c.post('/api/answer', json=payload(provider='ollama')).status_code == 409
                c.post('/api/control', json={'enabled': False})
            finally:
                finish.set()
            result = response.result().json()
            assert result['experiment_enabled'] is True
            complete = c.get('/metrics').text
            assert f'w12_requests_total{{variant="{variant}"}} 1' in complete
            assert f'w12_requests_by_status{{variant="{variant}",status="pending"}} 0' in complete
