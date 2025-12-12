"""Author repository for data access operations"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.models import Author
from .base_repository import BaseRepository


class AuthorRepository(BaseRepository[Author]):
    """Repository for Author entity data access.
    
    Extends BaseRepository with author-specific query methods.
    """
    
    def __init__(self, db: Session):
        """Initialize the author repository.
        
        Args:
            db: The database session.
        """
        super().__init__(Author, db)
    
    def get_all(self) -> List[Author]:
        """Retrieve all authors with their books eagerly loaded.
        
        Returns:
            List of all authors with their associated books.
        """
        return (
            self.db.query(Author)
            .options(joinedload(Author.books))
            .all()
        )
    
    def get_by_id(self, id: int) -> Optional[Author]:
        """Retrieve an author by ID with books eagerly loaded.
        
        Args:
            id: The author's primary key.
            
        Returns:
            The author if found, None otherwise.
        """
        return (
            self.db.query(Author)
            .options(joinedload(Author.books))
            .filter(Author.id == id)
            .first()
        )
    
    def has_books(self, author_id: int) -> bool:
        """Check if an author has any associated books.
        
        Args:
            author_id: The author's primary key.
            
        Returns:
            True if the author has books, False otherwise.
        """
        author = self.get_by_id(author_id)
        return author is not None and len(author.books) > 0
    
    def get_by_name(self, name: str) -> Optional[Author]:
        """Find an author by their full name.
        
        Args:
            name: The author's name to search for.
            
        Returns:
            The author if found, None otherwise.
        """
        return (
            self.db.query(Author)
            .filter(Author.name == name)
            .first()
        )
