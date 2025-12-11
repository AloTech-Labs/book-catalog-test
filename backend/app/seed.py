from datetime import date
from sqlalchemy.orm import Session

from .models import Author, Book, Genre, Publisher


def seed_database(db: Session) -> None:
    """Populate database with sample data if empty."""
    
    # Check if data already exists
    if db.query(Genre).first():
        return

    # Create Genres
    genres = [
        Genre(name="Fiction", description="Literary works based on imagination"),
        Genre(name="Non-Fiction", description="Factual and informative works"),
        Genre(name="Science Fiction", description="Speculative fiction with scientific themes"),
        Genre(name="Fantasy", description="Fiction with magical or supernatural elements"),
        Genre(name="Mystery", description="Fiction dealing with puzzling crimes"),
        Genre(name="Romance", description="Stories centered on romantic relationships"),
        Genre(name="Thriller", description="Suspenseful and exciting fiction"),
        Genre(name="Biography", description="Account of someone's life"),
        Genre(name="History", description="Study of past events"),
        Genre(name="Self-Help", description="Books for personal improvement"),
    ]
    db.add_all(genres)

    # Create Publishers
    publishers = [
        Publisher(
            name="Penguin Random House",
            website="https://www.penguinrandomhouse.com",
            description="One of the world's largest English-language publishers",
            creation_date=date(2013, 7, 1),
        ),
        Publisher(
            name="HarperCollins",
            website="https://www.harpercollins.com",
            description="Global publishing company",
            creation_date=date(1989, 1, 1),
        ),
        Publisher(
            name="Simon & Schuster",
            website="https://www.simonandschuster.com",
            description="American publishing company",
            creation_date=date(1924, 1, 2),
        ),
        Publisher(
            name="Macmillan Publishers",
            website="https://www.macmillan.com",
            description="Global trade publishing company",
            creation_date=date(1843, 1, 1),
        ),
        Publisher(
            name="Hachette Book Group",
            website="https://www.hachettebookgroup.com",
            description="Major US trade publisher",
            creation_date=date(2006, 1, 1),
        ),
    ]
    db.add_all(publishers)

    # Create Authors
    authors = [
        Author(name="George", surname="Orwell", birthyear=1903),
        Author(name="Jane", surname="Austen", birthyear=1775),
        Author(name="Ernest", surname="Hemingway", birthyear=1899),
        Author(name="Virginia", surname="Woolf", birthyear=1882),
        Author(name="Gabriel", surname="García Márquez", birthyear=1927),
    ]
    db.add_all(authors)
    db.commit()

    # Create Books
    books = [
        Book(
            title="1984",
            edition="1st Edition",
            published_date=date(1949, 6, 8),
            publisher_id=1,
            genre_id=3,
            authors=[authors[0]],
        ),
        Book(
            title="Animal Farm",
            edition="1st Edition",
            published_date=date(1945, 8, 17),
            publisher_id=1,
            genre_id=1,
            authors=[authors[0]],
        ),
        Book(
            title="Pride and Prejudice",
            edition="Revised Edition",
            published_date=date(1813, 1, 28),
            publisher_id=2,
            genre_id=6,
            authors=[authors[1]],
        ),
        Book(
            title="The Old Man and the Sea",
            edition="1st Edition",
            published_date=date(1952, 9, 1),
            publisher_id=3,
            genre_id=1,
            authors=[authors[2]],
        ),
        Book(
            title="Mrs Dalloway",
            edition="1st Edition",
            published_date=date(1925, 5, 14),
            publisher_id=4,
            genre_id=1,
            authors=[authors[3]],
        ),
        Book(
            title="One Hundred Years of Solitude",
            edition="Anniversary Edition",
            published_date=date(1967, 5, 30),
            publisher_id=5,
            genre_id=4,
            authors=[authors[4]],
        ),
    ]
    db.add_all(books)
    db.commit()
