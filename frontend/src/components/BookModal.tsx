/**
 * BookModal - Modal component for creating/editing books
 */

import React, { useState, useEffect } from 'react';
import type { Book, BookFormData, Author, Publisher, Genre } from '../types';

interface BookModalProps {
  book?: Book;
  authors: Author[];
  publishers: Publisher[];
  genres: Genre[];
  defaultAuthorId?: number;
  onSave: (data: BookFormData) => Promise<void>;
  onClose: () => void;
}

export const BookModal: React.FC<BookModalProps> = ({
  book,
  authors,
  publishers,
  genres,
  defaultAuthorId,
  onSave,
  onClose,
}) => {
  const [formData, setFormData] = useState<BookFormData>({
    title: '',
    edition: '',
    published_date: '',
    publisher_id: undefined,
    genre_id: undefined,
    author_ids: defaultAuthorId ? [defaultAuthorId] : [],
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (book) {
      setFormData({
        title: book.title,
        edition: book.edition || '',
        published_date: book.published_date || '',
        publisher_id: book.publisher_id,
        genre_id: book.genre_id,
        author_ids: book.authors.map(a => a.id),
      });
    }
  }, [book]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    try {
      await onSave(formData);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name.endsWith('_id') 
        ? (value ? parseInt(value, 10) : undefined)
        : value,
    }));
  };

  const handleAuthorToggle = (authorId: number) => {
    setFormData(prev => ({
      ...prev,
      author_ids: prev.author_ids.includes(authorId)
        ? prev.author_ids.filter(id => id !== authorId)
        : [...prev.author_ids, authorId],
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>{book ? 'Edit Book' : 'Add New Book'}</h2>

        {error && <div className="error-message">{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              type="text"
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Enter book title"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="edition">Edition</label>
            <input
              type="text"
              id="edition"
              name="edition"
              value={formData.edition}
              onChange={handleChange}
              placeholder="e.g., 1st Edition"
            />
          </div>

          <div className="form-group">
            <label htmlFor="published_date">Published Date</label>
            <input
              type="date"
              id="published_date"
              name="published_date"
              value={formData.published_date}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label htmlFor="publisher_id">Publisher</label>
            <select
              id="publisher_id"
              name="publisher_id"
              value={formData.publisher_id || ''}
              onChange={handleChange}
            >
              <option value="">Select a publisher</option>
              {publishers.map(publisher => (
                <option key={publisher.id} value={publisher.id}>
                  {publisher.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="genre_id">Genre</label>
            <select
              id="genre_id"
              name="genre_id"
              value={formData.genre_id || ''}
              onChange={handleChange}
            >
              <option value="">Select a genre</option>
              {genres.map(genre => (
                <option key={genre.id} value={genre.id}>
                  {genre.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Authors</label>
            <div className="checkbox-group">
              {authors.map(author => (
                <label key={author.id} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={formData.author_ids.includes(author.id)}
                    onChange={() => handleAuthorToggle(author.id)}
                  />
                  {author.name} {author.surname}
                </label>
              ))}
            </div>
          </div>

          <div className="modal-buttons">
            <button
              type="button"
              className="cancel-btn"
              onClick={onClose}
              disabled={loading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="save-btn" 
              disabled={loading}
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
