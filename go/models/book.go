package models

type Book struct {
	Id     int    `db:"id" json:"id"`
	Author string `db:"author" json:"author"`
	Title  string `db:"title" json:"title"`
}
