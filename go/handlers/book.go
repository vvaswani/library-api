package handlers

import (
	"database/sql"
	"encoding/json"
	"log"
	"strconv"

	//"main/ent"
	"main/repositories"
	"net/http"
)

type BookHandler struct {
	db *sql.DB
}

func NewBookHandler(db *sql.DB) *BookHandler {
	return &BookHandler{db: db}
}

func (h BookHandler) GetBooks(w http.ResponseWriter, r *http.Request) {
	rp := repositories.NewBookRepository(h.db)
	books, err := rp.GetBooks()
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error finding books", err)
		return
	}

	h.writeResponse(w, http.StatusOK, books)
}

func (h BookHandler) GetBook(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.handleError(w, http.StatusBadRequest, "Invalid book ID", err)
		return
	}
	rp := repositories.NewBookRepository(h.db)
	book, err := rp.GetBook(id)
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error finding book", err)
		return
	}

	h.writeResponse(w, http.StatusOK, book)
}

func (h BookHandler) writeResponse(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
	}
}

func (h BookHandler) handleError(w http.ResponseWriter, status int, message string, err error) {
	log.Printf("%s: %v", message, err)
	h.writeResponse(w, status, map[string]string{"error": message})
}

/*
type BookHandler struct {
	ent *ent.Client
}

func NewBookHandler(ent *ent.Client) *BookHandler {
	return &BookHandler{ent: ent}
}

// writeResponse sends a JSON response with the specified status code.
func (h BookHandler) writeResponse(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)

	if err := json.NewEncoder(w).Encode(data); err != nil {
		log.Printf("Error encoding JSON response: %v", err)
	}
}

// handleError sends an error response as JSON.
func (h BookHandler) handleError(w http.ResponseWriter, status int, message string, err error) {
	log.Printf("%s: %v", message, err)
	h.writeResponse(w, status, map[string]string{"error": message})
}

func (h BookHandler) GetBook(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id") // Adjust this based on how you handle path parameters
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.handleError(w, http.StatusBadRequest, "Invalid book ID", err)
		return
	}

	rp := repositories.NewBookRepository(h.ent)
	book, err := rp.GetBook(id)
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error finding book", err)
		return
	}

	h.writeResponse(w, http.StatusOK, book)
}

func (h BookHandler) GetBooks(w http.ResponseWriter, r *http.Request) {
	rp := repositories.NewBookRepository(h.ent)
	books, err := rp.GetBooks()
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error finding books", err)
		return
	}

	h.writeResponse(w, http.StatusOK, books)
}

func (h BookHandler) CreateBook(w http.ResponseWriter, r *http.Request) {
	var b ent.Book
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		h.handleError(w, http.StatusBadRequest, "Error decoding JSON request", err)
		return
	}

	rp := repositories.NewBookRepository(h.ent)
	book, err := rp.CreateBook(b)
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error creating book", err)
		return
	}

	w.Header().Set("Location", fmt.Sprintf("/books/%d", book.ID))
	h.writeResponse(w, http.StatusCreated, book)
}

func (h BookHandler) UpdateBook(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.handleError(w, http.StatusBadRequest, "Invalid book ID", err)
		return
	}

	var b ent.Book
	if err := json.NewDecoder(r.Body).Decode(&b); err != nil {
		h.handleError(w, http.StatusBadRequest, "Error decoding JSON request", err)
		return
	}

	rp := repositories.NewBookRepository(h.ent)
	book, err := rp.UpdateBook(id, b)
	if err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error updating book", err)
		return
	}

	w.Header().Set("Location", fmt.Sprintf("/books/%d", book.ID))
	h.writeResponse(w, http.StatusOK, book)
}

func (h BookHandler) DeleteBook(w http.ResponseWriter, r *http.Request) {
	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		h.handleError(w, http.StatusBadRequest, "Invalid book ID", err)
		return
	}

	rp := repositories.NewBookRepository(h.ent)
	if err := rp.DeleteBook(id); err != nil {
		h.handleError(w, http.StatusInternalServerError, "Error deleting book", err)
		return
	}

	w.WriteHeader(http.StatusNoContent) // 204 No Content
}
*/
