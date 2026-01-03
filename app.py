from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
from services.ai_service import AIService
from services.book_service import BookService
import os

# Load environment variables
load_dotenv()

# Create a Flask app
app = Flask(__name__)

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Initialize AI service
ai_service = AIService()

# Initialize Book service
book_service = BookService(supabase)

#POST requests: Create R U D
@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    
    if 'title' not in new_book or 'author' not in new_book:
        return jsonify({'error': 'Missing title or author'}), 400
 
    response = book_service.create_book(new_book['title'], new_book['author'])

    return jsonify(response), 201

#GET requests: C Read U D
@app.route('/books')
def get_books():
    response = book_service.get_books()
    
    return jsonify({
        'books': response
    })

@app.route('/books/<int:book_id>')
def get_book(book_id):
    response = book_service.get_book(book_id)
    if response is None:
        return jsonify({'message': 'Book not found'}), 404
    
    return jsonify(response), 200

#PUT requests: C R Update D
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    update_data = request.get_json()
    
    if 'title' not in update_data or 'author' not in update_data:
        return jsonify({'error': 'Missing title or author'}), 400

    response = book_service.update_book(book_id, title=update_data['title'], author=update_data['author'])

    if response is None:
        return jsonify({'message': 'Book not found'}), 404

    return jsonify(response), 200

#DELETE requests: C R U Delete
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    response = book_service.delete_book(book_id)
    
    if response is None:
        return jsonify({'message': 'Book not found'}), 404

    return jsonify({'message': 'Book deleted'}), 200

#AI requests
@app.route('/books/<int:book_id>/summary', methods=['GET'])
def get_book_summary(book_id):
    book = book_service.get_book(book_id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    print("Book data:", book)
    print("Summary field:", book.get('summary'))

    if book.get('summary'):
        return jsonify({
            'book': book,
            'summary': book['summary'],
            'cached': True
        }), 200
    
    print("Generating summary...")
    summary = ai_service.generate_book_summary(book['title'], book['author'])
    
    print("Summary generated")

    book_service.update_book(book_id, summary=summary)

    return jsonify({
        'book': book,
        'summary': summary,
        'cached': False
    }), 200

@app.route('/books/<int:book_id>/similar', methods=['GET'])
def get_similar_books(book_id):
    book = book_service.get_book(book_id)
    
    if book is None:
        return jsonify({'message': 'Book not found'}), 404
    
    if book.get('similar_books'):
        return jsonify({
            'book': book,
            'similar_books': book['similar_books'],
            'cached': True
        }), 200
    
    similar_books = ai_service.suggest_similar_books(book['title'], book['author'])
    
    book_service.update_book(book_id, similar_books=similar_books)
    
    return jsonify({
        'book': book,
        'similar_books': similar_books,
        'cached': False
    }), 200

# Run the app
if __name__ == '__main__':
    app.run()