# Tyler Khin
# models.py
# Date: April 17th, 2025
# This is where the database is defined

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Initialize the database
db = SQLAlchemy()


# Define the Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    status = db.Column(db.String(20))
    rating = db.Column(db.Float)
    notes = db.Column(db.Text)
