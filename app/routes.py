from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request



# hello_world_bp = Blueprint("hello_world", __name__)

# @hello_world_bp.route("/hello-world", methods=["GET"])
# def say_hello_world():
#     my_beautiful_response_body = "Hello, World!"
#     return my_beautiful_response_body

# @hello_world_bp.route("/hello/JSON", methods=["GET"])
# def say_hello_json():
#     return {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }

# @hello_world_bp.route("/broken-endpoint-with-broken-server-code")
# def broken_endpoint():
#     response_body = {
#         "name": "Ada Lovelace",
#         "message": "Hello!",
#         "hobbies": ["Fishing", "Swimming", "Watching Reality Shows"]
#     }
#     new_hobby = "Surfing"
#     response_body["hobbies"].append(new_hobby)
#     return response_body

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ] 

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["POST"])
def create_books():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return jsonify({"message": "missing data"}),400
    new_book = Book(title=request_body["title"],description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return f"Book {new_book.title} successfully created", 201


@books_bp.route("", methods=["GET"])
def handle_books():
    books=Book.query.all()
    books_response = []
    for book in books:
        books_response.append(book.fill_the_dict())
       
    return jsonify(books_response),200

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book_id = int(book_id)
    book=Book.query.get(book_id)
    if book is None:
        return {"Error": f"Book {book_id} was Not Found"},404
    if request.method == "GET":
        return jsonify(book.fill_the_dict())
    elif request.method =="PUT":
        required_data=request.get_json()
        book.title=required_data["title"]
        book.description=required_data["description"]
        db.session.commit()
        return jsonify(book.fill_the_dict()),200
    elif request.method=="DELETE":
        db.session.delete(book)
        db.session.commit()
        return make_response(f"Book {book.id}  Successfully deleted"),200
        
        

