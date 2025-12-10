"""Publisher router with CRUD operations."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from ..database import get_db
from ..models import Publisher
from ..schemas import (
    PublisherCreate,
    PublisherUpdate,
    PublisherSummary,
    PublisherResponse,
)

router = APIRouter(prefix="/publishers", tags=["Publishers"])


@router.get("", response_model=list[PublisherSummary])
def get_publishers(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Filter by name"),
    sort_by: Optional[str] = Query("name", description="Sort field"),
    order: Optional[str] = Query("asc", description="Sort order: asc or desc"),
):
    """Get list of all publishers with optional filtering and sorting."""
    query = db.query(Publisher)

    # Apply filters
    if name:
        query = query.filter(Publisher.name.ilike(f"%{name}%"))

    # Apply sorting
    sort_column = getattr(Publisher, sort_by, Publisher.name)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    return query.all()


@router.post("", response_model=PublisherResponse, status_code=201)
def create_publisher(publisher: PublisherCreate, db: Session = Depends(get_db)):
    """Create a new publisher."""
    db_publisher = Publisher(**publisher.model_dump())
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@router.get("/{publisher_id}", response_model=PublisherResponse)
def get_publisher(publisher_id: int, db: Session = Depends(get_db)):
    """Get a specific publisher by ID."""
    publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if not publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")
    return publisher


@router.put("/{publisher_id}", response_model=PublisherResponse)
def update_publisher(
    publisher_id: int, publisher: PublisherUpdate, db: Session = Depends(get_db)
):
    """Update an existing publisher."""
    db_publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    for key, value in publisher.model_dump().items():
        setattr(db_publisher, key, value)

    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@router.delete("/{publisher_id}", status_code=204)
def delete_publisher(publisher_id: int, db: Session = Depends(get_db)):
    """Delete a publisher."""
    db_publisher = db.query(Publisher).filter(Publisher.id == publisher_id).first()
    if not db_publisher:
        raise HTTPException(status_code=404, detail="Publisher not found")

    db.delete(db_publisher)
    db.commit()
    return None
