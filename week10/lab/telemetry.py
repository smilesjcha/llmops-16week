"""Small in-memory teaching instrument, NOT an OpenTelemetry SDK/exporter."""

from collections import Counter, deque
from contextlib import contextmanager
from contextvars import ContextVar
from datetime import datetime, timezone
import json
import re
import secrets
import time

TRACE = ContextVar("week10_trace", default=None)
PARENT = ContextVar("week10_parent", default=None)
ORIGIN = ContextVar("week10_origin", default=None)
TRACEPARENT = re.compile(r"00-([0-9a-f]{32})-([0-9a-f]{16})-(0[01])\Z")
BUCKETS = (0.05, 0.1, 0.25, 0.5, 1.0)


def trace_context(value: str | None):
    """Educational version-00 subset. Invalid/unsupported contexts start a new trace."""
    m = TRACEPARENT.fullmatch(value or "")
    if m and int(m[1], 16) and int(m[2], 16):
        return m[1], m[2]
    return secrets.token_hex(16), None


class Telemetry:
    def __init__(self, manifest, *, emit_logs=False):
        self.manifest = manifest
        self.instance_id = secrets.token_hex(8)
        self.emit_logs = emit_logs
        self.logs = deque(maxlen=200)
        self.spans = deque(maxlen=800)
        self.counts = Counter()
        self.buckets = Counter()
        self.duration_sum = 0.0
        self.total = 0
        self.active = 0

    @contextmanager
    def span(self, name):
        if name not in {"assist", "retrieve", "generate", "format"}:
            raise ValueError("span name must come from a bounded vocabulary")
        started = time.perf_counter()
        parent = PARENT.get()
        sid = secrets.token_hex(8)
        token = PARENT.set(sid)
        status = "OK"
        try:
            yield sid
        except BaseException:
            status = "ERROR"
            raise
        finally:
            self.spans.append(
                {
                    "trace_id": TRACE.get(),
                    "span_id": sid,
                    "parent_id": parent,
                    "name": name,
                    "offset_ms": round((started - ORIGIN.get()) * 1000, 3),
                    "duration_ms": round((time.perf_counter() - started) * 1000, 3),
                    "status": status,
                    "release": self.manifest["release"],
                }
            )
            PARENT.reset(token)

    def finish(self, *, request_id, status, started):
        elapsed = max(0, time.perf_counter() - started)
        # Only /api/v1/assist is instrumented: health/scrape/UI do not pollute the denominator.
        self.counts[status] += 1
        self.total += 1
        self.duration_sum += elapsed
        for bound in BUCKETS:
            if elapsed <= bound:
                self.buckets[bound] += 1
        record = {
            "event": "request_completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "trace_id": TRACE.get(),
            "route": "/api/v1/assist",
            "status": status,
            "duration_ms": round(elapsed * 1000, 3),
            "release": self.manifest["release"],
            "config_id": self.manifest["config_id"],
        }
        # No raw message, answer, exception text, IP, headers, or user identity.
        self.logs.append(record)
        if self.emit_logs:
            print(json.dumps(record, ensure_ascii=False), flush=True)

    def snapshot(self):
        return {
            "release": self.manifest,
            "instance_id": self.instance_id,
            "total": self.total,
            "active": self.active,
            "status_counts": dict(self.counts),
            "logs": list(self.logs),
            "spans": list(self.spans),
            "retention": {"logs": 200, "spans": 800},
            "scope": "single process; synthetic; not OTLP",
        }

    def prometheus(self):
        lines = [
            "# HELP lab_assist_requests_total Completed assist requests by HTTP status.",
            "# TYPE lab_assist_requests_total counter",
        ]
        for status, count in sorted(self.counts.items()):
            lines.append(f'lab_assist_requests_total{{status="{status}"}} {count}')
        lines += [
            "# HELP lab_assist_duration_seconds All completed assist durations, including errors.",
            "# TYPE lab_assist_duration_seconds histogram",
        ]
        for bound in BUCKETS:
            lines.append(
                f'lab_assist_duration_seconds_bucket{{le="{bound:g}"}} {self.buckets[bound]}'
            )
        lines += [
            f'lab_assist_duration_seconds_bucket{{le="+Inf"}} {self.total}',
            f"lab_assist_duration_seconds_sum {self.duration_sum:.9f}",
            f"lab_assist_duration_seconds_count {self.total}",
            "# HELP lab_assist_active In-flight admitted assist requests.",
            "# TYPE lab_assist_active gauge",
            f"lab_assist_active {self.active}",
        ]
        return "\n".join(lines) + "\n"
