import os

from database import paper_collection
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from llm_feats import get_summary
from pydantic import BaseModel
from pymongo.errors import DuplicateKeyError


class PaperName(BaseModel):
    name: str


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
    return [doc["name"] for doc in list(paper_collection.find())]


@app.post("/uploadpdf")
def upload_file(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    # Save the reference in MongoDB
    paper_doc = {"name": file.filename, "file_path": file_location}
    summary = get_summary(paper_doc)
    paper_doc["summary"] = summary
    try:
        result_id = paper_collection.insert_one(paper_doc)
        result_id = result_id.inserted_id
    except DuplicateKeyError:
        result_id = 0
        print("A paper with this title already exists.")

    return {"filename": file.filename, "id": str(result_id)}


@app.post("/deletepdf")
def delete_pdf(paper: PaperName):
    file_name = paper.name
    file_location = f"files/{file_name}"

    if os.path.exists(file_location):
        os.remove(file_location)
        file_deletion = "File is found and deleted"
    else:
        print("The file does not exist")
        file_deletion = "File is not found"

    result = paper_collection.delete_one({"name": file_name})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"File not found in database. {file_deletion}.",
        )

    return {"message": f"File deleted successfully. {file_deletion}"}
