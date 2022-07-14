
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)

class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=False)
    reading = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, price, author, description, reading):
        self.name = name
        self.price = price
        self.author = author
        self.description = description
        self.reading = reading

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "author", "description","reading")

book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route("/book/add", methods=["POST"])
def add_book():
    name = request.json.get("name")
    description = request.json.get("description")
    author = request.json.get("author")
    price = request.json.get("price")
    reading = request.json.get("reading")

    record = Books(name, price, author, description, reading)
    db.session.add(record)
    db.session.commit()

    return jsonify(book_schema.dump(record))


@app.route("/book/get", methods=["GET"])
def get_all_books():
    all_books = Books.query.all()
    return jsonify(books_schema.dump(all_books))

@app.route("/books/<id>", methods=["DELETE"])
def book_id(id):
    book = Books.query.get(id)
    db.session.del





if __name__ == "__main__":
    app.run(debug=True)



