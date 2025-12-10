/**
 * Type definitions for the Book Catalog application
 */

export interface Author {
  id: number;
  name: string;
  surname: string;
  birthyear?: number;
}

export interface AuthorWithBooks extends Author {
  books: BookSummary[];
}

export interface BookSummary {
  id: number;
  title: string;
}

export interface Book {
  id: number;
  title: string;
  edition?: string;
  published_date?: string;
  publisher_id?: number;
  genre_id?: number;
  authors: Author[];
  publisher?: Publisher;
  genre?: Genre;
}

export interface Publisher {
  id: number;
  name: string;
  website?: string;
  description?: string;
  creation_date?: string;
}

export interface Genre {
  id: number;
  name: string;
  description?: string;
}

export interface AuthorFormData {
  name: string;
  surname: string;
  birthyear?: number;
}

export interface BookFormData {
  title: string;
  edition?: string;
  published_date?: string;
  publisher_id?: number;
  genre_id?: number;
  author_ids: number[];
}
