# Tyler Khin
# book_routes.py
# Date: April 17th, 2025
# This is where all the routes and a few functions are defined

# Import flask and its functions, the database, and the requests library
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import db, Book
import requests

# Create the blueprint
book_bp = Blueprint("book_bp", __name__)


# Helper function for database
def serialize_book(book):
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "genre": book.genre,
        "status": book.status,
        "rating": book.rating,
        "notes": book.notes,
    }


# Homepage route index.html, displays a list of books
@book_bp.route("/", methods=["GET"])
def get_books():
    books = Book.query.with_entities(
        Book.id, Book.title, Book.author, Book.status
    ).all()
    print("Books from DB:", books)

    books = [
        (b.id, b.title, b.author, (b.status and b.status.lower() == "read"))
        for b in books
    ]
    return render_template("index.html", books=books)


# Goes to add.html, adds a new book
@book_bp.route("/add", methods=["GET", "POST"])
def add_books():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        genre = request.form.get("genre")
        status = request.form.get("status")  # e.g., 'read' or 'unread'
        rating = request.form.get("rating")
        notes = request.form.get("notes")

        new_book = Book(
            title=title,
            author=author,
            genre=genre,
            status=status,
            rating=float(rating) if rating else None,
            notes=notes,
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("book_bp.get_books"))

    return render_template("add.html")


# Goes to edit.html, edits a book's info and updates database
@book_bp.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_books(id):
    book = Book.query.get_or_404(id)

    if request.method == "POST":
        book.genre = request.form.get("genre")
        book.status = request.form.get("status")
        rating = request.form.get("rating")
        book.rating = float(rating) if rating else None

        db.session.commit()
        return redirect(url_for("book_bp.get_books"))

    return render_template("edit.html", book=book)


# Deletes a book from the homepage and database
@book_bp.route("/delete/<int:id>", methods=["POST"])
def delete_books(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({"status": "success"})


# Goes to book_list.html, displays a specific book's info
@book_bp.route("/view/<int:id>", methods=["GET"])
def view_books(id):
    book = Book.query.get(id)
    return render_template("book_list.html", book=book)


# Calls the API in add.html, searches for books and displays 5 results
@book_bp.route("/search", methods=["GET"])
def search_books():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Parameter 'q' is required"}), 400

    api_url = "https://www.googleapis.com/books/v1/volumes"
    params = {"q": query, "maxResults": 5}
    response = requests.get(api_url, params=params)

    if response.status_code != 200:
        return jsonify({"error": "Google Books API error"}), 500

    data = response.json()
    results = []
    for item in data.get("items", []):
        info = item.get("volumeInfo", {})
        results.append(
            {
                "title": info.get("title"),
                "author": ", ".join(info.get("authors", [])),
                "genre": ", ".join(info.get("categories", [])),
                "description": info.get("description", "").strip(),
                "rating": info.get("averageRating"),
                "ratingsCount": info.get("ratingsCount"),
                "image": info.get("imageLinks", {}).get("thumbnail", ""),
            }
        )
    return jsonify(results)


# Marks a book as read
@book_bp.route("/mark-read/<int:book_id>", methods=["POST"])
def mark_read(book_id):
    book = Book.query.get_or_404(book_id)
    book.status = "read"
    db.session.commit()
    return jsonify({"status": "success"})
