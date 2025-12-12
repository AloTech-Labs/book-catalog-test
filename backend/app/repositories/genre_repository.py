"""Genre repository for data access operations"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Genre
from .base_repository import BaseRepository


class GenreRepository(BaseRepository[Genre]):
    """Repository for Genre entity data access.
    
    Extends BaseRepository with genre-specific query methods.
    """
    
    def __init__(self, db: Session):
        """Initialize the genre repository.
        
        Args:
            db: The database session.
        """
        super().__init__(Genre, db)
    
    def get_by_name(self, name: str) -> Optional[Genre]:
        """Find a genre by its name.
        
        Args:
            name: The genre name to search for.
            
        Returns:
            The genre if found, None otherwise.
        """
        return (
            self.db.query(Genre)
            .filter(Genre.name == name)
            .first()
        )
    
    def get_all_sorted(self) -> List[Genre]:
        """Retrieve all genres sorted alphabetically by name.
        
        Returns:
            List of all genres sorted by name.
        """
        return (
            self.db.query(Genre)
            .order_by(Genre.name)
            .all()
        )
