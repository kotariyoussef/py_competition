import sys
import os
from urllib.parse import parse_qs
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib
from urllib.parse import parse_qs

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_manager import DBManager

class FlashcardsWeb:
    """Web-based Flashcards Application using built-in Python libraries."""

    def __init__(self):
        self.db = DBManager()
        self.template_dir = "templates"

    def render_html(self, template_name, context=None):
        """Render HTML content by replacing placeholders with values."""
        with open(f"templates/{template_name}", "r") as file:
            content = file.read()

        if context:
            # Debugging: Log the context
            print(f"Rendering template {template_name} with context: {context}")

            # Convert each value in context to string before replacing in content
            for key, value in context.items():
                try:
                    content = content.replace(f"{{{{ {key} }}}}", str(value))  # Convert value to string
                except Exception as e:
                    print(f"Error replacing key: {key} with value: {value}. Exception: {e}")
                    continue

        return content

    def display_decks(self):
        """Display all decks on the webpage."""
        decks = self.db.get_decks()
        if decks:
            decks_list = "\n".join(
                [f'<li><a href="/deck/{deck[0]}">{deck[1]}</a>: {deck[2]}</li>' for deck in decks]
            )
            context = {"decks_list": decks_list}
        else:
            context = {"message": "No decks available. Please add some decks."}
        return self.render_html("deck_list.html", context)

    def display_flashcards(self, deck_id):
        """Display all flashcards for a specific deck."""
        flashcards = self.db.get_flashcards(deck_id)
        if flashcards:
            flashcards_list = "\n".join(
                [f'<li>Q: {card[1]}<br> A: {card[2]} <br> Hint: {card[3]}</li>' for card in flashcards]
            )
            context = {"flashcards_list": flashcards_list,"deck_id": deck_id}
        else:
            context = {"flashcards_list":"No Flashcards of this deck.","deck_id": deck_id}
        return self.render_html("flashcard_list.html", context)

    def add_deck_form(self):
        """Display a form to add a new deck."""
        return self.render_html("add_deck.html", {})

    def add_flashcard_form(self, deck_id):
        """Display a form to add a new flashcard to a deck."""
        return self.render_html("add_flashcard.html", {"deck_id": deck_id})

    def add_deck(self, form_data):
        """Add a new deck to the database."""
        name = form_data.getvalue("name")
        description = form_data.getvalue("description")
        self.db.add_deck(name, description)
        return self.render_html("success.html", {"message": "Deck added successfully!"})

    def add_flashcard(self, deck_id, form_data):
        """Add a flashcard to a specific deck."""
        question = form_data.getvalue("question")
        answer = form_data.getvalue("answer")
        hint = form_data.getvalue("hint")
        self.db.add_flashcard(deck_id, question, answer, hint)
        return self.render_html("success.html", {"message": "Flashcard added successfully!"})

    def handle_request(self, path, form_data=None):
        """Handle incoming requests based on the URL path."""
        if path == "/":
            return self.display_decks()
        elif path.startswith("/deck/"):
            deck_id = int(path.split("/deck/")[1])  # Extract deck_id for viewing flashcards
            return self.display_flashcards(deck_id)
        elif path == "/add_deck":
            if form_data:
                return self.add_deck(form_data)
            return self.add_deck_form()
        elif path.startswith("/add_flashcard/"):
            # Fix: Correctly extract the deck_id from the path
            print(path)
            try:
                deck_id = int(path.split("/add_flashcard/")[1])  # Extract deck_id from URL
                if form_data:
                    return self.add_flashcard(deck_id, form_data)
                return self.add_flashcard_form(deck_id)
            except ValueError:
                return self.render_html("error.html", {"message": "Invalid deck ID."})
        else:
            return self.render_html("error.html", {"message": "Page not found."})


def run(port = 7080):
    """Run the HTTP server."""
    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            path = urllib.parse.unquote(self.path)
            content = flashcards_web.handle_request(path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())

        def do_POST(self):
            path = urllib.parse.unquote(self.path)
            
            # Manually parse the form data from the body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse the POST data as form data (like cgi.FieldStorage would do)
            form_data = parse_qs(post_data)
            
            # Convert the parsed data to a format similar to cgi.FieldStorage
            class FakeFieldStorage:
                def __init__(self, form_data):
                    self.form_data = form_data
                def getvalue(self, key):
                    return self.form_data.get(key, [None])[0]
            
            form_storage = FakeFieldStorage(form_data)
            
            content = flashcards_web.handle_request(path, form_storage)
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode())

    flashcards_web = FlashcardsWeb()
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"Starting server on http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
