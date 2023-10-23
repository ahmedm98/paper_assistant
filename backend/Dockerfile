# backend/Dockerfile

FROM python:3.9-slim

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN python -c 'from sentence_transformers import SentenceTransformer; SentenceTransformer("sentence-transformers/all-mpnet-base-v2")'

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000" ]