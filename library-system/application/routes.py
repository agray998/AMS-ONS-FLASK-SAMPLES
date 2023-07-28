from application import app
from application.book import Book
from flask import request
from random import choice

def book_builder(book) -> dict:
    '''
    Creates a serialisable dict from a book object
    '''
    return {
        "isbn": book.isbn,
        "title": book.title,
        "by": book.author,
        "genre": book.genre,
        "pages": book.pages
        }

@app.route('/')
def index() -> str:
    '''
    Overview of available functionality
    '''
    return '''
    Library Management System<br>
    Endpoints:<br>
    /search -> search for books by author<br>
    /new -> add a new book<br>
    /update -> update a book<br>
    /delete -> delete a book<br>
    /validate -> check the validity of an ISBN
    /suggested -> get a random recommendation
    '''

@app.route('/search')
def search() -> list:
    '''
    Returns a list of books (represented as dicts) written by a given author
    Author is specified via query param
    '''
    author = request.args.get("author")
    return list(map(book_builder, Book.search(author)))

@app.route('/new')
def create() -> str:
    '''
    Creates a new book object from info supplied via query params
    Will return custom 403 if the specified ISBN is already taken
    '''
    if request.args.get("isbn") in map(lambda b: b.isbn, Book.books):
        return f"{request.args.get('isbn')} is already in use", 403
    book = Book(**request.args, fromrepr=True)
    return f"Added new book: {str(book)}"

@app.route('/update/<isbn>')
def update(isbn: str) -> str:
    '''
    Finds a book by ISBN and updates the attributes using info from query params
    Any attrs not supplied will default to current values (i.e behaves as a PATCH
    rather than a PUT). Currently does not indicate if ISBN not found - should 
    update to return custom 404
    '''
    for book in Book.books:
        if book.isbn.replace("-", "") == isbn.replace("-", ""):
            book.title = request.args.get("title", book.title)
            book.author = request.args.get("author", book.author)
            book.genre = request.args.get("genre", book.genre)
            book.pages = int(request.args.get("pages", book.pages))
            break
    return f"Updated book with ISBN: {isbn}"

@app.route('/delete/<isbn>')
def delete(isbn: str) -> str:
    '''
    Finds a book by ISBN and deletes it. Currently does not indicate if 
    ISBN not found - should update to return custom 404
    '''
    for i, book in enumerate(Book.books):
        if book.isbn.replace("-", "") == isbn.replace("-", ""):
            del Book.books[i]
            break
    return f"Deleted book with ISBN: {isbn}"

@app.route('/validate/<isbn>')
def validate_isbn(isbn: str) -> dict:
    '''
    Takes an ISBN and returns a dict with:
    - the given isbn
    - the validity of the given ISBN as determined by Book.valid_isbn()
    '''
    return {
        "isbn": isbn,
        "valid": Book.valid_isbn(isbn)
    }

@app.route('/suggested')
def suggestion() -> dict:
    '''
    Selects a random book and returns book details as a dict.
    If a genre is specified as a query param then suggested book 
    will be of that genre - otherwise any book can be returned
    '''
    genre = request.args.get("genre", "")
    options = list(filter(lambda b: b.genre == genre, Book.books))
    return book_builder(choice(options if genre else Book.books))