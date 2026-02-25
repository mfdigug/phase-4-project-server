from flask import jsonify, request
from flask_restful import Resource

from config import app, db, api

from models import User, BookCopy, BookRequest


@app.route('/api/books')
def get_books():
    return jsonify({
        "books": [
            "Book 1",
            "Book 2",
            "Book 3"
        ]
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
