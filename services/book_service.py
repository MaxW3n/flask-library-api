from supabase import Client


class BookService:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_book(self, book_id):
        response = self.supabase.table('books').select('title, author').eq('id', book_id).execute()
        
        if len(response.data) == 0:
            return None
        
        return response.data[0]
    
    def get_books(self):
        response = self.supabase.table('books').select('*').execute()
        
        return response.data
    
    def create_book(self, title, author):
        response = self.supabase.table('books').insert({
            'title': title,
            'author': author
        }).execute()
        
        return response.data[0]
    
    def update_book(self, book_id, **fields):
        response = self.supabase.table('books').update(fields).eq('id', book_id).execute()
        
        if len(response.data) == 0:
            return None
        
        return response.data[0]
    
    def delete_book(self, book_id):
        response = self.supabase.table('books').delete().eq('id', book_id).execute()
        
        if len(response.data) == 0:
            return None
        
        return response.data[0]