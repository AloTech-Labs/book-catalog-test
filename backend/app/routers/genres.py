"""Genre API endpoints.

This module defines thin REST API endpoints for Genre operations.
Business logic is delegated to the GenreService.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import GenreCreate, GenreUpdate, GenreSummary, GenreResponse
from ..services import GenreService


router = APIRouter(prefix="/genres", tags=["Genres"])


def get_genre_service(db: Session = Depends(get_db)) -> GenreService:
    """Dependency injection for GenreService."""
    return GenreService(db)


@router.get("", response_model=List[GenreSummary])
def get_genres(service: GenreService = Depends(get_genre_service)):
    """Get list of all genres sorted by name.
    
    Returns a list of all genres with summary information.
    """
    return service.get_all_genres()


@router.post("", response_model=GenreResponse, status_code=201)
def create_genre(
    genre: GenreCreate,
    service: GenreService = Depends(get_genre_service)
):
    """Create a new genre.
    
    Args:
        genre: The genre data to create.
        
    Returns:
        The newly created genre.
    """
    return service.create_genre(genre)


@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service)
):
    """Get a specific genre by ID.
    
    Args:
        genre_id: The genre's primary key.
        
    Returns:
        The genre details.
    """
    return service.get_genre_by_id(genre_id)


@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int,
    genre: GenreUpdate,
    service: GenreService = Depends(get_genre_service)
):
    """Update an existing genre.
    
    Args:
        genre_id: The genre's primary key.
        genre: The updated genre data.
        
    Returns:
        The updated genre.
    """
    return service.update_genre(genre_id, genre)


@router.delete("/{genre_id}", status_code=204)
def delete_genre(
    genre_id: int,
    service: GenreService = Depends(get_genre_service)
):
    """Delete a genre.
    
    Fails if the genre has associated books.
    
    Args:
        genre_id: The genre's primary key.
    """
    service.delete_genre(genre_id)
    return None
