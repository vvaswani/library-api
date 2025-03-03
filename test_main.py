import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .main import create_app
from .dependencies import get_db, database_url
from .models import Base, BookIn
from .repositories import create_book, get_books, get_book, update_book, delete_book

# Test data constants
TEST_BOOKS = [
    {"title": "Carrie", "author": "Stephen King"},
    {"title": "Ready Player One", "author": "Ernest Cline"},
]


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    test_engine = create_engine(database_url)
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


@pytest.fixture
def test_app(test_engine):
    """Create test FastAPI application with test database"""

    def override_get_db():
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=test_engine
        )
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)


class TestMainApp:
    def test_create_app(self, test_app):
        """Test application creation"""
        assert test_app is not None

    def test_database_initialization(self, test_engine):
        """Test database initialization"""
        inspector = inspect(test_engine)
        assert "books" in inspector.get_table_names()

    def test_router_inclusion(self, client):
        """Test router inclusion and basic API endpoint"""
        response = client.get("/api/books/")
        assert response.status_code == 200

    def test_invalid_endpoint(self, client):
        """Test handling of invalid endpoints"""
        response = client.get("/invalid")
        assert response.status_code == 404


# Repository Tests
class TestBookRepository:
    def test_create_book(self, test_db):
        """Test creating a new book"""
        book = create_book(test_db, BookIn(**TEST_BOOKS[0]))
        assert book.title == TEST_BOOKS[0]["title"]
        assert book.author == TEST_BOOKS[0]["author"]
        assert book.id is not None

    def test_get_books(self, test_db):
        """Test getting all books"""
        book1 = create_book(test_db, BookIn(**TEST_BOOKS[0]))
        book2 = create_book(test_db, BookIn(**TEST_BOOKS[1]))

        books = get_books(test_db)
        assert len(books) >= 2
        assert any(b.id == book1.id for b in books)
        assert any(b.id == book2.id for b in books)

    def test_get_book(self, test_db):
        """Test getting a specific book"""
        created_book = create_book(test_db, BookIn(**TEST_BOOKS[0]))
        retrieved_book = get_book(test_db, created_book.id)
        assert retrieved_book is not None
        assert retrieved_book.id == created_book.id
        assert retrieved_book.title == TEST_BOOKS[0]["title"]

    def test_update_book(self, test_db):
        """Test updating a book"""
        book = create_book(test_db, BookIn(**TEST_BOOKS[0]))
        updated_data = BookIn(**TEST_BOOKS[1])
        updated_book = update_book(test_db, book.id, updated_data)
        assert updated_book is not None
        assert updated_book.title == TEST_BOOKS[1]["title"]
        assert updated_book.author == TEST_BOOKS[1]["author"]

    def test_delete_book(self, test_db):
        """Test deleting a book"""
        book = create_book(test_db, BookIn(title="To Delete", author="Author"))
        deleted_book = delete_book(test_db, book.id)

        assert deleted_book is not None
        assert deleted_book.id == book.id
        assert get_book(test_db, book.id) is None

    def test_nonexistent_operations(self, test_db):
        """Test operations on nonexistent books"""
        assert get_book(test_db, 999999) is None
        assert update_book(test_db, 999999, BookIn(title="Test", author="Test")) is None
        assert delete_book(test_db, 999999) is None


class TestBookRouter:
    def test_create_book_success(self, client):
        """Test successful book creation"""
        response = client.post("/api/books/", json=TEST_BOOKS[0])
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == TEST_BOOKS[0]["title"]
        assert data["author"] == TEST_BOOKS[0]["author"]
        assert "id" in data

    def test_create_book_invalid_data(self, client):
        """Test book creation with invalid data"""
        response = client.post("/api/books/", json={"title": ""})
        assert response.status_code == 422

    def test_get_books_success(self, client, test_db):
        """Test getting list of books"""
        # Create test books
        for book_data in TEST_BOOKS:
            client.post("/api/books/", json=book_data)

        response = client.get("/api/books/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert isinstance(data, list)
        assert any(book["title"] == TEST_BOOKS[0]["title"] for book in data)
        assert any(book["title"] == TEST_BOOKS[1]["title"] for book in data)

    def test_get_books_pagination(self, client):
        """Test books list pagination"""
        response = client.get("/api/books/?skip=1&limit=1")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 1

    def test_get_book_by_id_success(self, client):
        """Test getting a specific book"""
        create_response = client.post("/api/books/", json=TEST_BOOKS[0])
        book_id = create_response.json()["id"]

        response = client.get(f"/api/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == TEST_BOOKS[0]["title"]
        assert data["author"] == TEST_BOOKS[0]["author"]

    def test_get_book_not_found(self, client):
        """Test getting a non-existent book"""
        response = client.get("/api/books/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"

    def test_update_book_success(self, client):
        """Test successful book update"""
        # Create initial book
        create_response = client.post("/api/books/", json=TEST_BOOKS[0])
        book_id = create_response.json()["id"]

        # Update to second book data
        response = client.put(f"/api/books/{book_id}", json=TEST_BOOKS[1])
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id
        assert data["title"] == TEST_BOOKS[1]["title"]
        assert data["author"] == TEST_BOOKS[1]["author"]

    def test_update_book_not_found(self, client):
        """Test updating a non-existent book"""
        book_data = {"title": "Updated Title", "author": "Updated Author"}
        response = client.put("/api/books/99999", json=book_data)
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"

    def test_delete_book_success(self, client):
        """Test successful book deletion"""
        create_response = client.post("/api/books/", json=TEST_BOOKS[0])
        book_id = create_response.json()["id"]

        response = client.delete(f"/api/books/{book_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book_id

        # Verify book is deleted
        get_response = client.get(f"/api/books/{book_id}")
        assert get_response.status_code == 404

    def test_delete_book_not_found(self, client):
        """Test deleting a non-existent book"""
        response = client.delete("/api/books/99999")
        assert response.status_code == 404
        assert response.json()["detail"] == "Book not found"
