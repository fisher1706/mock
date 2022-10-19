from flask import Flask


app = Flask(__name__)

from valitor import *


@app.route('/')
def home():
    return "facking with valitor!!!"


if __name__ == '__main__':
    app.run(debug=True)
