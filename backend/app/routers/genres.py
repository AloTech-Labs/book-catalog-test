"""Genre router with CRUD operations."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..database import get_db
from ..models import Genre
from ..schemas import GenreCreate, GenreUpdate, GenreSummary, GenreResponse

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=list[GenreSummary])
def get_genres(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
    sort_by: Optional[str] = Query("name", description="Sort field"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
):
    """Get list of all genres with optional filtering and sorting."""
    query = db.query(Genre)

    # Apply filters
    if name:
        query = query.filter(Genre.name.ilike(f"%{name}%"))

    # Apply sorting
    sort_column = getattr(Genre, sort_by, Genre.name)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    return query.all()


@router.post("", response_model=GenreResponse, status_code=201)
def create_genre(genre: GenreCreate, db: Session = Depends(get_db)):
    """Create a new genre."""
    db_genre = Genre(**genre.model_dump())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    """Get a specific genre by ID."""
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(genre_id: int, genre: GenreUpdate, db: Session = Depends(get_db)):
    """Update an existing genre."""
    db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    for key, value in genre.model_dump().items():
        setattr(db_genre, key, value)

    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.delete("/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    """Delete a genre."""
    db_genre = db.query(Genre).filter(Genre.id == genre_id).first()
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")

    db.delete(db_genre)
    db.commit()
    return None
