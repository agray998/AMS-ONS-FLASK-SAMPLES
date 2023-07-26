from application import app
from application.book import Book
from flask import request
from random import choice

def book_builder(book):
    return {
        "isbn": book.isbn,
        "title": book.title,
        "by": book.author,
        "genre": book.genre,
        "pages": book.pages
        }

@app.route('/')
def index():
    return '''
    Library Management System<br>
    Endpoints:<br>
    /search -> search for books by author<br>
    /new -> add a new book<br>
    /update -> update a book<br>
    /delete -> delete a book<br>
    /validate -> check the validity of an ISBN
    '''

@app.route('/search')
def search():
    author = request.args.get("author")
    return list(map(book_builder, Book.search(author)))

@app.route('/new')
def create():
    book = Book(**request.args, fromrepr=True)
    return f"Added new book: {str(book)}"

@app.route('/update/<isbn>')
def update(isbn):
    for book in Book.books:
        if book.isbn.replace("-", "") == isbn.replace("-", ""):
            book.title = request.args.get("title", book.title)
            book.author = request.args.get("author", book.author)
            book.genre = request.args.get("genre", book.genre)
            book.pages = int(request.args.get("pages", book.pages))
            break
    return f"Updated book with ISBN: {isbn}"

@app.route('/delete/<isbn>')
def delete(isbn):
    for i, book in enumerate(Book.books):
        if book.isbn.replace("-", "") == isbn.replace("-", ""):
            del Book.books[i]
            break
    return f"Deleted book with ISBN: {isbn}"

@app.route('/validate/<isbn>')
def validate_isbn(isbn):
    return {
        "isbn": isbn,
        "valid": Book.valid_isbn(isbn)
    }

@app.route('/suggested')
def suggestion():
    genre = request.args.get("genre", "")
    options = list(filter(lambda b: b.genre == genre, Book.books))
    return book_builder(choice(options if genre else Book.books))