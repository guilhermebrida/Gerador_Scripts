FROM python:3.9

WORKDIR /api_copiloto

COPY pyproject.toml poetry.lock /api_copiloto/

RUN pip install poetry

RUN poetry install --no-root --no-dev

COPY . /api_copiloto

CMD ["poetry", "run", "python", "main.py"]

