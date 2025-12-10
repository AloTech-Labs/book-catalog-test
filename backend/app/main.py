"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base, SessionLocal
from .seed import seed_database
from .routers import authors, books, genres, publishers

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Catalog API",
    description="REST API for managing a catalog of books, authors, publishers, and genres",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(genres.router)
app.include_router(publishers.router)


@app.on_event("startup")
def startup_event():
    """Seed database on startup."""
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()


@app.get("/", tags=["Health"])
def root():
    """Health check endpoint."""
    return {"status": "healthy", "message": "Book Catalog API is running"}
