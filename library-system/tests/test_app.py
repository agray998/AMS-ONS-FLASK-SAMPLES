from application.routes import create, search, delete, index, validate_isbn, update, suggestion
from application.book import Book
from flask import request
from application import app

def test_index():
    assert index() == '''
    Library Management System<br>
    Endpoints:<br>
    /search -> search for books by author<br>
    /new -> add a new book<br>
    /update -> update a book<br>
    /delete -> delete a book<br>
    /validate -> check the validity of an ISBN
    /suggested -> get a random recommendation
    '''

def test_create():
    with app.test_request_context():
        request.args = {"isbn": "123-4-56-789012-3", "author":"John Smith", "pages":300, "genre": "sci-fi", "title": "sample book"}
        assert create() == "Added new book: Written by John Smith, sample book is a gripping 300-page sci-fi novel"
        assert len(Book.books) == 1

def test_create_exists():
    Book.books = []
    with app.test_request_context():
        Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
        request.args = {"isbn": "123-4-56-789012-3", "author":"John Smith", "pages":300, "genre": "sci-fi", "title": "sample book"}
        assert create() == ("123-4-56-789012-3 is already in use", 403)
        assert len(Book.books) == 1
    
def test_search():
    Book.books = []
    Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
    Book(isbn="123-4-56-789012-8", title="Blah2", pages=300, genre="sci-fi", fromrepr=True)
    Book(isbn="123-4-56-789012-4", title="sample", pages=223, genre="biography", author="James Roberts", fromrepr=True)
    Book(isbn="123-4-56-789012-6", title="places", pages=100, genre="travel", author="Alice Jones", fromrepr=True)
    with app.test_request_context():
        request.args = {"author": "Unknown"}
        assert search() == [
            {
                "isbn": "123-4-56-789012-3",
                "title": "Blah",
                "by": "Unknown",
                "genre": "fantasy",
                "pages": 200
            },
            {
                "isbn": "123-4-56-789012-8",
                "title": "Blah2",
                "by": "Unknown",
                "genre": "sci-fi",
                "pages": 300
            }
        ]

def test_update():
    Book.books = []
    Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
    with app.test_request_context():
        request.args = {"title": "Updated title"}
        assert update("123-4-56-789012-3") == "Updated book with ISBN: 123-4-56-789012-3"
        assert Book.books[0].title == "Updated title"


def test_delete():
    Book.books = []
    Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
    assert delete("123-4-56-789012-3") == "Deleted book with ISBN: 123-4-56-789012-3"
    assert len(Book.books) == 0
    

def test_valid_isbn():
    assert validate_isbn("123-4-56-789012-3") == {
        "isbn": "123-4-56-789012-3",
        "valid": False
    }
    assert validate_isbn("123-4-56-789012-8") == {
        "isbn": "123-4-56-789012-8",
        "valid": True
    }

def test_suggestion_genre():
    Book.books = []
    Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
    Book(isbn="123-4-56-789012-8", title="Blah2", pages=300, genre="sci-fi", fromrepr=True)
    Book(isbn="123-4-56-789012-4", title="sample", pages=223, genre="fantasy", author="James Roberts", fromrepr=True)
    Book(isbn="123-4-56-789012-6", title="places", pages=100, genre="travel", author="Alice Jones", fromrepr=True)
    with app.test_request_context():
        request.args = {"genre": "fantasy"}
        for _ in range(10):
            b = suggestion()
            assert b.get("genre") == "fantasy"

def test_suggestion_any():
    Book.books = []
    Book(isbn="123-4-56-789012-3", title="Blah", pages=200, genre="fantasy", fromrepr=True)
    Book(isbn="123-4-56-789012-8", title="Blah2", pages=300, genre="sci-fi", fromrepr=True)
    Book(isbn="123-4-56-789012-4", title="sample", pages=223, genre="fantasy", author="James Roberts", fromrepr=True)
    Book(isbn="123-4-56-789012-6", title="places", pages=100, genre="travel", author="Alice Jones", fromrepr=True)
    with app.test_request_context():
        request.args = {}
        for _ in range(10):
            b = suggestion()
            assert isinstance(b, dict)
            assert b.get("by") is not None