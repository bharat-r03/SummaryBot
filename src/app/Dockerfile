FROM python:3.11.9

WORKDIR /

RUN python -m pip install uv

ADD . /app

WORKDIR /app

RUN uv sync --locked

RUN uv run --active spacy download en_core_web_sm

CMD [ "uv", "run", "fastapi", "run", "main.py" ]