from openai import OpenAI
import os

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generate_book_summary(self, title, author):
        prompt = f"Generate a brief 2-3 sentence summary for the book with the given title: {title} and author: {author}."
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content

    def suggrest_similar_books(self, title, author):
        pass