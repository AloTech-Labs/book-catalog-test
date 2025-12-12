# Book Catalog - Full Stack Application

A complete web application for managing a catalog of books, built with React (frontend) and Python/FastAPI (backend).

## Overview

This application allows users to:
- Browse and manage authors
- View and manage books by each author
- Assign multiple authors to books
- Categorize books by genre and publisher

##  Project Structure

```
python task/
├── backend/                  # Python FastAPI backend
│   ├── app/
│   │   ├── routers/         # API route handlers
│   │   ├── main.py          # Application entry point
│   │   ├── models.py        # Database models
│   │   ├── schemas.py       # Pydantic schemas
│   │   ├── database.py      # Database configuration
│   │   └── seed.py          # Sample data
│   ├── requirements.txt
│   └── README.md
│
├── frontend/                 # React TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.tsx          # Main app component
│   │   ├── api.ts           # API service
│   │   └── types.ts         # Type definitions
│   ├── package.json
│   └── README.md
│
└── README.md                 # This file
```

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Database storage
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **CSS3** - Styling

##  Quick Start

### 1. Start the Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

Backend will be running at: http://localhost:8080

### 2. Start the Frontend

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be running at: http://localhost:3000

##  API Documentation

When the backend is running, visit:
- **Swagger UI**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## API Endpoints

| Endpoint | Methods | Description |
|----------|---------|-------------|
| `/authors` | GET, POST | List/create authors |
| `/authors/{id}` | GET, PUT, DELETE | Get/update/delete author |
| `/books` | GET, POST | List/create books |
| `/books/{id}` | GET, PUT, DELETE | Get/update/delete book |
| `/genres` | GET, POST | List/create genres |
| `/genres/{id}` | GET, PUT, DELETE | Get/update/delete genre |
| `/publishers` | GET, POST | List/create publishers |
| `/publishers/{id}` | GET, PUT, DELETE | Get/update/delete publisher |

##  Data Models

### Author
- `name` (string): First name
- `surname` (string): Last name
- `birthyear` (integer, optional): Year of birth

### Book
- `title` (string): Book title
- `edition` (string, optional): Edition info
- `published_date` (date, optional): Publication date
- `publisher_id` (integer, optional): Publisher reference
- `genre_id` (integer, optional): Genre reference
- `author_ids` (array): List of author IDs

### Publisher
- `name` (string): Publisher name
- `website` (string, optional): Website URL
- `description` (string, optional): Description
- `creation_date` (date, optional): Founded date

### Genre
- `name` (string): Genre name
- `description` (string, optional): Description

## Features

### Frontend Features
- ✅ Author navigation sidebar
- ✅ Author CRUD operations
- ✅ Book CRUD operations
- ✅ Book details view
- ✅ Modal forms for create/edit
- ✅ Delete confirmation dialogs
- ✅ Error handling

### Backend Features
- ✅ RESTful API design
- ✅ Full CRUD for all entities
- ✅ Filtering and sorting
- ✅ Data validation
- ✅ Relationship management
- ✅ Cascade delete protection
- ✅ Auto-seeding sample data

## Business Rules

1. **Authors cannot be deleted** if they have associated books
2. **Publishers and genres** are managed as read-only in the frontend (simulating admin-only access)
3. **Books can have multiple authors** (many-to-many relationship)
4. **Author list can be empty** for a book

## Testing

### Backend Testing
```bash
# Using curl
curl http://localhost:8080/authors
curl http://localhost:8080/books

# Using Swagger UI
# Visit http://localhost:8080/docs
```

### Frontend Testing
1. Open http://localhost:3000
2. Click on authors to view their books
3. Use Add/Edit/Delete buttons to test CRUD operations

## ample Data

The application comes pre-seeded with:
- **5 Authors**: George Orwell, Jane Austen, Ernest Hemingway, Virginia Woolf, Gabriel García Márquez
- **6 Books**: 1984, Animal Farm, Pride and Prejudice, The Old Man and the Sea, Mrs Dalloway, One Hundred Years of Solitude
- **10 Genres**: Fiction, Non-Fiction, Science Fiction, Fantasy, Mystery, Romance, Thriller, Biography, History, Self-Help
- **5 Publishers**: Penguin Random House, HarperCollins, Simon & Schuster, Macmillan Publishers, Hachette Book Group

