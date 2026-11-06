"""Validated startup configuration and non-secret release identity."""

from dataclasses import dataclass
import hashlib
import json
import math
import os


@dataclass(frozen=True)
class Settings:
    release: str = "v1"
    timeout_s: float = 0.25
    capacity: int = 2
    emit_logs: bool = False

    def __post_init__(self):
        if self.release not in {"v1", "v2"}:
            raise ValueError("WEEK10_RELEASE must be v1 or v2")
        if type(self.capacity) is not int or not 1 <= self.capacity <= 8:
            raise ValueError("capacity must be an integer from 1 to 8")
        if (
            type(self.timeout_s) not in {float, int}
            or not math.isfinite(self.timeout_s)
            or not 0.05 <= self.timeout_s <= 2
        ):
            raise ValueError("timeout_s must be finite, from 0.05 to 2")
        if type(self.emit_logs) is not bool:
            raise ValueError("emit_logs must be bool")

    @classmethod
    def from_env(cls):
        logs = os.getenv("WEEK10_LOG_STDOUT", "1")
        if logs not in {"0", "1"}:
            raise ValueError("WEEK10_LOG_STDOUT must be 0 or 1")
        return cls(
            release=os.getenv("WEEK10_RELEASE", "v1"),
            timeout_s=float(os.getenv("WEEK10_TIMEOUT_S", "0.25")),
            capacity=int(os.getenv("WEEK10_CAPACITY", "2")),
            emit_logs=logs == "1",
        )

    def manifest(self):
        public = {
            "release": self.release,
            "model": "mock-fixed-v1",
            "prompt": self.release,
            "dataset": "synthetic-docs-v1",
            "schema": "assist-v1",
            "timeout_s": self.timeout_s,
            "capacity": self.capacity,
        }
        # A configuration fingerprint is NOT a secret hash or a source commit.
        public["config_id"] = hashlib.sha256(
            json.dumps(public, sort_keys=True).encode()
        ).hexdigest()[:12]
        return public
