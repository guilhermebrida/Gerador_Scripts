FROM python:3.9

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . .

RUN pip install poetry

RUN poetry install --no-root --no-dev

EXPOSE 5000

CMD ["poetry", "run", "python", "api_copiloto/main.py"]


