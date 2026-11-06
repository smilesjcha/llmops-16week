# Optional path. Build context is week10/lab, not the repository root.
# Pin a reviewed digest for operational release; this course tag is not immutable.
FROM python:3.11.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-runtime.txt /app/requirements-runtime.txt
RUN python -m pip install --no-cache-dir -r requirements-runtime.txt
RUN mkdir -p /app/week10/lab
COPY __init__.py app.py config.py telemetry.py experiments.py index.html /app/week10/lab/
USER 10001
EXPOSE 8010
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8010/health/ready',timeout=2)"
CMD ["python", "-m", "uvicorn", "week10.lab.app:app", "--host", "0.0.0.0", "--port", "8010", "--no-access-log"]
