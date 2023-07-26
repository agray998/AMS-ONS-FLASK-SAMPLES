from flask import Flask
from random import choice

first_names = ["alice", "bob", "charlotte", "dwayne", "edna", "fahad", "gwen", "herbert"]
last_names = ["smith", "jones", "roberts", "wright", "cooper", "williams", "francis", "clarkson"]

app = Flask(__name__)

@app.route('/')
def index():
    return "Random Name Generator"

@app.route('/generate')
def generate():
    return choice(first_names) + " " + choice(last_names)

if __name__ == '__main__':
    app.run(debug=True)