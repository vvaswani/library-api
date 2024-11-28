/*
package schema

import (
	"entgo.io/ent"
	"entgo.io/ent/dialect/entsql"
	"entgo.io/ent/schema"
	"entgo.io/ent/schema/field"
)

// Book holds the schema definition for the Book entity.
type Book struct {
	ent.Schema
}

func (Book) Annotations() []schema.Annotation {
	return []schema.Annotation{
		entsql.Annotation{Table: "book"},
	}
}

// Fields of the Book.
func (Book) Fields() []ent.Field {
	return []ent.Field{
		field.Int("id").
			Positive(),
		field.String("author").
			Default(""),
		field.String("title").
			Default(""),
	}
}

// Edges of the Book.
func (Book) Edges() []ent.Edge {
	return nil
}
*/
