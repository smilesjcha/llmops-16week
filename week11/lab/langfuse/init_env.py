"""Create per-machine credentials once, without printing secrets or overwriting them."""

import os
import secrets
from pathlib import Path


def initialize(directory=None):
    path = (Path(directory) if directory else Path(__file__).parent) / ".env"
    if path.exists():
        return path, False
    values = {
        "LANGFUSE_PORT": "3011",
        "LANGFUSE_BASE_URL": "http://localhost:3011",
        "LANGFUSE_PUBLIC_KEY": "pk-lf-" + secrets.token_hex(16),
        "LANGFUSE_SECRET_KEY": "sk-lf-" + secrets.token_hex(32),
        "LANGFUSE_LOGIN_EMAIL": "student@example.test",
        "LANGFUSE_LOGIN_PASSWORD": secrets.token_hex(16),
        **{
            key: secrets.token_hex(32)
            for key in [
                "POSTGRES_PASSWORD",
                "CLICKHOUSE_PASSWORD",
                "REDIS_AUTH",
                "MINIO_ROOT_PASSWORD",
                "NEXTAUTH_SECRET",
                "SALT",
                "ENCRYPTION_KEY",
            ]
        },
    }
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8") as file:
        file.write(
            "# Local credentials. Do not commit, share, or regenerate while keeping database volumes.\n"
        )
        file.write("\n".join(f"{key}={value}" for key, value in values.items()) + "\n")
    return path, True


if __name__ == "__main__":
    path, created = initialize()
    print("Created" if created else "Kept existing", path)
    print("Open this file in VS Code for LANGFUSE_LOGIN_EMAIL / LANGFUSE_LOGIN_PASSWORD.")
    print("Credentials are not printed. Existing files and Docker volumes are preserved.")
