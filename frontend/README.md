# Book Catalog - Frontend

A React-based web application for managing a catalog of books and authors. Built with TypeScript, Vite, and modern React practices.

##  Architecture

The frontend follows a component-based architecture:

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── AuthorDetails.tsx # Author info and books display
│   │   ├── AuthorModal.tsx   # Author create/edit form
│   │   ├── BookModal.tsx     # Book create/edit form
│   │   ├── Sidebar.tsx       # Author navigation sidebar
│   │   └── index.ts          # Component exports
│   ├── api.ts                # API service functions
│   ├── types.ts              # TypeScript type definitions
│   ├── App.tsx               # Main application component
│   ├── main.tsx              # Application entry point
│   └── index.css             # Global styles
├── index.html                # HTML template
├── package.json              # Dependencies and scripts
├── tsconfig.json             # TypeScript configuration
└── vite.config.ts            # Vite configuration
```

##  Prerequisites

- Node.js 18.x or higher
- npm or yarn

## Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

## Running the Application

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:3000`

**Note**: Make sure the backend API is running at `http://localhost:8080` before starting the frontend.

##  Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

##  Features

### Author Management
- View list of all authors in the sidebar
- Click an author to view their details and books
- Add new authors via the "Add" button
- Edit existing author information
- Delete authors (only if they have no books)

### Book Management
- View books by selected author
- Click a book to view its full details
- Add new books with:
  - Title
  - Edition
  - Published date
  - Publisher (from predefined list)
  - Genre (from predefined list)
  - Multiple authors
- Edit existing book information
- Delete books

### User Interface
- Responsive sidebar navigation
- Clean and intuitive design
- Modal dialogs for create/edit operations
- Confirmation dialogs for delete operations
- Error handling with user-friendly messages

##  UI Layout

```
┌─────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌────────────────────────────────┐   │
│  │          │  │      Author Header             │   │
│  │  Authors │  ├────────────────────────────────┤   │
│  │  Sidebar │  │    Author Information          │   │
│  │          │  ├────────────────────────────────┤   │
│  │  - Author│  │ ┌─────────────┬──────────────┐ │   │
│  │  - Author│  │ │ Books List  │ Book Details │ │   │
│  │  - Author│  │ │             │              │ │   │
│  │          │  │ │             │              │ │   │
│  └──────────┘  │ └─────────────┴──────────────┘ │   │
│                └────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

##  API Integration

The frontend communicates with the backend API at `http://localhost:8080`. The API service (`api.ts`) provides typed functions for:

- `authorApi`: CRUD operations for authors
- `bookApi`: CRUD operations for books
- `publisherApi`: Read operations for publishers
- `genreApi`: Read operations for genres

## Components

### Sidebar
Displays the list of authors with:
- Add author button
- Clickable author items
- Active state for selected author

### AuthorDetails
Shows selected author information:
- Author name and details
- Edit/Delete buttons
- List of books by the author
- Book details panel

### AuthorModal
Form for creating/editing authors:
- Name field (required)
- Surname field (required)
- Birth year field (optional)

### BookModal
Form for creating/editing books:
- Title field (required)
- Edition field
- Published date picker
- Publisher dropdown
- Genre dropdown
- Author checkboxes (multiple selection)

## Type Safety

The application uses TypeScript with strict mode enabled. All data models are typed:

- `Author` / `AuthorWithBooks`
- `Book` / `BookSummary`
- `Publisher`
- `Genre`
- `AuthorFormData`
- `BookFormData`

## Testing

Manual testing can be performed by:
1. Starting the backend server
2. Starting the frontend development server
3. Testing all CRUD operations through the UI

##  Notes

- Publishers and genres are read-only in the UI (managed via backend)
- Authors cannot be deleted if they have associated books
- Data is fetched from the backend on application startup
