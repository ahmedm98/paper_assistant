from chroma_database import collection
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from llm_feats import get_summary
from pydantic import BaseModel
from utils import delete_document


class Paper(BaseModel):
    _id: str
    name: str
    file_path: str
    summary: str


app = FastAPI()


# remove later. Just for development.
# Not needed when deploying the frontend and backend on docker containers.
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
                name=current_collection["metadatas"][i]["name"],
                file_path=current_collection["metadatas"][i]["file_path"],
                summary=current_collection["documents"][i],
            )
        )

    return papers


@app.post("/uploadpdf")
def upload_file(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # produce and save a summary
    summary = get_summary(file.filename)
    paper_doc = {
        "name": file.filename,
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
        print("The paper was not added to the database")

    return {"filename": file.filename, "id": str(result_id)}


@app.post("/deletepdf")
def delete_pdf(paper: Paper):
    file_name = paper.name
    file_deletion = delete_document(file_name)
    try:
        collection.delete([file_name])
        db_result = 1
    except ValueError:
        db_result = 0

    if db_result == 0:
        raise HTTPException(
            status_code=404,
            detail=f"File not found in database. {file_deletion}.",
        )
    print(db_result, file_deletion)
    return {
        "message": (
            f"{db_result} Files with name {file_name} deleted"
            f" successfully. {file_deletion}"
        )
    }
