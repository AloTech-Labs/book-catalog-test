"""Book router with CRUD operations."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..database import get_db
from ..models import Book, Author
from ..schemas import BookCreate, BookUpdate, BookSummary, BookResponse

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("", response_model=list[BookSummary])
def get_books(
    db: Session = Depends(get_db),
    title: Optional[str] = Query(None, description="Filter by title"),
    genre_id: Optional[int] = Query(None, description="Filter by genre"),
    publisher_id: Optional[int] = Query(None, description="Filter by publisher"),
    author_id: Optional[int] = Query(None, description="Filter by author"),
    sort_by: Optional[str] = Query("title", description="Sort field"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
):
    """Get list of all books with optional filtering and sorting."""
    query = db.query(Book)

    # Apply filters
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if genre_id:
        query = query.filter(Book.genre_id == genre_id)
    if publisher_id:
        query = query.filter(Book.publisher_id == publisher_id)
    if author_id:
        query = query.join(Book.authors).filter(Author.id == author_id)

    # Apply sorting
    sort_column = getattr(Book, sort_by, Book.title)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    return query.all()


@router.post("", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """Create a new book."""
    # Extract author_ids and create book without them
    author_ids = book.author_ids
    book_data = book.model_dump(exclude={"author_ids"})
    
    db_book = Book(**book_data)

    # Add authors
    if author_ids:
        authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
        if len(authors) != len(author_ids):
            raise HTTPException(status_code=400, detail="One or more authors not found")
        db_book.authors = authors

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Get a specific book by ID."""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    """Update an existing book."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Extract author_ids
    author_ids = book.author_ids
    book_data = book.model_dump(exclude={"author_ids"})

    for key, value in book_data.items():
        setattr(db_book, key, value)

    # Update authors
    if author_ids is not None:
        authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
        if len(authors) != len(author_ids):
            raise HTTPException(status_code=400, detail="One or more authors not found")
        db_book.authors = authors

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Delete a book."""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(db_book)
    db.commit()
    return None
