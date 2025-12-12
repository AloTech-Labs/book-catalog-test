"""Repository module for data access layer."""

from .author_repository import AuthorRepository
from .book_repository import BookRepository
from .genre_repository import GenreRepository
from .publisher_repository import PublisherRepository

__all__ = [
    "AuthorRepository",
    "BookRepository",
    "GenreRepository",
    "PublisherRepository",
]
