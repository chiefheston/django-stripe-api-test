FROM python:3.14.1-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /django

RUN apt-get update -y && \
    apt-get install -y python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap

COPY ../pyproject.toml /django
COPY ../uv.lock /django

RUN pip install --upgrade pip
RUN pip install --no-cache-dir uv

RUN uv sync --frozen

COPY ./src ./src

CMD ["uv", "run", "python", "src/app/manage.py", "runserver", "0.0.0.0:8000"]
