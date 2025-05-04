# Tyler Khin
# app.py
# Date: April 17th, 2025
# This is the main entry point for the application.

# Import flask and its functions, the database, and the routes
from flask import Flask
from models import db
from routes.book_routes import book_bp

# Create the Flask app
app = Flask(__name__)

# Configure the database; 'sqlite:///books.db' refers to the location of the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

# Register the routes
app.register_blueprint(book_bp)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
