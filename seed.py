#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc, sample

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, BookCopy, BookRequest


if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        print("Clearing existing data...")
        BookRequest.query.delete()
        BookCopy.query.delete()
        User.query.delete()
        db.session.commit()

        # Create 10 users
        print("Creating users...")
        users = []
        for _ in range(10):
            user = User(
                username=fake.unique.user_name(),
                email=fake.unique.email()
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        # Create books & assign owners
        print("Creating book copies...")
        books = []
        for user in users:
            for _ in range(2):
                book = BookCopy(
                    title=fake.unique.sentence(nb_words=4).rstrip('.'),
                    author=fake.name(),
                    condition=rc(['New', 'Good', 'Fair', 'Poor']),
                    genre=rc(['Fiction', 'Non-Fiction',
                             'Sci-Fi', 'Fantasy', 'Biography']),
                    is_available=True,
                    image=f"https://picsum.photos/200/300?random={randint(1,100)}",
                    owner=user
                )
                books.append(book)

        db.session.add_all(books)
        db.session.commit()

        # create requests
        print("Creating book requests...")
        all_requests = []
        for user in users:
            available_books = [
                b for b in books if b.is_available and b.owner != user]
            num_requests = randint(3, 5)
            requested_books = sample(available_books, num_requests)
            for book in requested_books:
                request = BookRequest(
                    requester=user,
                    book_copy=book,
                    status="pending"
                )

                all_requests.append(request)

        db.session.add_all(all_requests)
        db.session.commit()
