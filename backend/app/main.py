"""Main FastAPI application module."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .database import engine, Base, SessionLocal
from .seed import seed_database
from .routers import authors, books, genres, publishers
from .core.exceptions import AppException

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Book Catalog API",
    description="REST API for managing a catalog of books, authors, publishers, and genres",
    version="1.0.0",
)


# Global exception handler for custom application exceptions
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle custom application exceptions.
    
    Converts AppException and its subclasses into appropriate JSON responses
    with the correct HTTP status codes.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
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
