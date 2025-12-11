"""Service layer for Publisher business logic."""

from typing import List
from sqlalchemy.orm import Session

from app.models import Publisher
from app.schemas import PublisherCreate, PublisherUpdate
from app.repositories import PublisherRepository, BookRepository
from app.core.exceptions import NotFoundException, DeletionNotAllowedException


class PublisherService:
    """Service class for Publisher business logic.
    
    Encapsulates all business rules and validation logic for Publisher operations,
    providing a clean interface for the API layer.
    """
    
    def __init__(self, db: Session):
        """Initialize the publisher service.
        
        Args:
            db: The database session.
        """
        self.repository = PublisherRepository(db)
        self.book_repository = BookRepository(db)
    
    def get_all_publishers(self) -> List[Publisher]:
        """Retrieve all publishers sorted by name.
        
        Returns:
            List of all publishers sorted alphabetically.
        """
        return self.repository.get_all_sorted()
    
    def get_publisher_by_id(self, publisher_id: int) -> Publisher:
        """Retrieve a specific publisher by ID.
        
        Args:
            publisher_id: The publisher's primary key.
            
        Returns:
            The publisher if found.
            
        Raises:
            NotFoundException: If the publisher doesn't exist.
        """
        publisher = self.repository.get_by_id(publisher_id)
        if not publisher:
            raise NotFoundException("Publisher", publisher_id)
        return publisher
    
    def create_publisher(self, publisher_data: PublisherCreate) -> Publisher:
        """Create a new publisher.
        
        Args:
            publisher_data: The publisher data from the request.
            
        Returns:
            The newly created publisher.
        """
        publisher = Publisher(name=publisher_data.name)
        return self.repository.create(publisher)
    
    def update_publisher(self, publisher_id: int, publisher_data: PublisherUpdate) -> Publisher:
        """Update an existing publisher.
        
        Args:
            publisher_id: The publisher's primary key.
            publisher_data: The updated publisher data.
            
        Returns:
            The updated publisher.
            
        Raises:
            NotFoundException: If the publisher doesn't exist.
        """
        publisher = self.get_publisher_by_id(publisher_id)
        
        update_data = publisher_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(publisher, field, value)
        
        return self.repository.update(publisher)
    
    def delete_publisher(self, publisher_id: int) -> None:
        """Delete a publisher.
        
        Args:
            publisher_id: The publisher's primary key.
            
        Raises:
            NotFoundException: If the publisher doesn't exist.
            DeletionNotAllowedException: If the publisher has associated books.
        """
        publisher = self.get_publisher_by_id(publisher_id)
        
        book_count = self.book_repository.count_by_publisher(publisher_id)
        if book_count > 0:
            raise DeletionNotAllowedException(
                "Publisher",
                f"publisher has {book_count} associated book(s). Reassign or delete books first."
            )
        
        self.repository.delete(publisher)
