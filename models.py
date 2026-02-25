from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql import func


from config import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-book_copies.owner', '-book_requests.requester')
    # -book_copies.owner -> don't call the owner again
    # -book_requests.requester -> don't call the requester again

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    book_copies = db.relationship('BookCopy', backref='owner')
    # user.book_copies -> list of BookCopy objects owned by the user
    book_requests = db.relationship('BookRequest', backref='requester')
    # user.book_requests -> list of BookRequest objects made by the user

    def __repr__(self):
        return f'<User {self.username}>'


class BookCopy(db.Model, SerializerMixin):
    __tablename__ = 'book_copies'

    serialize_rules = ('-owner.book_copies',  # don't call all books again
                       '-book_requests.book_copy')  # don't call the book copy again for each request

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    condition = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    image = db.Column(db.String, nullable=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # let's you do book_copy.owner -> returns user object
    book_requests = db.relationship('BookRequest', backref='book_copy')
    # book_copy.book_requests -> list of BookRequest objects for this book copy

    def __repr__(self):
        return f'<BookCopy {self.title} by {self.author}, owned by User ID {self.owner_id}>'


class BookRequest(db.Model, SerializerMixin):
    __tablename__ = 'book_requests'

    serialize_rules = ('-requester.book_requests',  # don't call all requests again
                       '-book_copy.book_requests',  # don't call all requests for the book copy again
                       '-book_copy.owner')  # don't call the owner of the book copy again

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    status = db.Column(db.String(20), default='pending')

    requester_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    book_copy_id = db.Column(db.Integer, db.ForeignKey(
        'book_copies.id'), nullable=False)

    # Relationships: backrefs handle requester and book_copy automatically
    requester = db.relationship('User')
    book_copy = db.relationship('BookCopy')

    def __repr__(self):
        return f'<BookRequest {self.id} by User ID {self.requester_id} for BookCopy ID {self.book_copy_id}>'
