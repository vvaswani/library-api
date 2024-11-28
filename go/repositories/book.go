package repositories

import (
	"database/sql"
	"fmt"
	"main/models"
	// "main/ent"
	// "main/ent/book"
)

type BookRepository struct {
	db *sql.DB
}

// NewBookRepository creates a new instance of BookRepository.
func NewBookRepository(db *sql.DB) *BookRepository {
	return &BookRepository{db: db}
}

// GetBook retrieves a book by its ID.
func (r *BookRepository) GetBook(id int) (*models.Book, error) {
	var book models.Book
	row := r.db.QueryRow("SELECT id, title, author FROM book WHERE id = $1", id)

	err := row.Scan(&book.Id, &book.Title, &book.Author)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("no such book with ID %d", id)
		}
		return nil, fmt.Errorf("error retrieving book with ID %d: %w", id, err)
	}
	return &book, nil
}

// GetBooks retrieves all books.
func (r *BookRepository) GetBooks() ([]*models.Book, error) {
	rows, err := r.db.Query("SELECT id, title, author FROM book")
	if err != nil {
		return nil, fmt.Errorf("error retrieving books: %w", err)
	}
	defer rows.Close()

	var books []*models.Book
	for rows.Next() {
		var book models.Book
		if err := rows.Scan(&book.Id, &book.Title, &book.Author); err != nil {
			return nil, fmt.Errorf("error scanning book: %w", err)
		}
		books = append(books, &book)
	}

	if err = rows.Err(); err != nil {
		return nil, fmt.Errorf("error iterating over books: %w", err)
	}
	return books, nil
}

// CreateBook inserts a new book record.
func (r *BookRepository) CreateBook(b models.Book) (*models.Book, error) {
	result, err := r.db.Exec("INSERT INTO books (title, author) VALUES ($1, $2) RETURNING id", b.Title, b.Author)
	if err != nil {
		return nil, fmt.Errorf("error creating book: %w", err)
	}

	id, err := result.LastInsertId()
	if err != nil {
		return nil, fmt.Errorf("error retrieving last insert ID: %w", err)
	}

	b.Id = int(id)
	return &b, nil
}

// DeleteBook deletes a book by its ID.
func (r *BookRepository) DeleteBook(id int) error {
	result, err := r.db.Exec("DELETE FROM books WHERE id = $1", id)
	if err != nil {
		return fmt.Errorf("error deleting book with ID %d: %w", id, err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("error checking rows affected for ID %d: %w", id, err)
	}
	if rowsAffected == 0 {
		return fmt.Errorf("no book found with ID %d", id)
	}
	return nil
}

// UpdateBook updates an existing book record.
func (r *BookRepository) UpdateBook(id int, b models.Book) (*models.Book, error) {
	result, err := r.db.Exec("UPDATE books SET title = $1, author = $2 WHERE id = $3", b.Title, b.Author, id)
	if err != nil {
		return nil, fmt.Errorf("error updating book with ID %d: %w", id, err)
	}

	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return nil, fmt.Errorf("error checking rows affected for ID %d: %w", id, err)
	}
	if rowsAffected == 0 {
		return nil, fmt.Errorf("no book found with ID %d", id)
	}
	b.Id = id
	return &b, nil
}

/*
type BookRepository struct {
	ent *ent.Client
}

func NewBookRepository(ent *ent.Client) *BookRepository {
	return &BookRepository{ent: ent}
}

func (r BookRepository) GetBook(id int) (*ent.Book, error) {
	ctx := context.Background()
	b, err := r.ent.Book.
		Query().
		Where(book.ID(id)).
		Only(ctx)

	if err != nil {
		return nil, fmt.Errorf("no such book with ID %d: %w", id, err)
	}
	return b, nil
}

func (r BookRepository) GetBooks() ([]*ent.Book, error) {
	ctx := context.Background()
	books, err := r.ent.Book.
		Query().
		All(ctx)

	if err != nil {
		return nil, fmt.Errorf("error retrieving books: %w", err)
	}
	return books, nil
}

func (r BookRepository) CreateBook(b ent.Book) (*ent.Book, error) {
	ctx := context.Background()
	book, err := r.ent.Book.
		Create().
		SetAuthor(b.Author).
		SetTitle(b.Title).
		Save(ctx)

	if err != nil {
		return nil, fmt.Errorf("error creating book: %w", err)
	}
	return book, nil
}

func (r BookRepository) DeleteBook(id int) error {
	ctx := context.Background()
	err := r.ent.Book.
		DeleteOneID(id).
		Exec(ctx)

	if err != nil {
		return fmt.Errorf("error deleting book with ID %d: %w", id, err)
	}
	return nil
}

// UpdateBook updates an existing book record.
func (r BookRepository) UpdateBook(id int, b ent.Book) (*ent.Book, error) {
	ctx := context.Background()
	book, err := r.ent.Book.
		UpdateOneID(id).
		SetAuthor(b.Author).
		SetTitle(b.Title).
		Save(ctx)

	if err != nil {
		return nil, fmt.Errorf("error updating book with ID %d: %w", id, err)
	}
	return book, nil
}
*/
