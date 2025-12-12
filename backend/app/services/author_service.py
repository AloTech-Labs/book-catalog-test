"""Author service for business logic operations."""

from typing import List
from sqlalchemy.orm import Session

from app.models import Author
from app.schemas import AuthorCreate, AuthorUpdate
from app.repositories import AuthorRepository
from app.core.exceptions import NotFoundException, DeletionNotAllowedException


class AuthorService:
    """Service class for Author business logic.
    
    Encapsulates all business rules and validation logic for Author operations,
    providing a clean interface for the API layer.
    """
    
    def __init__(self, db: Session):
        """Initialize the author service.
        
        Args:
            db: The database session.
        """
        self.repository = AuthorRepository(db)
    
    def get_all_authors(self) -> List[Author]:
        """Retrieve all authors.
        
        Returns:
            List of all authors with their books.
        """
        return self.repository.get_all()
    
    def get_author_by_id(self, author_id: int) -> Author:
        """Retrieve a specific author by ID.
        
        Args:
            author_id: The author's primary key.
            
        Returns:
            The author if found.
            
        Raises:
            NotFoundException: If the author doesn't exist.
        """
        author = self.repository.get_by_id(author_id)
        if not author:
            raise NotFoundException("Author", author_id)
        return author
    
    def create_author(self, author_data: AuthorCreate) -> Author:
        """Create a new author.
        
        Args:
            author_data: The author data from the request.
            
        Returns:
            The newly created author.
        """
        author = Author(
            name=author_data.name,
            surname=author_data.surname,
            birthyear=author_data.birthyear
        )
        return self.repository.create(author)
    
    def update_author(self, author_id: int, author_data: AuthorUpdate) -> Author:
        """Update an existing author.
        
        Args:
            author_id: The author's primary key.
            author_data: The updated author data.
            
        Returns:
            The updated author.
            
        Raises:
            NotFoundException: If the author doesn't exist.
        """
        author = self.get_author_by_id(author_id)
        
        update_data = author_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(author, field, value)
        
        return self.repository.update(author)
    
    def delete_author(self, author_id: int) -> None:
        """Delete an author.
        
        Args:
            author_id: The author's primary key.
            
        Raises:
            NotFoundException: If the author doesn't exist.
            DeletionNotAllowedException: If the author has associated books.
        """
        author = self.get_author_by_id(author_id)
        
        if self.repository.has_books(author_id):
            raise DeletionNotAllowedException(
                "Author",
                "author has associated books. Remove book associations first."
            )
        
        self.repository.delete(author)
