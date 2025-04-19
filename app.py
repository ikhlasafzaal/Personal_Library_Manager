import json
import streamlit as st

class PersonalLibraryManager:
    def __init__(self):
        self.library = []

    def add_book(self, title, author, year, genre, read_status):
        book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        }
        self.library.append(book)
        st.success("📚 Book added successfully!")

    def remove_book(self, title):
        book_to_remove = None
        for book in self.library:
            if book["title"].lower() == title.lower():
                book_to_remove = book
                break

        if book_to_remove:
            self.library.remove(book_to_remove)
            st.success("❌ Book removed successfully!")
        else:
            st.warning("🚫 Book not found.")

    def search_books(self, search_type, search_value):
        if search_type == "title":
            matches = [book for book in self.library if search_value.lower() in book["title"].lower()]
        elif search_type == "author":
            matches = [book for book in self.library if search_value.lower() in book["author"].lower()]
        elif search_type == "genre":
            matches = [book for book in self.library if search_value.lower() in book["genre"].lower()]
        elif search_type == "year":
            try:
                year = int(search_value)
                matches = [book for book in self.library if book["year"] == year]
            except ValueError:
                matches = []
                st.warning("⚠️ Invalid year format.")
        else:
            matches = []

        return matches

    def display_books(self):
        if self.library:
            st.subheader("📖 Your Library:")
            for i, book in enumerate(self.library, 1):
                read_status = "✅ Read" if book["read_status"] else "❌ Unread"
                st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
        else:
            st.warning("🛑 Your library is empty.")

    def display_statistics(self):
        total_books = len(self.library)
        if total_books == 0:
            st.warning("❗ No books in the library.")
            return
        read_books = sum(1 for book in self.library if book["read_status"])
        read_percentage = (read_books / total_books) * 100
        st.write(f"📊 Total books: {total_books}")
        st.write(f"📚 Percentage read: {read_percentage:.1f}%")

    def save_to_file(self, filename="library.json"):
        with open(filename, "w") as file:
            json.dump(self.library, file)
        st.success("💾 Library saved to file.")

    def load_from_file(self, filename="library.json"):
        try:
            with open(filename, "r") as file:
                self.library = json.load(file)
            st.success("📥 Library loaded from file.")
        except FileNotFoundError:
            st.warning("📂 No saved library found, starting fresh.")
        except json.JSONDecodeError:
            st.warning("⚠️ Error loading the library from file. The file may be corrupted.")

# Streamlit UI for managing the library

def show_menu():
    st.title("📚 Personal Library Manager")
    st.sidebar.header("📋 Menu")
    menu_options = ["Add a book", "Remove a book", "Search for a book", "Display all books", "Display statistics", "Save Library", "Exit"]
    choice = st.sidebar.radio("Choose an option:", menu_options)

    return choice

def main():
    manager = PersonalLibraryManager()
    manager.load_from_file()

    # Show menu and handle different actions
    choice = show_menu()

    if choice == "Add a book":
        with st.form("add_book_form"):
            st.subheader("➕ Add a new book")
            title = st.text_input("Enter the book title:")
            author = st.text_input("Enter the author:")
            year = st.number_input("Enter the publication year:", min_value=1000, max_value=2025, step=1)
            genre = st.text_input("Enter the genre:")
            read_status = st.radio("📖 Have you read this book?", ("Yes", "No")) == "Yes"
            submit_button = st.form_submit_button("Add Book")

            if submit_button:
                if title and author and genre:
                    manager.add_book(title, author, year, genre, read_status)
                else:
                    st.warning("⚠️ Please fill in all fields.")

    elif choice == "Remove a book":
        title_to_remove = st.text_input("Enter the title of the book to remove:")
        if st.button("❌ Remove Book"):
            if title_to_remove:
                manager.remove_book(title_to_remove)
            else:
                st.warning("⚠️ Please enter a title.")

    elif choice == "Search for a book":
        st.subheader("🔍 Search for a book")
        search_type = st.selectbox("Search by:", ["title", "author", "genre", "year"])
        search_value = st.text_input(f"Enter the {search_type}:")
        if st.button("Search"):
            if search_value:
                matches = manager.search_books(search_type, search_value)
                if matches:
                    for i, book in enumerate(matches, 1):
                        read_status = "✅ Read" if book["read_status"] else "❌ Unread"
                        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
                else:
                    st.warning("❌ No matching books found.")
            else:
                st.warning("⚠️ Please enter a search value.")

    elif choice == "Display all books":
        manager.display_books()

    elif choice == "Display statistics":
        manager.display_statistics()

    elif choice == "Save Library":
        manager.save_to_file()

    elif choice == "Exit":
        st.success("👋 Goodbye!")
        return

if __name__ == "__main__":
    main()
