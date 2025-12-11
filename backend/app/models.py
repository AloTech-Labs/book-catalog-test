from datetime import date
from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey, Table
from sqlalchemy.orm import relationship

from .database import Base

# Association table for many-to-many relationship between books and authors
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
)


class Author(Base):
    """Author model."""
    
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    birthyear = Column(Integer, nullable=True)

    # Relationship
    books = relationship("Book", secondary=book_authors, back_populates="authors")


class Publisher(Base):
    """Publisher model."""
    
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    creation_date = Column(Date, nullable=True)

    # Relationship
    books = relationship("Book", back_populates="publisher")


class Genre(Base):
    """Genre model."""
    
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Relationship
    books = relationship("Book", back_populates="genre")


class Book(Base):
    """Book model."""
    
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    edition = Column(String(50), nullable=True)
    published_date = Column(Date, nullable=True)
    
    # Foreign keys
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), nullable=True)

    # Relationships
    authors = relationship("Author", secondary=book_authors, back_populates="books")
    publisher = relationship("Publisher", back_populates="books")
    genre = relationship("Genre", back_populates="books")
