from datetime import datetime, timedelta

class LibraryItem:
    def __init__(self, item_id, title, author, category):
        self.item_id = item_id
        self.title = title
        self.author = author
        self.category = category
        self.is_checked_out = False
        self.due_date = None
        self.borrower = None

    def check_out(self, borrower, days=14):
        if self.is_checked_out:
            return False
        self.is_checked_out = True
        self.borrower = borrower
        self.due_date = datetime.now() + timedelta(days=days)
        borrower.borrow_item(self)
        return True

    def return_item(self):
        if not self.is_checked_out:
            return False
        self.is_checked_out = False
        self.borrower.return_item(self)
        self.borrower = None
        self.due_date = None
        return True

    def calculate_fine(self, fine_per_day=1):
        if self.is_checked_out and datetime.now() > self.due_date:
            overdue_days = (datetime.now() - self.due_date).days
            return overdue_days * fine_per_day
        return 0

    def __str__(self):
        status = "Checked out" if self.is_checked_out else "Available"
        return f"{self.item_id}: {self.title} by {self.author} ({self.category}) - {status}"

class Book(LibraryItem):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title, author, "Book")

class Magazine(LibraryItem):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title, author, "Magazine")

class DVD(LibraryItem):
    def __init__(self, item_id, title, author):
        super().__init__(item_id, title, author, "DVD")

class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
        self.borrowed_items = []

    def borrow_item(self, item):
        self.borrowed_items.append(item)

    def return_item(self, item):
        self.borrowed_items.remove(item)

    def __str__(self):
        return f"{self.user_id}: {self.name} - {len(self.borrowed_items)} items borrowed"

class Library:
    def __init__(self):
        self.items = []
        self.users = []
        self.item_id_counter = 1
        self.user_id_counter = 1

    def add_item(self, item_type, title, author):
        item = None
        if item_type == "Book":
            item = Book(self.item_id_counter, title, author)
        elif item_type == "Magazine":
            item = Magazine(self.item_id_counter, title, author)
        elif item_type == "DVD":
            item = DVD(self.item_id_counter, title, author)

        if item:
            self.items.append(item)
            self.item_id_counter += 1
            return item
        return None

    def add_user(self, name):
        user = User(self.user_id_counter, name)
        self.users.append(user)
        self.user_id_counter += 1
        return user

    def search_item(self, title=None, author=None, category=None):
        results = []
        for item in self.items:
            if title and title.lower() in item.title.lower():
                results.append(item)
            elif author and author.lower() in item.author.lower():
                results.append(item)
            elif category and category.lower() in item.category.lower():
                results.append(item)
        return results

    def check_out_item(self, item_id, user_id):
        item = next((item for item in self.items if item.item_id == item_id), None)
        user = next((user for user in self.users if user.user_id == user_id), None)
        if item and user and not item.is_checked_out:
            return item.check_out(user)
        return False

    def return_item(self, item_id):
        item = next((item for item in self.items if item.item_id == item_id), None)
        if item and item.is_checked_out:
            return item.return_item()
        return False

    def calculate_fine(self, item_id, fine_per_day=1):
        item = next((item for item in self.items if item.item_id == item_id), None)
        if item and item.is_checked_out:
            return item.calculate_fine(fine_per_day)
        return 0

    def get_user_borrowing_history(self, user_id):
        user = next((user for user in self.users if user.user_id == user_id), None)
        if user:
            return user.borrowed_items
        return []

# Command-Line Interface

def main():
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add Item")
        print("2. Add User")
        print("3. Search Items")
        print("4. Check Out Item")
        print("5. Return Item")
        print("6. Calculate Fine")
        print("7. View User Borrowing History")
        print("8. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            item_type = input("Enter item type (Book/Magazine/DVD): ")
            title = input("Enter title: ")
            author = input("Enter author: ")
            item = library.add_item(item_type, title, author)
            if item:
                print(f"Added {item}")
            else:
                print("Invalid item type.")

        elif choice == "2":
            name = input("Enter user name: ")
            user = library.add_user(name)
            print(f"Added user: {user}")

        elif choice == "3":
            search_type = input("Search by title, author, or category? ").lower()
            search_term = input("Enter search term: ")
            results = []
            if search_type == "title":
                results = library.search_item(title=search_term)
            elif search_type == "author":
                results = library.search_item(author=search_term)
            elif search_type == "category":
                results = library.search_item(category=search_term)

            if results:
                print("Search results:")
                for item in results:
                    print(item)
            else:
                print("No items found.")

        elif choice == "4":
            try:
                item_id = int(input("Enter item ID to check out: "))
                user_id = int(input("Enter user ID: "))
                if library.check_out_item(item_id, user_id):
                    print("Item checked out successfully.")
                else:
                    print("Failed to check out item.")
            except ValueError:
                print("Invalid ID. Please enter a numeric ID.")

        elif choice == "5":
            try:
                item_id = int(input("Enter item ID to return: "))
                if library.return_item(item_id):
                    print("Item returned successfully.")
                else:
                    print("Failed to return item.")
            except ValueError:
                print("Invalid ID. Please enter a numeric ID.")

        elif choice == "6":
            try:
                item_id = int(input("Enter item ID to calculate fine: "))
                fine = library.calculate_fine(item_id)
                print(f"Fine: ${fine}")
            except ValueError:
                print("Invalid ID. Please enter a numeric ID.")

        elif choice == "7":
            try:
                user_id = int(input("Enter user ID to view borrowing history: "))
                history = library.get_user_borrowing_history(user_id)
                if history:
                    print("Borrowing history:")
                    for item in history:
                        print(item)
                else:
                    print("No borrowing history found.")
            except ValueError:
                print("Invalid ID. Please enter a numeric ID.")

        elif choice == "8":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
1