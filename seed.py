#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc

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
                username=fake.user_name(),
                email=fake.email()
            )
            users.append(user)
        db.session.add_all(users)
        db.session.commit()

        print("Creating book copies...")
        books = []
        for user in users:
            for _ in range(2):
                book = BookCopy(
                    title=fake.sentence(nb_words=4),
                    author=fake.name(),
                    condition=rc(['New', 'Good', 'Fair', 'Poor']),
                    genre=rc(['Fiction', 'Non-Fiction',
                             'Sci-Fi', 'Fantasy', 'Biography']),
                    owner=user
                )
