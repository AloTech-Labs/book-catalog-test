# Book Catalog API - Backend

A RESTful API backend built with FastAPI and SQLAlchemy for managing a catalog of books, authors, publishers, and genres.

## Architecture

This backend follows a microservice-oriented architecture with clear separation of concerns:

```
backend/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py               # FastAPI application entry point
│   ├── database.py           # Database configuration
│   ├── models.py             # SQLAlchemy ORM models
│   ├── schemas.py            # Pydantic schemas for validation
│   ├── seed.py               # Initial data seeding
│   └── routers/              # API route handlers
│       ├── __init__.py
│       ├── authors.py
│       ├── books.py
│       ├── genres.py
│       └── publishers.py
└── requirements.txt          # Python dependencies
```

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

The API will be available at `http://localhost:8080`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## API Endpoints

### Authors
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/authors` | Get all authors (with filtering & sorting) |
| POST | `/authors` | Create a new author |
| GET | `/authors/{id}` | Get author by ID with books |
| PUT | `/authors/{id}` | Update an author |
| DELETE | `/authors/{id}` | Delete an author (if no books) |

### Books
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/books` | Get all books (with filtering & sorting) |
| POST | `/books` | Create a new book |
| GET | `/books/{id}` | Get book by ID |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

### Genres
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/genres` | Get all genres |
| POST | `/genres` | Create a new genre |
| GET | `/genres/{id}` | Get genre by ID |
| PUT | `/genres/{id}` | Update a genre |
| DELETE | `/genres/{id}` | Delete a genre |

### Publishers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/publishers` | Get all publishers |
| POST | `/publishers` | Create a new publisher |
| GET | `/publishers/{id}` | Get publisher by ID |
| PUT | `/publishers/{id}` | Update a publisher |
| DELETE | `/publishers/{id}` | Delete a publisher |

## Query Parameters

### Filtering
- `name`: Filter by name (partial match)
- `surname`: Filter by surname (authors only)
- `title`: Filter by title (books only)
- `genre_id`: Filter by genre (books only)
- `publisher_id`: Filter by publisher (books only)
- `author_id`: Filter by author (books only)

### Sorting
- `sort_by`: Field to sort by (default varies by endpoint)
- `order`: Sort order (`asc` or `desc`)

##  Data Models

### Author
```json
{
  "id": 1,
  "name": "George",
  "surname": "Orwell",
  "birthyear": 1903
}
```

### Book
```json
{
  "id": 1,
  "title": "1984",
  "edition": "1st Edition",
  "published_date": "1949-06-08",
  "publisher_id": 1,
  "genre_id": 3,
  "authors": [...],
  "publisher": {...},
  "genre": {...}
}
```

### Publisher
```json
{
  "id": 1,
  "name": "Penguin Random House",
  "website": "https://www.penguinrandomhouse.com",
  "description": "One of the world's largest publishers",
  "creation_date": "2013-07-01"
}
```

### Genre
```json
{
  "id": 1,
  "name": "Fiction",
  "description": "Literary works based on imagination"
}
```

## Database

The application uses SQLite by default with the database file `book_catalog.db`. The database is automatically created and seeded with sample data on first run.

## Testing

To test the API endpoints, you can use:
- The built-in Swagger UI at `/docs`
- curl commands
- Postman or similar API testing tools

Example curl commands:

```bash
# Get all authors
curl http://localhost:8080/authors

# Create a new author
curl -X POST http://localhost:8080/authors \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane", "surname": "Doe", "birthyear": 1990}'

# Get author with books
curl http://localhost:8080/authors/1

# Delete an author
curl -X DELETE http://localhost:8080/authors/1
```

## Important Notes
- The database is seeded with sample publishers and genres on first run
- CORS is enabled for frontend development (ports 3000 and 5173)
