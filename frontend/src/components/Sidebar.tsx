/**
 * Sidebar - Author navigation sidebar component
 */

import React from 'react';
import type { Author } from '../types';

interface SidebarProps {
  authors: Author[];
  selectedAuthorId: number | null;
  onSelectAuthor: (author: Author) => void;
  onAddAuthor: () => void;
  loading: boolean;
}

export const Sidebar: React.FC<SidebarProps> = ({
  authors,
  selectedAuthorId,
  onSelectAuthor,
  onAddAuthor,
  loading,
}) => {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Authors</h2>
        <button className="add-btn" onClick={onAddAuthor}>
          + Add
        </button>
      </div>
      
      <div className="author-list">
        {loading ? (
          <div className="loading">Loading authors...</div>
        ) : authors.length === 0 ? (
          <div className="empty-state">
            <p>No authors yet</p>
          </div>
        ) : (
          authors.map(author => (
            <div
              key={author.id}
              className={`author-item ${
                selectedAuthorId === author.id ? 'active' : ''
              }`}
              onClick={() => onSelectAuthor(author)}
            >
              <span className="author-name">
                {author.surname}, {author.name}
              </span>
            </div>
          ))
        )}
      </div>
    </aside>
  );
};
