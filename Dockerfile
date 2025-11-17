FROM python:3.11.14
LABEL authors="amandakershaw"

#RUN pip install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" ./

RUN uv sync --locked

COPY "predict.py" "model.bin" ./

EXPOSE 9696

ENTRYPOINT ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]