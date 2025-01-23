from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)

DATA_FILE = "books.json"

def load_books():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_books(books):
    with open(DATA_FILE, "w") as file:
        json.dump(books, file, indent=4)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or not data.get("заголовок") or not data.get("автор"):
        abort(400, "Название и Автор являются обязательными полями")

    new_book = {
        "id": len(load_books()) + 1,
        "заголовок": data["заголовок"],
        "автор": data["автор"],
        "год": data.get("год"),
        "жанр": data.get("жанр")
    }

    books = load_books()
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201

@app.route("/books", methods=["GET"])
def get_books():
    books = load_books()
    return jsonify(books), 200

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    books = load_books()
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        abort(404, f"Книга с ID {book_id} не найдена")
    return jsonify(book), 200

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()
    books = load_books()
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        abort(404, f"Книга с ID {book_id} не найдена")

    book["заголовок"] = data.get("заголовок", book["заголовок"])
    book["автор"] = data.get("автор", book["автор"])
    book["год"] = data.get("год", book["год"])
    book["жанр"] = data.get("жанр", book["жанр"])

    save_books(books)
    return jsonify(book), 200

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()
    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        abort(404, f"Книга с ID {book_id} не найдена")

    books.remove(book)
    save_books(books)
    return jsonify({"message": "Книга удалена"}), 200

if __name__ == "__main__":
    app.run(debug=True)