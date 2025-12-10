/**
 * AuthorModal - Modal component for creating/editing authors
 */

import React, { useState, useEffect } from 'react';
import type { Author, AuthorFormData } from '../types';

interface AuthorModalProps {
  author?: Author;
  onSave: (data: AuthorFormData) => Promise<void>;
  onClose: () => void;
}

export const AuthorModal: React.FC<AuthorModalProps> = ({ 
  author, 
  onSave, 
  onClose 
}) => {
  const [formData, setFormData] = useState<AuthorFormData>({
    name: '',
    surname: '',
    birthyear: undefined,
  });
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (author) {
      setFormData({
        name: author.name,
        surname: author.surname,
        birthyear: author.birthyear,
      });
    }
  }, [author]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!formData.name.trim() || !formData.surname.trim()) {
      setError('Name and surname are required');
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'birthyear' 
        ? (value ? parseInt(value, 10) : undefined)
        : value,
    }));
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <h2>{author ? 'Edit Author' : 'Add New Author'}</h2>
        
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Name *</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="Enter first name"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="surname">Surname *</label>
            <input
              type="text"
              id="surname"
              name="surname"
              value={formData.surname}
              onChange={handleChange}
              placeholder="Enter surname"
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="birthyear">Birth Year</label>
            <input
              type="number"
              id="birthyear"
              name="birthyear"
              value={formData.birthyear || ''}
              onChange={handleChange}
              placeholder="Enter birth year"
              min="1"
              max={new Date().getFullYear()}
            />
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
