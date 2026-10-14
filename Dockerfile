FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .
COPY data ./data
USER 65534:65534
CMD ["uvicorn", "eka.api:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
