/**
 * AuthorDetails - Component to display author information and their books
 */

import React from 'react';
import type { AuthorWithBooks, Book } from '../types';

interface AuthorDetailsProps {
  author: AuthorWithBooks;
  selectedBook: Book | null;
  onEditAuthor: () => void;
  onDeleteAuthor: () => void;
  onSelectBook: (bookId: number) => void;
  onAddBook: () => void;
  onEditBook: () => void;
  onDeleteBook: () => void;
}

export const AuthorDetails: React.FC<AuthorDetailsProps> = ({
  author,
  selectedBook,
  onEditAuthor,
  onDeleteAuthor,
  onSelectBook,
  onAddBook,
  onEditBook,
  onDeleteBook,
}) => {
  return (
    <>
      <div className="content-header">
        <h1>{author.name} {author.surname}</h1>
        <p>{author.books.length} book(s) in catalog</p>
      </div>

      <div className="content-body">
        {/* Author Info Section */}
        <div className="author-info">
          <div className="author-info-header">
            <h3>Author Information</h3>
            <div className="action-buttons">
              <button className="edit-btn" onClick={onEditAuthor}>
                Edit
              </button>
              <button className="delete-btn" onClick={onDeleteAuthor}>
                Delete
              </button>
            </div>
          </div>
          <div className="author-details">
            <p>
              <span>Name:</span> {author.name}
            </p>
            <p>
              <span>Surname:</span> {author.surname}
            </p>
            {author.birthyear && (
              <p>
                <span>Birth Year:</span> {author.birthyear}
              </p>
            )}
          </div>
        </div>

        {/* Books Section */}
        <div className="books-section">
          <div className="books-header">
            <h3>Books</h3>
            <button className="add-btn" onClick={onAddBook}>
              + Add Book
            </button>
          </div>

          <div className="books-grid">
            {/* Books List */}
            <div className="books-list">
              {author.books.length === 0 ? (
                <div className="empty-state">
                  <p>No books by this author</p>
                </div>
              ) : (
                author.books.map(book => (
                  <div
                    key={book.id}
                    className={`book-item ${
                      selectedBook?.id === book.id ? 'active' : ''
                    }`}
                    onClick={() => onSelectBook(book.id)}
                  >
                    <h4>{book.title}</h4>
                    <p>Click to view details</p>
                  </div>
                ))
              )}
            </div>

            {/* Book Details */}
            <div className="book-details">
              {selectedBook ? (
                <>
                  <div className="book-details-header">
                    <div>
                      <h3>{selectedBook.title}</h3>
                    </div>
                    <div className="action-buttons">
                      <button className="edit-btn" onClick={onEditBook}>
                        Edit
                      </button>
                      <button className="delete-btn" onClick={onDeleteBook}>
                        Delete
                      </button>
                    </div>
                  </div>
                  <div className="book-details-content">
                    {selectedBook.edition && (
                      <div className="detail-row">
                        <span className="detail-label">Edition:</span>
                        <span className="detail-value">{selectedBook.edition}</span>
                      </div>
                    )}
                    {selectedBook.published_date && (
                      <div className="detail-row">
                        <span className="detail-label">Published:</span>
                        <span className="detail-value">
                          {new Date(selectedBook.published_date).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                    {selectedBook.publisher && (
                      <div className="detail-row">
                        <span className="detail-label">Publisher:</span>
                        <span className="detail-value">
                          {selectedBook.publisher.name}
                        </span>
                      </div>
                    )}
                    {selectedBook.genre && (
                      <div className="detail-row">
                        <span className="detail-label">Genre:</span>
                        <span className="detail-value">{selectedBook.genre.name}</span>
                      </div>
                    )}
                    {selectedBook.authors.length > 0 && (
                      <div className="detail-row">
                        <span className="detail-label">Authors:</span>
                        <span className="detail-value">
                          {selectedBook.authors
                            .map(a => `${a.name} ${a.surname}`)
                            .join(', ')}
                        </span>
                      </div>
                    )}
                  </div>
                </>
              ) : (
                <div className="empty-state">
                  <h3>Select a book</h3>
                  <p>Click on a book to view its details</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};
