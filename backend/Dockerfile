# backend/Dockerfile

FROM python:3.9-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app


RUN pip install -r requirements.txt


COPY . /app

EXPOSE 8000

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000" ]