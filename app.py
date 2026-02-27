from flask import jsonify, request, make_response
from flask_restful import Resource

from config import app, db, api

from models import User, BookCopy, BookRequest


@app.route('/api/books')
def get_books():
    books = BookCopy.query.all()
    return make_response(jsonify([book.to_dict() for book in books]), 200)


@app.route('/api/users')
def get_users():
    users = User.query.all()
    return make_response(jsonify([user.to_dict() for user in users]), 200)


@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return make_response(jsonify(user.to_dict()), 200)
    else:
        return make_response(jsonify({"error": "User not found"}), 404)


@app.route("/api/users/<int:user_id>/pending_requests")
def get_incoming_requests(user_id):
    requests = (
        BookRequest.query
        .join(BookCopy)
        .filter(BookCopy.owner_id == user_id)
        .all()
    )

    requests_json = [r.to_dict() for r in requests]

    return make_response(jsonify(requests_json), 200)

@app.route('/api/book_requests')
def get_book_requests():
    book_requests = BookRequest.query.all()
    return make_response(jsonify([request.to_dict() for request in book_requests]), 200)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
