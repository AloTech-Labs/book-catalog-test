/**
 * API service for communicating with the backend
 */

import type { 
  Author, 
  AuthorWithBooks, 
  Book, 
  Publisher, 
  Genre,
  AuthorFormData,
  BookFormData 
} from './types';

const API_BASE_URL = 'http://localhost:8080';

/**
 * Generic fetch wrapper with error handling
 */
async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error! status: ${response.status}`);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T;
  }

  return response.json();
}

// ============== Author API ==============
export const authorApi = {
  getAll: (): Promise<Author[]> => 
    fetchApi<Author[]>('/authors'),

  getById: (id: number): Promise<AuthorWithBooks> => 
    fetchApi<AuthorWithBooks>(`/authors/${id}`),

  create: (data: AuthorFormData): Promise<AuthorWithBooks> =>
    fetchApi<AuthorWithBooks>('/authors', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: AuthorFormData): Promise<AuthorWithBooks> =>
    fetchApi<AuthorWithBooks>(`/authors/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number): Promise<void> =>
    fetchApi<void>(`/authors/${id}`, {
      method: 'DELETE',
    }),
};

// ============== Book API ==============
export const bookApi = {
  getAll: (): Promise<Book[]> => 
    fetchApi<Book[]>('/books'),

  getById: (id: number): Promise<Book> => 
    fetchApi<Book>(`/books/${id}`),

  create: (data: BookFormData): Promise<Book> =>
    fetchApi<Book>('/books', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  update: (id: number, data: BookFormData): Promise<Book> =>
    fetchApi<Book>(`/books/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    }),

  delete: (id: number): Promise<void> =>
    fetchApi<void>(`/books/${id}`, {
      method: 'DELETE',
    }),
};

// ============== Publisher API ==============
export const publisherApi = {
  getAll: (): Promise<Publisher[]> => 
    fetchApi<Publisher[]>('/publishers'),

  getById: (id: number): Promise<Publisher> => 
    fetchApi<Publisher>(`/publishers/${id}`),
};

// ============== Genre API ==============
export const genreApi = {
  getAll: (): Promise<Genre[]> => 
    fetchApi<Genre[]>('/genres'),

  getById: (id: number): Promise<Genre> => 
    fetchApi<Genre>(`/genres/${id}`),
};
