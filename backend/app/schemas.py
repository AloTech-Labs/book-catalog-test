from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

# ============== Author Schemas ==============
class AuthorBase(BaseModel):
    """Base author schema."""
    name: str
    surname: str
    birthyear: Optional[int] = None


class AuthorCreate(AuthorBase):
    """Schema for creating an author."""
    pass


class AuthorUpdate(AuthorBase):
    """Schema for updating an author."""
    pass


class AuthorSummary(BaseModel):
    """Summary schema for author list."""
    id: int
    name: str
    surname: str

    model_config = ConfigDict(from_attributes=True)


class AuthorResponse(AuthorBase):
    """Full author response schema."""
    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorWithBooks(AuthorResponse):
    """Author with their books."""
    books: list["BookSummary"] = []


# ============== Publisher Schemas ==============
class PublisherBase(BaseModel):
    """Base publisher schema."""
    name: str
    website: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[date] = None


class PublisherCreate(PublisherBase):
    """Schema for creating a publisher."""
    pass


class PublisherUpdate(PublisherBase):
    """Schema for updating a publisher."""
    pass


class PublisherSummary(BaseModel):
    """Summary schema for publisher list."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class PublisherResponse(PublisherBase):
    """Full publisher response schema."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============== Genre Schemas ==============
class GenreBase(BaseModel):
    """Base genre schema."""
    name: str
    description: Optional[str] = None


class GenreCreate(GenreBase):
    """Schema for creating a genre."""
    pass


class GenreUpdate(GenreBase):
    """Schema for updating a genre."""
    pass


class GenreSummary(BaseModel):
    """Summary schema for genre list."""
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class GenreResponse(GenreBase):
    """Full genre response schema."""
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============== Book Schemas ==============
class BookBase(BaseModel):
    """Base book schema."""
    title: str
    edition: Optional[str] = None
    published_date: Optional[date] = None
    publisher_id: Optional[int] = None
    genre_id: Optional[int] = None


class BookCreate(BookBase):
    """Schema for creating a book."""
    author_ids: list[int] = []


class BookUpdate(BookBase):
    """Schema for updating a book."""
    author_ids: list[int] = []


class BookSummary(BaseModel):
    """Summary schema for book list."""
    id: int
    title: str

    model_config = ConfigDict(from_attributes=True)


class BookResponse(BookBase):
    """Full book response schema."""
    id: int
    authors: list[AuthorSummary] = []
    publisher: Optional[PublisherSummary] = None
    genre: Optional[GenreSummary] = None

    model_config = ConfigDict(from_attributes=True)


# Rebuild models for forward references
AuthorWithBooks.model_rebuild()
