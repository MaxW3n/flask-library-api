from flask import Flask, jsonify, request
from supabase import create_client, Client
from dotenv import load_dotenv
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

#POST requests: Create R U D
@app.route('/books', methods=['POST'])
def create_book():
    new_book = request.get_json()
    
    if 'title' not in new_book or 'author' not in new_book:
        return jsonify({'error': 'Missing title or author'}), 400
 
    response = supabase.table("books").insert({
        'title': new_book['title'],
        'author': new_book['author']
    }).execute()

    return jsonify(response.data[0]), 201

#GET requests: C Read U D
@app.route('/books')
def get_books():
    response = supabase.table("books").select("*").execute()
    
    return jsonify({
        'books': response.data
    })

@app.route('/books/<int:book_id>')
def get_book(book_id):
    response = supabase.table("books").select("*").eq('id', book_id).execute()
    if len(response.data) == 0:
        return jsonify({'message': 'Book not found'}), 404
    
    return jsonify(response.data[0]), 200

#PUT requests: C R Update D
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    update_data = request.get_json()
    
    # Validate
    if 'title' not in update_data or 'author' not in update_data:
        return jsonify({'error': 'Missing title or author'}), 400

    response = supabase.table('books').update({
        'title': update_data['title'],
        'author': update_data['author']
    }).eq('id', book_id).execute()

    if len(response.data) == 0:
        return jsonify({'message': 'Book not found'}), 404

    return jsonify(response.data[0]), 200

#DELETE requests: C R U Delete
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    response = supabase.table('books').delete().eq('id', book_id).execute()
    
    if len(response.data) == 0:
        return jsonify({'message': 'Book not found'}), 404

    return jsonify({'message': 'Book deleted'}), 200

# Run the app
if __name__ == '__main__':
    app.run()