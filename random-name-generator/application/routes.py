from application import app
from flask import request
from random import choice

first_names = ["alice", "bob", "charlotte", "dwayne", "edna", "fahad", "gwen", "herbert"]
last_names = ["smith", "jones", "roberts", "wright", "cooper", "williams", "francis", "clarkson"]

@app.route('/')
def index():
    return "Random Name Generator"

'''
@app.route('/generate/<int:num>')
def generate(num: int):
    return [{"firstname":choice(first_names), "lastname":choice(last_names)} for i in range(num)]
'''

@app.route('/generate')
def generate():
    num = int(request.args.get("num", 1))
    return [{"firstname":choice(first_names), "lastname":choice(last_names)} for i in range(num)]