from flask import Flask

app = Flask(__name__)

@app.route('/home')
def random_func_name():
    return "Hello World!" + random_func_2()

@app.route('/blah')
def random_func_2():
    return "sample text"

if __name__ == '__main__':
    app.run(debug=True)