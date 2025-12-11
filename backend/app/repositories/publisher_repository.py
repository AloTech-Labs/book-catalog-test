"""Publisher repository for data access operations"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models import Publisher
from .base_repository import BaseRepository


class PublisherRepository(BaseRepository[Publisher]):
    """Repository for Publisher entity data access.
    
    Extends BaseRepository with publisher-specific query methods.
    """
    
    def __init__(self, db: Session):
        """Initialize the publisher repository.
        
        Args:
            db: The database session.
        """
        super().__init__(Publisher, db)
    
    def get_by_name(self, name: str) -> Optional[Publisher]:
        """Find a publisher by its name.
        
        Args:
            name: The publisher name to search for.
            
        Returns:
            The publisher if found, None otherwise.
        """
        return (
            self.db.query(Publisher)
            .filter(Publisher.name == name)
            .first()
        )
    
    def get_all_sorted(self) -> List[Publisher]:
        """Retrieve all publishers sorted alphabetically by name.
        
        Returns:
            List of all publishers sorted by name.
        """
        return (
            self.db.query(Publisher)
            .order_by(Publisher.name)
            .all()
        )
