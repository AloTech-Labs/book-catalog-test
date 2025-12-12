/**
 * Book Catalog Application
 * Main App component that manages the application state and layout
 */

import { useState, useEffect, useCallback } from 'react';
import { 
  Sidebar, 
  AuthorDetails, 
  AuthorModal, 
  BookModal 
} from './components';
import { authorApi, bookApi, publisherApi, genreApi } from './api';
import type { 
  Author, 
  AuthorWithBooks, 
  Book, 
  Publisher, 
  Genre,
  AuthorFormData,
  BookFormData 
} from './types';

function App() {
  // State for data
  const [authors, setAuthors] = useState<Author[]>([]);
  const [selectedAuthor, setSelectedAuthor] = useState<AuthorWithBooks | null>(null);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [publishers, setPublishers] = useState<Publisher[]>([]);
  const [genres, setGenres] = useState<Genre[]>([]);

  // State for UI
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  // Modal state
  const [showAuthorModal, setShowAuthorModal] = useState(false);
  const [showBookModal, setShowBookModal] = useState(false);
  const [editingAuthor, setEditingAuthor] = useState<Author | undefined>();
  const [editingBook, setEditingBook] = useState<Book | undefined>();

  /**
   * Load initial data on mount
   */
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true);
        const [authorsData, publishersData, genresData] = await Promise.all([
          authorApi.getAll(),
          publisherApi.getAll(),
          genreApi.getAll(),
        ]);
        setAuthors(authorsData);
        setPublishers(publishersData);
        setGenres(genresData);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load data');
      } finally {
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  /**
   * Refresh authors list
   */
  const refreshAuthors = useCallback(async () => {
    try {
      const authorsData = await authorApi.getAll();
      setAuthors(authorsData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to refresh authors');
    }
  }, []);

  /**
   * Handle author selection
   */
  const handleSelectAuthor = useCallback(async (author: Author) => {
    try {
      const authorDetails = await authorApi.getById(author.id);
      setSelectedAuthor(authorDetails);
      setSelectedBook(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load author details');
    }
  }, []);

  /**
   * Handle book selection
   */
  const handleSelectBook = useCallback(async (bookId: number) => {
    try {
      const bookDetails = await bookApi.getById(bookId);
      setSelectedBook(bookDetails);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load book details');
    }
  }, []);

  /**
   * Save author (create or update)
   */
  const handleSaveAuthor = async (data: AuthorFormData) => {
    if (editingAuthor) {
      await authorApi.update(editingAuthor.id, data);
      if (selectedAuthor?.id === editingAuthor.id) {
        const updatedAuthor = await authorApi.getById(editingAuthor.id);
        setSelectedAuthor(updatedAuthor);
      }
    } else {
      await authorApi.create(data);
    }
    await refreshAuthors();
    setEditingAuthor(undefined);
  };

  /**
   * Delete author
   */
  const handleDeleteAuthor = async () => {
    if (!selectedAuthor) return;

    if (!window.confirm(`Are you sure you want to delete ${selectedAuthor.name} ${selectedAuthor.surname}?`)) {
      return;
    }

    try {
      await authorApi.delete(selectedAuthor.id);
      setSelectedAuthor(null);
      setSelectedBook(null);
      await refreshAuthors();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete author');
    }
  };

  /**
   * Save book (create or update)
   */
  const handleSaveBook = async (data: BookFormData) => {
    if (editingBook) {
      await bookApi.update(editingBook.id, data);
    } else {
      await bookApi.create(data);
    }
    
    // Refresh author to get updated book list
    if (selectedAuthor) {
      const updatedAuthor = await authorApi.getById(selectedAuthor.id);
      setSelectedAuthor(updatedAuthor);
    }
    
    // Refresh selected book if editing
    if (editingBook) {
      const updatedBook = await bookApi.getById(editingBook.id);
      setSelectedBook(updatedBook);
    }
    
    setEditingBook(undefined);
  };

  /**
   * Delete book
   */
  const handleDeleteBook = async () => {
    if (!selectedBook) return;

    if (!window.confirm(`Are you sure you want to delete "${selectedBook.title}"?`)) {
      return;
    }

    try {
      await bookApi.delete(selectedBook.id);
      setSelectedBook(null);
      
      // Refresh author to get updated book list
      if (selectedAuthor) {
        const updatedAuthor = await authorApi.getById(selectedAuthor.id);
        setSelectedAuthor(updatedAuthor);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete book');
    }
  };

  /**
   * Open author modal for adding
   */
  const handleAddAuthor = () => {
    setEditingAuthor(undefined);
    setShowAuthorModal(true);
  };

  /**
   * Open author modal for editing
   */
  const handleEditAuthor = () => {
    if (selectedAuthor) {
      setEditingAuthor(selectedAuthor);
      setShowAuthorModal(true);
    }
  };

  /**
   * Open book modal for adding
   */
  const handleAddBook = () => {
    setEditingBook(undefined);
    setShowBookModal(true);
  };

  /**
   * Open book modal for editing
   */
  const handleEditBook = () => {
    if (selectedBook) {
      setEditingBook(selectedBook);
      setShowBookModal(true);
    }
  };

  return (
    <div className="app">
      {/* Sidebar with authors list */}
      <Sidebar
        authors={authors}
        selectedAuthorId={selectedAuthor?.id ?? null}
        onSelectAuthor={handleSelectAuthor}
        onAddAuthor={handleAddAuthor}
        loading={loading}
      />

      {/* Main content area */}
      <main className="main-content">
        {error && (
          <div className="error-message" style={{ margin: '20px' }}>
            {error}
            <button 
              onClick={() => setError('')}
              style={{ marginLeft: '10px', cursor: 'pointer' }}
            >
              ✕
            </button>
          </div>
        )}

        {selectedAuthor ? (
          <AuthorDetails
            author={selectedAuthor}
            selectedBook={selectedBook}
            onEditAuthor={handleEditAuthor}
            onDeleteAuthor={handleDeleteAuthor}
            onSelectBook={handleSelectBook}
            onAddBook={handleAddBook}
            onEditBook={handleEditBook}
            onDeleteBook={handleDeleteBook}
          />
        ) : (
          <div className="empty-state" style={{ flex: 1 }}>
            <h3>Welcome to Book Catalog</h3>
            <p>Select an author from the sidebar to view their books</p>
          </div>
        )}
      </main>

      {/* Author Modal */}
      {showAuthorModal && (
        <AuthorModal
          author={editingAuthor}
          onSave={handleSaveAuthor}
          onClose={() => {
            setShowAuthorModal(false);
            setEditingAuthor(undefined);
          }}
        />
      )}

      {/* Book Modal */}
      {showBookModal && (
        <BookModal
          book={editingBook}
          authors={authors}
          publishers={publishers}
          genres={genres}
          defaultAuthorId={selectedAuthor?.id}
          onSave={handleSaveBook}
          onClose={() => {
            setShowBookModal(false);
            setEditingBook(undefined);
          }}
        />
      )}
    </div>
  );
}

export default App;
