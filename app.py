from flask import jsonify, request, make_response
from flask_restful import Resource

from config import app, db, api

from models import User, BookCopy, BookRequest


class Books(Resource):
    def get(self):
        return make_response(jsonify([book.to_dict() for book in BookCopy.query.all()]), 200)

    def post(self):
        data = request.get_json()
        new_book = BookCopy(
            title=data['title'],
            author=data['author'],
            condition=data['condition'],
            genre=data['genre'],
            owner_id=data['owner_id'],
            image=data.get('image')
        )
        db.session.add(new_book)
        db.session.commit()
        return make_response(jsonify(new_book.to_dict()), 201)

    def delete(self, id):
        record = BookCopy.query.filter(BookCopy.id == id).first()
        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted "}

        response = make_response(
            response_dict,
            200
        )
        return response


api.add_resource(Books, '/api/books')


class Users(Resource):
    def get(self):
        return make_response(jsonify([user.to_dict() for user in User.query.all()]), 200)


api.add_resource(Users, '/api/users')


class UserByID(Resource):
    def get_user(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)


api.add_resource(UserByID, '/api/users/<int:id>')


class UserRequests(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if user:
            requests = BookRequest.query.join(
                BookCopy).filter(BookCopy.owner_id == id).all()
            return make_response(jsonify([request.to_dict() for request in requests]), 200)
        else:
            return make_response(jsonify({"error": "User not found"}), 404)


api.add_resource(UserRequests, '/api/users/<int:id>/pending_requests')


class BookRequests(Resource):
    def post(self):
        data = request.get_json()

        existing = BookRequest.query.filter_by(
            requester_id=data['requester_id'],
            book_copy_id=data['book_copy_id']
        ).first()

        if existing:
            return make_response(jsonify({"error": "Request already exists"}), 400)

        new_request = BookRequest(
            requester_id=data['requester_id'],
            book_copy_id=data['book_copy_id']
        )
        db.session.add(new_request)
        db.session.commit()

        return make_response(jsonify(new_request.to_dict()), 201)


api.add_resource(BookRequests, '/api/book_requests')


class BookRequestByID(Resource):
    def delete(self, id):
        request_record = BookRequest.query.filter(BookRequest.id == id).first()

        if not request_record:
            return make_response(jsonify({"error": "Request not found"}), 404)

        db.session.delete(request_record)
        db.session.commit()

        return make_response(jsonify({"message": "Request successfully deleted"}), 200)


api.add_resource(BookRequestByID, '/api/book_requests/<int:id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
