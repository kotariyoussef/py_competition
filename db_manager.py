import sqlite3
from datetime import datetime


class DBManager:
    """Database Manager for Flashcards App."""
    
    def __init__(self, db_name="flashcards.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_tables()

    def create_tables(self):
        """Create tables for the flashcards app."""
        cursor = self.conn.cursor()

        # Decks Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Decks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Flashcards Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deck_id INTEGER,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                hint TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deck_id) REFERENCES Decks (id)
            )
        """)

        # Progress Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER,
                correct_count INTEGER DEFAULT 0,
                incorrect_count INTEGER DEFAULT 0,
                last_reviewed TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (card_id) REFERENCES Flashcards (id)
            )
        """)

        self.conn.commit()

    def add_deck(self, name, description):
        """Add a new deck."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Decks (name, description, created_at, updated_at)
            VALUES (?, ?, ?, ?)
        """, (name, description, datetime.now(), datetime.now()))
        self.conn.commit()

    def add_flashcard(self, deck_id, question, answer, hint=None):
        """Add a new flashcard to a specific deck."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO Flashcards (deck_id, question, answer, hint, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (deck_id, question, answer, hint, datetime.now(), datetime.now()))
        self.conn.commit()

    def get_decks(self):
        """Retrieve all decks."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, description FROM Decks")
        return cursor.fetchall()

    def get_flashcards(self, deck_id):
        """Retrieve flashcards for a specific deck."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, question, answer, hint FROM Flashcards WHERE deck_id = ?
        """, (deck_id,))
        return cursor.fetchall()

    def add_progress(self, card_id, correct):
        """Update progress for a specific flashcard."""
        cursor = self.conn.cursor()

        # Check if progress exists
        cursor.execute("""
            SELECT id, correct_count, incorrect_count FROM Progress WHERE card_id = ?
        """, (card_id,))
        progress = cursor.fetchone()

        if progress:
            # Update existing progress
            progress_id, correct_count, incorrect_count = progress
            if correct:
                correct_count += 1
            else:
                incorrect_count += 1

            cursor.execute("""
                UPDATE Progress
                SET correct_count = ?, incorrect_count = ?, last_reviewed = ?
                WHERE id = ?
            """, (correct_count, incorrect_count, datetime.now(), progress_id))
        else:
            # Insert new progress record
            cursor.execute("""
                INSERT INTO Progress (card_id, correct_count, incorrect_count, last_reviewed)
                VALUES (?, ?, ?, ?)
            """, (card_id, 1 if correct else 0, 0 if correct else 1, datetime.now()))

        self.conn.commit()

    def get_progress(self, card_id):
        """Retrieve progress for a specific flashcard."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT correct_count, incorrect_count FROM Progress WHERE card_id = ?
        """, (card_id,))
        return cursor.fetchone()

    def close(self):
        """Close the database connection."""
        self.conn.close()


# Example Usage
if __name__ == "__main__":
    db = DBManager()

    # Create a new deck
    db.add_deck("Python Basics", "A deck for learning Python fundamentals")

    # Add flashcards to the deck
    db.add_flashcard(1, "What is Python?", "A programming language", "Think of a snake 🐍")
    db.add_flashcard(1, "What does 'len()' do?", "Returns the length of an object", "Used for strings, lists, etc.")

    # Display all decks
    print("Available Decks:")
    for deck in db.get_decks():
        print(f"{deck[0]}. {deck[1]} - {deck[2]}")

    # Display flashcards for the first deck
    print("\nFlashcards in 'Python Basics':")
    for card in db.get_flashcards(1):
        print(f"Q: {card[1]} | A: {card[2]} | Hint: {card[3]}")

    # Update progress for a flashcard
    db.add_progress(card_id=1, correct=True)
    db.add_progress(card_id=1, correct=False)

    # Display progress for a flashcard
    progress = db.get_progress(1)
    print("\nProgress for Flashcard 1:")
    print(f"Correct: {progress[0]}, Incorrect: {progress[1]}")

    db.close()
