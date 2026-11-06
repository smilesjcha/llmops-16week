# 10주차 이미지·근거·실험 출처

확인일: 2026-11-06. 외부 도식은 개념 설명용이고, 실습 캡처는 직접 실행한 합성 MOCK 서비스다. 외부 제품을 사용해 전체 운영 환경을 구축했다고 표현하지 않는다.

## OpenTelemetry 공식 도식

OpenTelemetry Authors, [Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/), [Context propagation](https://opentelemetry.io/docs/concepts/context-propagation/). 사이트 소스의 [CC BY 4.0 라이선스](https://github.com/open-telemetry/opentelemetry.io/blob/main/LICENSE), [라이선스 원문](https://creativecommons.org/licenses/by/4.0/).

- `otel-waterfall.svg` 원본: [waterfall-trace.svg](https://raw.githubusercontent.com/open-telemetry/opentelemetry.io/main/static/img/waterfall-trace.svg)
- `otel-context.svg` 원본: [context-propagation-example.svg](https://raw.githubusercontent.com/open-telemetry/opentelemetry.io/main/content/en/docs/concepts/context-propagation/context-propagation-example.svg)
- 전체 PNG는 원본 SVG의 비율·내용을 유지한 고해상도 변환본. `*-detail.svg/png`는 텍스트 가독성을 위해 waterfall의 상단4행과 context 도식의 상단 요청을 확대 발췌한 것으로, 하단은 생략했고 전체 원본도 함께 보존했다. PPT에서는 PowerPoint의 native grayscale 효과로 회색조 표시하며 원본 이미지 바이트를 보존한다. 원본 그래픽의 요청·서비스·레이블을 임의 실측 수치로 대체하지 않았다.
- 28·30쪽에 출처·저자·라이선스·표시 변경을 표기했다. 이 그림은 실습 서비스의 성능 자료가 아니다.

## 실제 실행 캡처

`lab-release.png`, `lab-success.png`, `lab-trace.png`, `lab-timeout-trace.png`, `lab-signals.png`: `scripts/capture_week10_lab.mjs`로 자신이 생성한 임시 로컬 Uvicorn과 브라우저에서 캡처. 합성 질문만 입력, 사용자·학생 자료·API 키 없음. 요청·Trace ID는 임의 발급값이다. 캡처 후 자신이 생성한 브라우저와 서버를 종료한다.

## 실측 차트와 제한

`measurements.json`: Python3.11.14·단일 프로세스·실제 localhost TCP·MOCK 검색10ms/생성30ms 조건의 정상 요청1건과, HTTPX ASGITransport에서 동일 합성 입력4건씩 v1/v2를 비교한 결과. 날짜·단위·표본은 파일에 기록했다. 단일 정상 Trace의 부모/자식 기간은 포함 관계다. 코드에 정의한 고정 문자열 검사이며 모델 품질·GPU·분산 처리 성능으로 일반화하지 않는다. 원시 QA는 로컬 `output/validation/week10/`에 두고 공개 차트에는 필요한 집계만 사용한다.

## 장표별 추가 근거

- [Docker build best practices](https://docs.docker.com/build/building/best-practices/): 빌드 문맥·의존성·이미지 버전.
- [Docker run](https://docs.docker.com/engine/containers/run/): 이미지/컨테이너·포트·런타임 설정.
- [Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/): 생존·준비·초기화의 개념. 클러스터 실습 아님.
- [OpenTelemetry traces](https://opentelemetry.io/docs/concepts/signals/traces/): Trace·Span·관계.
- [W3C Trace Context](https://www.w3.org/TR/trace-context/): traceparent. 실습은 제한된00버전 예시이고 전체 표준 구현 아님.
- [Prometheus naming](https://prometheus.io/docs/practices/naming/), [histograms](https://prometheus.io/docs/practices/histograms/): 단위·라벨·누적 버킷·구간 집계.
- [Google SRE monitoring](https://sre.google/sre-book/monitoring-distributed-systems/): 사용자 영향·모니터링 질문. 임의 실습 임계값을 운영 SLO로 주장하지 않음.

Docker CLI는 존재하지만 검수 시 daemon이 꺼져 있어 이미지 빌드·컨테이너 기동은 미검증이다. 실제 모델·GPU·외부 수집 백엔드도 이번 검증 대상이 아니다. 해당 제한은 강의안·실습 안내에 표시했다.
