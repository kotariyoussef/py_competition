import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db_manager import DBManager

class FlashcardsApp:
    """Console-based Flashcards Application."""
    
    def __init__(self):
        self.db = DBManager()
    
    def display_decks(self):
        """Display all decks."""
        decks = self.db.get_decks()
        if decks:
            print("Available Decks:")
            for deck in decks:
                print(f"{deck[0]}. {deck[1]} - {deck[2]}")
        else:
            print("No decks available. Please add some decks.")

    def display_flashcards(self, deck_id):
        """Display all flashcards for a specific deck."""
        flashcards = self.db.get_flashcards(deck_id)
        if flashcards:
            print("\nFlashcards:")
            for card in flashcards:
                print(f"Q: {card[1]} | A: {card[2]} | Hint: {card[3]}")
        else:
            print("No flashcards available in this deck.")

    def quiz(self, deck_id):
        """Start a quiz for a specific deck."""
        flashcards = self.db.get_flashcards(deck_id)
        if flashcards:
            for card in flashcards:
                print(f"\nQ: {card[1]}")
                answer = input("Your answer: ")
                correct = answer.lower() == card[2].lower()  # Simple comparison for now
                self.db.add_progress(card[0], correct)
                print(f"Correct answer: {card[2]}")
                print(f"Your answer was {'correct' if correct else 'incorrect'}!\n")
        else:
            print("No flashcards available in this deck to quiz on.")

    def main_menu(self):
        """Display the main menu for the app."""
        while True:
            print("\n--- Flashcards App ---")
            print("1. Add a new deck")
            print("2. Add flashcards to a deck")
            print("3. View all decks")
            print("4. Quiz on a deck")
            print("5. Exit")
            
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_deck()
            elif choice == "2":
                self.add_flashcards()
            elif choice == "3":
                self.display_decks()
            elif choice == "4":
                self.start_quiz()
            elif choice == "5":
                self.db.close()
                print("Goodbye!")
                break
            else:
                print("Invalid choice! Please try again.")

    def add_deck(self):
        """Add a new deck."""
        name = input("Enter deck name: ")
        description = input("Enter deck description: ")
        self.db.add_deck(name, description)
        print(f"Deck '{name}' added successfully!")

    def add_flashcards(self):
        """Add flashcards to an existing deck."""
        self.display_decks()
        deck_id = int(input("\nEnter deck ID to add flashcards: "))
        question = input("Enter question: ")
        answer = input("Enter answer: ")
        hint = input("Enter hint (optional): ")
        self.db.add_flashcard(deck_id, question, answer, hint)
        print("Flashcard added successfully!")

    def start_quiz(self):
        """Start a quiz on a specific deck."""
        self.display_decks()
        deck_id = int(input("\nEnter deck ID to quiz on: "))
        self.quiz(deck_id)


def main():
    app = FlashcardsApp()
    app.main_menu()

# Run the application
if __name__ == "__main__":
    main()
