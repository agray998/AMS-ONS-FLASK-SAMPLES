from application import app
from application.book import *
from flask import request

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
    return "Library Management System"

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
        if book.isbn == isbn:
            book.title = request.args.get("title", book.title)
            book.author = request.args.get("author", book.author)
            book.genre = request.args.get("genre", book.genre)
            book.pages = int(request.args.get("pages", book.pages))
            break
    return f"Updated book with ISBN: {isbn}"

@app.route('/delete/<isbn>')
def delete(isbn):
    for i, book in enumerate(Book.books):
        if book.isbn == isbn:
            del Book.books[i]
            break
    return f"Deleted book with ISBN: {isbn}"