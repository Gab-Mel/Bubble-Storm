from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    questions = relationship("QuestionModel", back_populates="document", lazy="joined")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    document = relationship("DocumentModel", back_populates="questions")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
