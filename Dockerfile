FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install aiogram sqlalchemy psycopg2-binary

CMD ["python", "main.py"]