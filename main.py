from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
from models import Book, Base

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic schema for book creation
class BookCreate(BaseModel):
    title: str
    author: str

# Pydantic schema for returning book data
class BookOut(BookCreate):
    id: int

    class Config:
        orm_mode = True

# Get all books
@app.get("/books", response_model=List[BookOut])
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books

# Add a new book
@app.post("/books", response_model=BookOut)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author=book.author)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
