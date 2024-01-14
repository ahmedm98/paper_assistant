import logging
import os

from chroma_database import collection
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from llm_feats import answer_question_rag, get_embedding, get_summary
from pydantic import BaseModel
from typing import Optional
from utils import delete_document

logging.basicConfig(level=logging.INFO)


class Paper(BaseModel):
    _id: str
    name: str
    file_path: str
    summary: str


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/get_papers")
def get_papers():
    current_collection = collection.get()
    papers = []
    for i in range(len(current_collection["ids"])):
        papers.append(
            Paper(
                _id=current_collection["ids"][i],
                name=current_collection["metadatas"][i]["name"].replace(
                    ".pdf", ""
                ),
                file_path=current_collection["metadatas"][i]["file_path"],
                summary=current_collection["documents"][i],
            )
        )
    print(papers)
    return papers


@app.post("/uploadpdf")
def upload_file(file: UploadFile = File(...)):
    directory = f"files/{file.filename.replace('.pdf','')}"
    file_location = directory + f"/{file.filename}"

    # Check if the directory already exists
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)

    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # produce and save a summary
    summary = get_summary(file.filename.replace(".pdf", ""))
    paper_doc = {
        "name": file.filename.replace(".pdf", ""),
        "file_path": file_location,
        "summary": summary,
    }

    # Save the paper in db
    try:
        collection.add(
            ids=[paper_doc["name"]],
            metadatas=[
                {
                    "name": paper_doc["name"],
                    "file_path": paper_doc["file_path"],
                }
            ],
            documents=[paper_doc["summary"]],
        )
        result_id = 1
    except ValueError:
        result_id = 0
        logging.error("The paper was not added to the database")

    return {"filename": file.filename, "id": str(result_id)}


@app.post("/deletepdf")
def delete_pdf(paper: Paper):
    file_name = paper.name
    file_deletion = delete_document(file_name)
    try:
        logging.info(f"deleting {file_name}")
        collection.delete([file_name])
        db_result = 1
    except ValueError:
        db_result = 0

    if db_result == 0:
        raise HTTPException(
            status_code=404,
            detail=f"File not found in database. {file_deletion}.",
        )
    logging.info(str(db_result) + " -----" + file_deletion)
    return {
        "message": (
            f"{db_result} Files with name {file_name} deleted"
            f" successfully. {file_deletion}"
        )
    }


class SearchPaper(BaseModel):
    text: str
    k: Optional[int] = 2


@app.post("/get_top_k")
def get_top_k(input: SearchPaper):
    text = input.text
    k = input.k
    input_embedding = get_embedding(text)
    results = chroma_vector_search(input_embedding, k)
    papers = []

    for i in range(len(results["ids"][0])):
        papers.append(
            Paper(
                _id=results["ids"][0][i],
                name=results["metadatas"][0][i]["name"],
                file_path=results["metadatas"][0][i]["file_path"],
                summary=results["documents"][0][i],
            )
        )
    return papers


class User_Question(BaseModel):
    text: str


@app.post("/get_rag")
def get_rag(input_text: User_Question):
    text = input_text.text
    input_embedding = get_embedding(text)
    top_documents = chroma_vector_search(input_embedding, 3)
    response = answer_question_rag(question=text, context=top_documents)
    return response


def chroma_vector_search(input_embedding: list, k: int):
    return collection.query(
        query_embeddings=[input_embedding],
        n_results=k,
    )
