"""Base repository providing common data access patterns"""

from typing import TypeVar, Generic, Type, Optional, List
from sqlalchemy.orm import Session
from app.models import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic base repository with common CRUD operations.
    
    Provides a standard interface for data access operations that can be
    shared across all entity repositories.
    
    Attributes:
        model: The SQLAlchemy model class this repository manages.
        db: The database session for operations.
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """Initialize the repository.
        
        Args:
            model: The SQLAlchemy model class to operate on.
            db: The database session.
        """
        self.model = model
        self.db = db
    
    def get_all(self) -> List[ModelType]:
        """Retrieve all records of this model type.
        
        Returns:
            List of all model instances.
        """
        return self.db.query(self.model).all()
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        """Retrieve a single record by its ID.
        
        Args:
            id: The primary key value.
            
        Returns:
            The model instance if found, None otherwise.
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def create(self, entity: ModelType) -> ModelType:
        """Create a new record in the database.
        
        Args:
            entity: The model instance to persist.
            
        Returns:
            The persisted model instance with updated attributes.
        """
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity: ModelType) -> ModelType:
        """Update an existing record in the database.
        
        Args:
            entity: The model instance with updated values.
            
        Returns:
            The updated model instance.
        """
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def delete(self, entity: ModelType) -> None:
        """Delete a record from the database.
        
        Args:
            entity: The model instance to delete.
        """
        self.db.delete(entity)
        self.db.commit()
    
    def exists(self, id: int) -> bool:
        """Check if a record exists by its ID.
        
        Args:
            id: The primary key value to check.
            
        Returns:
            True if the record exists, False otherwise.
        """
        return self.db.query(self.model).filter(self.model.id == id).count() > 0
