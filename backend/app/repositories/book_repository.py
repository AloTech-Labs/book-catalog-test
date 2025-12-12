"""Book repository for data access operations"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models import Book
from .base_repository import BaseRepository


class BookRepository(BaseRepository[Book]):
    """Repository for Book entity data access.
    
    Extends BaseRepository with book-specific query methods.
    """
    
    def __init__(self, db: Session):
        """Initialize the book repository.
        
        Args:
            db: The database session.
        """
        super().__init__(Book, db)
    
    def get_all(self) -> List[Book]:
        """Retrieve all books with related entities eagerly loaded.
        
        Returns:
            List of all books with authors, genre, and publisher.
        """
        return (
            self.db.query(Book)
            .options(
                joinedload(Book.authors),
                joinedload(Book.genre),
                joinedload(Book.publisher)
            )
            .all()
        )
    
    def get_by_id(self, id: int) -> Optional[Book]:
        """Retrieve a book by ID with related entities eagerly loaded.
        
        Args:
            id: The book's primary key.
            
        Returns:
            The book if found, None otherwise.
        """
        return (
            self.db.query(Book)
            .options(
                joinedload(Book.authors),
                joinedload(Book.genre),
                joinedload(Book.publisher)
            )
            .filter(Book.id == id)
            .first()
        )
    
    def get_by_author(self, author_id: int) -> List[Book]:
        """Retrieve all books by a specific author.
        
        Args:
            author_id: The author's primary key.
            
        Returns:
            List of books by the specified author.
        """
        return (
            self.db.query(Book)
            .options(
                joinedload(Book.authors),
                joinedload(Book.genre),
                joinedload(Book.publisher)
            )
            .join(Book.authors)
            .filter(Book.authors.any(id=author_id))
            .all()
        )
    
    def get_by_genre(self, genre_id: int) -> List[Book]:
        """Retrieve all books in a specific genre.
        
        Args:
            genre_id: The genre's primary key.
            
        Returns:
            List of books in the specified genre.
        """
        return (
            self.db.query(Book)
            .options(
                joinedload(Book.authors),
                joinedload(Book.genre),
                joinedload(Book.publisher)
            )
            .filter(Book.genre_id == genre_id)
            .all()
        )
    
    def get_by_publisher(self, publisher_id: int) -> List[Book]:
        """Retrieve all books by a specific publisher.
        
        Args:
            publisher_id: The publisher's primary key.
            
        Returns:
            List of books from the specified publisher.
        """
        return (
            self.db.query(Book)
            .options(
                joinedload(Book.authors),
                joinedload(Book.genre),
                joinedload(Book.publisher)
            )
            .filter(Book.publisher_id == publisher_id)
            .all()
        )
    
    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        """Find a book by its ISBN.
        
        Args:
            isbn: The book's ISBN to search for.
            
        Returns:
            The book if found, None otherwise.
        """
        return (
            self.db.query(Book)
            .filter(Book.isbn == isbn)
            .first()
        )
    
    def count_by_genre(self, genre_id: int) -> int:
        """Count books in a specific genre.
        
        Args:
            genre_id: The genre's primary key.
            
        Returns:
            Number of books in the genre.
        """
        return (
            self.db.query(Book)
            .filter(Book.genre_id == genre_id)
            .count()
        )
    
    def count_by_publisher(self, publisher_id: int) -> int:
        """Count books from a specific publisher.
        
        Args:
            publisher_id: The publisher's primary key.
            
        Returns:
            Number of books from the publisher.
        """
        return (
            self.db.query(Book)
            .filter(Book.publisher_id == publisher_id)
            .count()
        )
