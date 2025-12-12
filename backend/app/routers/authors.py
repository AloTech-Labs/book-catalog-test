"""Author API endpoints"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import AuthorCreate, AuthorUpdate, AuthorSummary, AuthorWithBooks
from ..services import AuthorService


router = APIRouter(prefix="/authors", tags=["Authors"])


def get_author_service(db: Session = Depends(get_db)) -> AuthorService:
    """Dependency injection for AuthorService."""
    return AuthorService(db)


@router.get("", response_model=List[AuthorSummary])
def get_authors(service: AuthorService = Depends(get_author_service)):
    """Get list of all authors.
    
    Returns a list of all authors with summary information.
    """
    return service.get_all_authors()


@router.post("", response_model=AuthorWithBooks, status_code=201)
def create_author(
    author: AuthorCreate,
    service: AuthorService = Depends(get_author_service)
):
    """Create a new author.
    
    Args:
        author: The author data to create.
        
    Returns:
        The newly created author with their books.
    """
    return service.create_author(author)


@router.get("/{author_id}", response_model=AuthorWithBooks)
def get_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service)
):
    """Get a specific author by ID with their books.
    
    Args:
        author_id: The author's primary key.
        
    Returns:
        The author with their associated books.
    """
    return service.get_author_by_id(author_id)


@router.put("/{author_id}", response_model=AuthorWithBooks)
def update_author(
    author_id: int,
    author: AuthorUpdate,
    service: AuthorService = Depends(get_author_service)
):
    """Update an existing author.
    
    Args:
        author_id: The author's primary key.
        author: The updated author data.
        
    Returns:
        The updated author with their books.
    """
    return service.update_author(author_id, author)


@router.delete("/{author_id}", status_code=204)
def delete_author(
    author_id: int,
    service: AuthorService = Depends(get_author_service)
):
    """Delete an author.
    
    Fails if the author has associated books.
    
    Args:
        author_id: The author's primary key.
    """
    service.delete_author(author_id)
    return None
