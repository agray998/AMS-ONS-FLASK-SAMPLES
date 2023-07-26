class Book():
    books = []

    @staticmethod
    def initialise_list(bookfile):
        with open(bookfile, 'r') as file:
            for book in file:
                eval(book)

    def __init__(self, title, pages, isbn, genre, fromrepr = False, author = "Unknown", bookfile = "books.list"):
        self.title = title
        self.pages = pages
        self.isbn = isbn
        self.genre = genre
        self.author = author
        Book.books.append(self)
        if not fromrepr:
            with open(bookfile, 'a') as file:
                file.write(self.__repr__() + '\n')
    
    @staticmethod
    def valid_isbn(isbn):
        digits = ''.join(isbn.split('-'))
        if len(digits) != 13:
            return False
        diglist = [int(digit) for digit in digits]
        return ((sum([diglist[i] for i in range(12) if i % 2 == 0]) + 3 * sum([diglist[i] for i in range(12) if i % 2 != 0]) + diglist[-1]) % 10) == 0
    
    @staticmethod
    def search(author):
        return list(filter(lambda book: book.author == author, Book.books))

    def __str__(self):
        return f"Written by {self.author}, {self.title} is a gripping {self.pages}-page {self.genre} novel"
    
    def __repr__(self):
        return f"Book('{self.title}', {self.pages}, '{self.isbn}', '{self.genre}', fromrepr=True, author='{self.author}')"
