FROM python:3.9
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry install
CMD ["fastapi", "run", "app.py"]
