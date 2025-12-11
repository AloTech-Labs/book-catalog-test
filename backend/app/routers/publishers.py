"""Publisher API endpoints.

This module defines thin REST API endpoints for Publisher operations.
Business logic is delegated to the PublisherService.
"""

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import PublisherCreate, PublisherUpdate, PublisherSummary, PublisherResponse
from ..services import PublisherService


router = APIRouter(prefix="/publishers", tags=["Publishers"])


def get_publisher_service(db: Session = Depends(get_db)) -> PublisherService:
    """Dependency injection for PublisherService."""
    return PublisherService(db)


@router.get("", response_model=List[PublisherSummary])
def get_publishers(service: PublisherService = Depends(get_publisher_service)):
    """Get list of all publishers sorted by name.
    
    Returns a list of all publishers with summary information.
    """
    return service.get_all_publishers()


@router.post("", response_model=PublisherResponse, status_code=201)
def create_publisher(
    publisher: PublisherCreate,
    service: PublisherService = Depends(get_publisher_service)
):
    """Create a new publisher.
    
    Args:
        publisher: The publisher data to create.
        
    Returns:
        The newly created publisher.
    """
    return service.create_publisher(publisher)


@router.get("/{publisher_id}", response_model=PublisherResponse)
def get_publisher(
    publisher_id: int,
    service: PublisherService = Depends(get_publisher_service)
):
    """Get a specific publisher by ID.
    
    Args:
        publisher_id: The publisher's primary key.
        
    Returns:
        The publisher details.
    """
    return service.get_publisher_by_id(publisher_id)


@router.put("/{publisher_id}", response_model=PublisherResponse)
def update_publisher(
    publisher_id: int,
    publisher: PublisherUpdate,
    service: PublisherService = Depends(get_publisher_service)
):
    """Update an existing publisher.
    
    Args:
        publisher_id: The publisher's primary key.
        publisher: The updated publisher data.
        
    Returns:
        The updated publisher.
    """
    return service.update_publisher(publisher_id, publisher)


@router.delete("/{publisher_id}", status_code=204)
def delete_publisher(
    publisher_id: int,
    service: PublisherService = Depends(get_publisher_service)
):
    """Delete a publisher.
    
    Fails if the publisher has associated books.
    
    Args:
        publisher_id: The publisher's primary key.
    """
    service.delete_publisher(publisher_id)
    return None
