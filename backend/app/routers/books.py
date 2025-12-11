"""Book API endpoints.

This module defines thin REST API endpoints for Book operations.
Business logic is delegated to the BookService.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import BookCreate, BookUpdate, BookSummary, BookResponse
from ..services import BookService


router = APIRouter(prefix="/books", tags=["Books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Dependency injection for BookService."""
    return BookService(db)


@router.get("", response_model=List[BookSummary])
def get_books(service: BookService = Depends(get_book_service)):
    """Get list of all books.
    
    Returns a list of all books with summary information.
    """
    return service.get_all_books()


@router.post("", response_model=BookResponse, status_code=201)
def create_book(
    book: BookCreate,
    service: BookService = Depends(get_book_service)
):
    """Create a new book.
    
    Args:
        book: The book data to create.
        
    Returns:
        The newly created book with all details.
    """
    return service.create_book(book)


@router.get("/{book_id}", response_model=BookResponse)
def get_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """Get a specific book by ID.
    
    Args:
        book_id: The book's primary key.
        
    Returns:
        The book with all related information.
    """
    return service.get_book_by_id(book_id)


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    service: BookService = Depends(get_book_service)
):
    """Update an existing book.
    
    Args:
        book_id: The book's primary key.
        book: The updated book data.
        
    Returns:
        The updated book with all details.
    """
    return service.update_book(book_id, book)


@router.delete("/{book_id}", status_code=204)
def delete_book(
    book_id: int,
    service: BookService = Depends(get_book_service)
):
    """Delete a book.
    
    Args:
        book_id: The book's primary key.
    """
    service.delete_book(book_id)
    return None
