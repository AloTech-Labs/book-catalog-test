"""Book service for business logic operations"""

from typing import List
from sqlalchemy.orm import Session

from app.models import Book, Author
from app.schemas import BookCreate, BookUpdate
from app.repositories import BookRepository, AuthorRepository, GenreRepository, PublisherRepository
from app.core.exceptions import NotFoundException, ValidationException


class BookService:
    """Service class for Book business logic"""
    
    def __init__(self, db: Session):
        """Initialize the book service.
        
        Args:
            db: The database session.
        """
        self.db = db
        self.repository = BookRepository(db)
        self.author_repository = AuthorRepository(db)
        self.genre_repository = GenreRepository(db)
        self.publisher_repository = PublisherRepository(db)
    
    def get_all_books(self) -> List[Book]:
        """Retrieve all books.
        
        Returns:
            List of all books with their related entities.
        """
        return self.repository.get_all()
    
    def get_book_by_id(self, book_id: int) -> Book:
        """Retrieve a specific book by ID.
        
        Args:
            book_id: The book's primary key.
            
        Returns:
            The book if found.
            
        Raises:
            NotFoundException: If the book doesn't exist.
        """
        book = self.repository.get_by_id(book_id)
        if not book:
            raise NotFoundException("Book", book_id)
        return book
    
    def create_book(self, book_data: BookCreate) -> Book:
        """Create a new book.
        
        Args:
            book_data: The book data from the request.
            
        Returns:
            The newly created book.
            
        Raises:
            ValidationException: If genre, publisher, or any author doesn't exist.
        """
        # Validate genre exists
        if not self.genre_repository.exists(book_data.genre_id):
            raise ValidationException(f"Genre with id {book_data.genre_id} not found")
        
        # Validate publisher exists
        if not self.publisher_repository.exists(book_data.publisher_id):
            raise ValidationException(f"Publisher with id {book_data.publisher_id} not found")
        
        # Validate all authors exist
        authors = self._get_and_validate_authors(book_data.author_ids)
        
        book = Book(
            title=book_data.title,
            isbn=book_data.isbn,
            publication_year=book_data.publication_year,
            genre_id=book_data.genre_id,
            publisher_id=book_data.publisher_id
        )
        book.authors = authors
        
        return self.repository.create(book)
    
    def update_book(self, book_id: int, book_data: BookUpdate) -> Book:
        """Update an existing book.
        
        Args:
            book_id: The book's primary key.
            book_data: The updated book data.
            
        Returns:
            The updated book.
            
        Raises:
            NotFoundException: If the book doesn't exist.
            ValidationException: If genre, publisher, or any author doesn't exist.
        """
        book = self.get_book_by_id(book_id)
        
        update_data = book_data.model_dump(exclude_unset=True)
        
        # Validate genre if being updated
        if "genre_id" in update_data and not self.genre_repository.exists(update_data["genre_id"]):
            raise ValidationException(f"Genre with id {update_data['genre_id']} not found")
        
        # Validate publisher if being updated
        if "publisher_id" in update_data and not self.publisher_repository.exists(update_data["publisher_id"]):
            raise ValidationException(f"Publisher with id {update_data['publisher_id']} not found")
        
        # Handle authors separately
        if "author_ids" in update_data:
            author_ids = update_data.pop("author_ids")
            book.authors = self._get_and_validate_authors(author_ids)
        
        # Update remaining fields
        for field, value in update_data.items():
            setattr(book, field, value)
        
        return self.repository.update(book)
    
    def delete_book(self, book_id: int) -> None:
        """Delete a book.
        
        Args:
            book_id: The book's primary key.
            
        Raises:
            NotFoundException: If the book doesn't exist.
        """
        book = self.get_book_by_id(book_id)
        self.repository.delete(book)
    
    def _get_and_validate_authors(self, author_ids: List[int]) -> List[Author]:
        """Validate and retrieve authors by their IDs.
        
        Args:
            author_ids: List of author primary keys.
            
        Returns:
            List of Author objects.
            
        Raises:
            ValidationException: If any author doesn't exist.
        """
        if not author_ids:
            raise ValidationException("At least one author is required")
        
        authors = []
        for author_id in author_ids:
            author = self.author_repository.get_by_id(author_id)
            if not author:
                raise ValidationException(f"Author with id {author_id} not found")
            authors.append(author)
        
        return authors
