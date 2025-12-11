"""Genre service for business logic operations"""

from typing import List
from sqlalchemy.orm import Session

from app.models import Genre
from app.schemas import GenreCreate, GenreUpdate
from app.repositories import GenreRepository, BookRepository
from app.core.exceptions import NotFoundException, DeletionNotAllowedException


class GenreService:
    """Service class for Genre business logic.
    
    Encapsulates all business rules and validation logic for Genre operations,
    providing a clean interface for the API layer.
    """
    
    def __init__(self, db: Session):
        """Initialize the genre service.
        
        Args:
            db: The database session.
        """
        self.repository = GenreRepository(db)
        self.book_repository = BookRepository(db)
    
    def get_all_genres(self) -> List[Genre]:
        """Retrieve all genres sorted by name.
        
        Returns:
            List of all genres sorted alphabetically.
        """
        return self.repository.get_all_sorted()
    
    def get_genre_by_id(self, genre_id: int) -> Genre:
        """Retrieve a specific genre by ID.
        
        Args:
            genre_id: The genre's primary key.
            
        Returns:
            The genre if found.
            
        Raises:
            NotFoundException: If the genre doesn't exist.
        """
        genre = self.repository.get_by_id(genre_id)
        if not genre:
            raise NotFoundException("Genre", genre_id)
        return genre
    
    def create_genre(self, genre_data: GenreCreate) -> Genre:
        """Create a new genre.
        
        Args:
            genre_data: The genre data from the request.
            
        Returns:
            The newly created genre.
        """
        genre = Genre(name=genre_data.name)
        return self.repository.create(genre)
    
    def update_genre(self, genre_id: int, genre_data: GenreUpdate) -> Genre:
        """Update an existing genre.
        
        Args:
            genre_id: The genre's primary key.
            genre_data: The updated genre data.
            
        Returns:
            The updated genre.
            
        Raises:
            NotFoundException: If the genre doesn't exist.
        """
        genre = self.get_genre_by_id(genre_id)
        
        update_data = genre_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(genre, field, value)
        
        return self.repository.update(genre)
    
    def delete_genre(self, genre_id: int) -> None:
        """Delete a genre.
        
        Args:
            genre_id: The genre's primary key.
            
        Raises:
            NotFoundException: If the genre doesn't exist.
            DeletionNotAllowedException: If the genre has associated books.
        """
        genre = self.get_genre_by_id(genre_id)
        
        book_count = self.book_repository.count_by_genre(genre_id)
        if book_count > 0:
            raise DeletionNotAllowedException(
                "Genre",
                f"genre has {book_count} associated book(s). Reassign or delete books first."
            )
        
        self.repository.delete(genre)
