
from fastapi import FastAPI, Depends, HTTPException
from database import load_database, load_session
from nlp import generate_questions
from models import DocumentModel, QuestionModel
from pydantic import BaseModel
from sqlalchemy.orm import Session, joinedload
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    load_database()

class CreateDocumentModel(BaseModel):
    title: str
    content: str

@app.post("/documents", status_code=201)
async def create_document(document: CreateDocumentModel = None, db: Session = Depends(load_session)):
    document = DocumentModel(title=document.title, content=document.content)
    db.add(document)
    db.commit()

    return {"id": document.id}


@app.get("/documents")
async def get_documents(db: Session = Depends(load_session)):
    return db.query(DocumentModel).all()

@app.get("/documents/{document_id}")
async def get_document(document_id: int, db: Session = Depends(load_session)):
    document = db.query(DocumentModel).filter(DocumentModel.id == document_id).options(
        joinedload(DocumentModel.questions)
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document

@app.get("/documents/{document_id}/questions")
async def get_questions(document_id: int, db: Session = Depends(load_session)):
    document = db.query(DocumentModel).get(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    text = document.content
    questions = generate_questions(text, 10)

    return questions

class CreateQuestionModel(BaseModel):
    text: str

@app.post("/documents/{document_id}/questions", status_code=201)
async def create_question(document_id: int, question: CreateQuestionModel, db: Session = Depends(load_session)):
    document = db.query(DocumentModel).get(document_id)

    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    question = QuestionModel(text=question.text, document_id=document_id)
    db.add(question)
    db.commit()

    return {"id": question.id}
