"""Author router with CRUD operations."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..database import get_db
from ..models import Author, Book
from ..schemas import (
    AuthorCreate,
    AuthorUpdate,
    AuthorSummary,
    AuthorWithBooks,
)

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("", response_model=list[AuthorSummary])
def get_authors(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
    surname: Optional[str] = Query(None, description="Filter by surname"),
    sort_by: Optional[str] = Query("surname", description="Sort field"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
):
    """Get list of all authors with optional filtering and sorting."""
    query = db.query(Author)

    # Apply filters
    if name:
        query = query.filter(Author.name.ilike(f"%{name}%"))
    if surname:
        query = query.filter(Author.surname.ilike(f"%{surname}%"))

    # Apply sorting
    sort_column = getattr(Author, sort_by, Author.surname)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    return query.all()


@router.post("", response_model=AuthorWithBooks, status_code=201)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    """Create a new author."""
    db_author = Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=AuthorWithBooks)
def get_author(author_id: int, db: Session = Depends(get_db)):
    """Get a specific author by ID with their books."""
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.put("/{author_id}", response_model=AuthorWithBooks)
def update_author(
    author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)
):
    """Update an existing author."""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    for key, value in author.model_dump().items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)
    return db_author


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    """Delete an author. Fails if author has associated books."""
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if author has associated books
    if db_author.books:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete author with associated books. Remove books first.",
        )

    db.delete(db_author)
    db.commit()
    return None
