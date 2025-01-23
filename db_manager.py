import sqlite3


class DBManager:
    def __init__(self, db_name="flashcards.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                hint TEXT,
                image_url TEXT,
                video_url TEXT,
                audio_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            );
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS card_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                card_id INTEGER NOT NULL,
                tag_id INTEGER NOT NULL,
                FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags (id) ON DELETE CASCADE
            );
        """)
        self.conn.commit()

    def add_card(self, question, answer, hint=None, image_url=None, audio_url=None, video_url=None):
        self.cursor.execute("""
        INSERT INTO flashcards (question, answer, hint, image_url, audio_url, video_url)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (question, answer, hint, image_url, audio_url, video_url))
        self.conn.commit()

    def get_cards(self):
        self.cursor.execute("SELECT * FROM flashcards;")
        return self.cursor.fetchall()

    def delete_card(self, card_id):
        self.cursor.execute("DELETE FROM flashcards WHERE id = ?", (card_id,))
        self.conn.commit()

    def add_tag(self, name):
        try:
            self.cursor.execute("INSERT INTO tags (name) VALUES (?)", (name,))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print(f"Tag {name} already exists.")

    def get_tags(self):
        self.cursor.execute("SELECT * FROM tags;")
        return self.cursor.fetchall()

    def delete_tag(self, tag_id):
        self.cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
        self.conn.commit()

    def assign_tag_to_card(self, tag_id, card_id):
        self.cursor.execute("""
        INSERT INTO card_tags (tag_id, card_id) VALUES (?, ?);
        """, (tag_id, card_id))
        self.conn.commit()

    def get_tags_for_card(self, card_id):
        self.cursor.execute("""
            SELECT t.id, t.name FROM tags t
            JOIN card_tags ct ON t.id = ct.tag_id
            WHERE ct.card_id = ?;
        """, (card_id,))
        return self.cursor.fetchall()

    def get_cards_for_tag(self, tag_id):
        self.cursor.execute("""
            SELECT c.id, c.question, c.answer, c.hint, c.image_url, c.audio_url, c.video_url FROM flashcards c
            JOIN card_tags ct ON c.id = ct.tag_id
            WHERE ct.tag_id = ?;
        """, (tag_id,))
        return self.cursor.fetchall()

    def unassign_tag_from_card(self, tag_id, card_id):
        self.cursor.execute("""
        DELETE FROM card_tags WHERE card_id = ? AND tag_id = ?;
        """, (card_id, tag_id))

    def close(self):
        self.conn.close()


# Example Usage
if __name__ == "__main__":
    db_manager = DBManager()

    # Add cards
    db_manager.add_card(
        question="What is the capital of France?",
        answer="Paris",
        hint="City of Light"
    )
    db_manager.add_card(
        question="What is 2 + 2?",
        answer="4",
        hint="Basic math"
    )

    # Add tags
    db_manager.add_tag("Geography")
    db_manager.add_tag("Math")

    # Assign tags to cards
    db_manager.assign_tag_to_card(card_id=1, tag_id=1)  # Assign "Geography" to card 1
    db_manager.assign_tag_to_card(card_id=2, tag_id=2)  # Assign "Math" to card 2

    # Get all cards
    print("All Cards:", db_manager.get_cards())

    # Get all tags
    print("All Tags:", db_manager.get_tags())

    # Get tags for a specific card
    print("Tags for Card 1:", db_manager.get_tags_for_card(card_id=1))

    # Get cards for a specific tag
    print("Cards with 'Math' Tag:", db_manager.get_cards_for_tag(tag_id=2))

    # Unassign a tag from a card
    db_manager.unassign_tag_from_card(card_id=1, tag_id=1)

    # Delete a card
    db_manager.delete_card(card_id=2)

    # Clean up
    db_manager.close()
