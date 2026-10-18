from storage import Storage
from book import Book
from member import Member, StudentMember, FacultyMember
from loan import Loan


class Library:
    def __init__(self):
        self.storage = Storage
        self.books = {}
        self.members = {}
        self.loans = {}

    def load_data(self):
        books_data = self.storage.load_data("data/books.json")
        members_data = self.storage.load_data("data/members.json")
        loans_data = self.storage.load_data("data/loans.json")

        if books_data is None or members_data is None or loans_data is None:
            return False

        try:
            loaded_books = {}
            loaded_members = {}
            loaded_loans = {}

            for data in books_data:
                book = Book.from_dict(data)
                if book.book_id in loaded_books:
                    return False
                loaded_books[book.book_id] = book

            for data in members_data:
                member = Member.from_dict(data)
                if member.member_id in loaded_members:
                    return False
                loaded_members[member.member_id] = member

            for data in loans_data:
                loan = Loan.from_dict(data)
                if loan.loan_id in loaded_loans:
                    return False
                loaded_loans[loan.loan_id] = loan

        except (ValueError, TypeError, KeyError):
            return False

        self.books = loaded_books
        self.members = loaded_members
        self.loans = loaded_loans
        return True

    def save_data(self):
        books_data = [book.to_dict() for book in self.books.values()]
        members_data = [member.to_dict() for member in self.members.values()]
        loans_data = [loan.to_dict() for loan in self.loans.values()]

        books_saved = self.storage.save_data("data/books.json", books_data)
        members_saved = self.storage.save_data("data/members.json", members_data)
        loans_saved = self.storage.save_data("data/loans.json", loans_data)
        return books_saved and members_saved and loans_saved

    def _save_books(self):
        return self.storage.save_data(
            "data/books.json", [book.to_dict() for book in self.books.values()]
        )

    def _save_members(self):
        return self.storage.save_data(
            "data/members.json", [member.to_dict() for member in self.members.values()]
        )

    def _save_loan_transaction(self, previous_books, previous_loans):
        books_data = [book.to_dict() for book in self.books.values()]
        loans_data = [loan.to_dict() for loan in self.loans.values()]

        if not self.storage.save_data("data/books.json", books_data):
            return False

        if self.storage.save_data("data/loans.json", loans_data):
            return True

        if not self.storage.save_data("data/books.json", previous_books):
            raise RuntimeError(
                "Could not restore books.json after a failed loan save. "
                "Stop using the application and restore consistent data from backup."
            )
        return False

    def add_book(self, book):
        if not isinstance(book, Book) or book.book_id in self.books:
            return False
        self.books[book.book_id] = book
        if not self._save_books():
            del self.books[book.book_id]
            return False
        return True

    def get_book(self, book_id):
        return self.books.get(book_id)

    def search_books(self, keyword):
        if not isinstance(keyword, str) or not keyword.strip():
            return []
        keyword = keyword.lower().strip()
        return [
            book for book in self.books.values()
            if keyword in book.title.lower()
            or keyword in book.author.lower()
            or keyword in book.category.lower()
        ]

    def update_book(self, book_id, **kwargs):
        book = self.get_book(book_id)
        if book is None:
            return False
        previous = book.to_dict()
        if not book.update_info(**kwargs):
            return False
        if not self._save_books():
            self.books[book_id] = Book.from_dict(previous)
            return False
        return True

    def add_book_copies(self, book_id, quantity):
        book = self.get_book(book_id)
        if book is None:
            return False
        previous = book.to_dict()
        if not book.add_copies(quantity):
            return False
        if not self._save_books():
            self.books[book_id] = Book.from_dict(previous)
            return False
        return True

    def remove_book_copies(self, book_id, quantity):
        book = self.get_book(book_id)
        if book is None:
            return False
        previous = book.to_dict()
        if not book.remove_copies(quantity):
            return False
        if not self._save_books():
            self.books[book_id] = Book.from_dict(previous)
            return False
        return True

    def remove_book(self, book_id):
        book = self.get_book(book_id)
        if book is None or book.total_copies != book.available_copies:
            return False
        if any(loan.book_id == book_id and loan.is_active() for loan in self.loans.values()):
            return False
        del self.books[book_id]
        if not self._save_books():
            self.books[book_id] = book
            return False
        return True

    def list_books(self):
        return list(self.books.values())

    def register_member(self, member):
        if not isinstance(member, (StudentMember, FacultyMember)):
            return False
        if member.member_id in self.members:
            return False
        self.members[member.member_id] = member
        if not self._save_members():
            del self.members[member.member_id]
            return False
        return True

    def get_member(self, member_id):
        return self.members.get(member_id)

    def update_member(self, member_id, **kwargs):
        member = self.get_member(member_id)
        if member is None:
            return False
        previous = member.to_dict()
        if not member.update_info(**kwargs):
            return False
        if not self._save_members():
            self.members[member_id] = Member.from_dict(previous)
            return False
        return True

    def suspend_member(self, member_id):
        member = self.get_member(member_id)
        if member is None or not member.is_active():
            return False
        member.suspend()
        if not self._save_members():
            member.activate()
            return False
        return True

    def activate_member(self, member_id):
        member = self.get_member(member_id)
        if member is None or member.is_active():
            return False
        member.activate()
        if not self._save_members():
            member.suspend()
            return False
        return True

    def list_members(self):
        return list(self.members.values())

    def get_loan(self, loan_id):
        return self.loans.get(loan_id)

    def borrow_book(self, member_id, book_id):
        member = self.get_member(member_id)
        book = self.get_book(book_id)
        if member is None or book is None:
            return False
        if not member.is_active() or not book.is_available():
            return False

        active_loans = 0
        for loan in self.loans.values():
            if loan.member_id == member_id and loan.is_active():
                active_loans += 1
                if loan.is_overdue() or loan.book_id == book_id:
                    return False
        if active_loans >= member.get_max_books():
            return False

        loan_number = 1
        while f"L{loan_number:03d}" in self.loans:
            loan_number += 1
        loan_id = f"L{loan_number:03d}"
        new_loan = Loan(
            loan_id, book_id, member_id,
            member.get_loan_duration(), member.get_fine_rate()
        )

        previous_books = [item.to_dict() for item in self.books.values()]
        previous_loans = [item.to_dict() for item in self.loans.values()]
        if not book.borrow_copy():
            return False
        self.loans[loan_id] = new_loan
        try:
            saved = self._save_loan_transaction(previous_books, previous_loans)
        except Exception:
            book.return_copy()
            del self.loans[loan_id]
            raise
        if not saved:
            book.return_copy()
            del self.loans[loan_id]
            return False
        return new_loan

    def return_book(self, loan_id):
        loan = self.get_loan(loan_id)
        if loan is None or not loan.is_active():
            return False
        book = self.get_book(loan.book_id)
        if book is None or book.available_copies >= book.total_copies:
            return False

        previous_books = [item.to_dict() for item in self.books.values()]
        previous_loans = [item.to_dict() for item in self.loans.values()]
        if not book.return_copy():
            return False
        fine = loan.return_book()
        if fine is False or fine is None:
            self.books[book.book_id] = Book.from_dict(
                next(item for item in previous_books if item["book_id"] == book.book_id)
            )
            return False
        try:
            saved = self._save_loan_transaction(previous_books, previous_loans)
        except Exception:
            self.books[book.book_id] = Book.from_dict(
                next(item for item in previous_books if item["book_id"] == book.book_id)
            )
            self.loans[loan_id] = Loan.from_dict(
                next(item for item in previous_loans if item["loan_id"] == loan_id)
            )
            raise
        if not saved:
            self.books[book.book_id] = Book.from_dict(
                next(item for item in previous_books if item["book_id"] == book.book_id)
            )
            self.loans[loan_id] = Loan.from_dict(
                next(item for item in previous_loans if item["loan_id"] == loan_id)
            )
            return False
        return fine

    def get_member_loans(self, member_id):
        if self.get_member(member_id) is None:
            return []
        return [loan for loan in self.loans.values() if loan.member_id == member_id]

    def list_active_loans(self):
        return [loan for loan in self.loans.values() if loan.is_active()]

    def list_overdue_loans(self):
        return [loan for loan in self.loans.values() if loan.is_overdue()]