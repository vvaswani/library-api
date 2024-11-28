package main

import (
	"database/sql"
	"log"

	//"main/ent"
	"main/handlers"
	"net/http"

	//entsql "entgo.io/ent/dialect/sql"
	_ "github.com/lib/pq"
)

func main() {
	connStr := "postgres://postgres:secret@localhost:5432/app?sslmode=disable"
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	/*
		drv := entsql.OpenDB("postgres", db)
		ent := ent.NewClient(ent.Driver(drv))

		bh := handlers.NewBookHandler(ent)
	*/
	bh := handlers.NewBookHandler(db)
	mux := http.NewServeMux()
	mux.HandleFunc("GET /books/{id}", bh.GetBook)
	mux.HandleFunc("GET /books", bh.GetBooks)
	//mux.HandleFunc("POST /books", bh.CreateBook)
	//mux.HandleFunc("DELETE /books/{id}", bh.DeleteBook)
	//mux.HandleFunc("PUT /books/{id}", bh.UpdateBook)

	log.Printf("Server is running on :8080")
	if err := http.ListenAndServe(":8080", mux); err != nil {
		log.Fatal(err)
	}
}
