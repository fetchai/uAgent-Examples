FROM python:3.12-slim
ENV PATH="$PATH:/root/.local/bin"

RUN apt-get update && \
    apt-get install -y curl gcc && \
    curl -sSL https://install.python-poetry.org/ | python3 -

WORKDIR /app
ADD pyproject.toml poetry.lock /app/
RUN poetry install
ADD . /app
EXPOSE 8000

ENTRYPOINT ["poetry", "run"]
CMD ["python", "main.py"]