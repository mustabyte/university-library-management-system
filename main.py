
from library import Library
from book import Book
from member import StudentMember, FacultyMember

def display_main_menu():
    print("\n==========================================")
    print("    UNIVERSITY LIBRARY MANAGEMENT SYSTEM")
    print("==========================================")
    print("1. Book Management")
    print("2. Member Management")
    print("3. Loan Management")
    print("4. Reports & Statistics")
    print("0. Exit")



def display_book_menu():
    print("\n========== BOOK MANAGEMENT ==========")
    print("1. Add New Book")
    print("2. Search Books")
    print("3. View All Books")
    print("4. View Book Details")
    print("5. Update Book Information")
    print("6. Add Book Copies")
    print("7. Remove Book Copies")
    print("8. Remove Book")
    print("0. Back to Main Menu")

def add_new_book(library):
    print("\n========== ADD NEW BOOK ==========")

    existing_ids = [
        int(book.book_id[1:])
        for book in library.list_books()
        if book.book_id.startswith("B") and book.book_id[1:].isdigit()
    ]

    next_id = max(existing_ids, default=0) + 1
    book_id = f"B{next_id:03d}"

    print(f"\nBook ID: {book_id} (Auto-generated)\n")

    title = input("Enter Title: ").strip()
    author = input("Enter Author: ").strip()
    category = input("Enter Category: ").strip()

    try:
        total_copies = int(input("Enter Total Copies: ").strip())

        if not title or not author or not category:
            print("Error: All fields are required.")
            return

        if total_copies <= 0:
            print("Error: Total copies must be greater than zero.")
            return

        book = Book(book_id, title, author, category, total_copies)

        if library.add_book(book):
            print(f"\nBook {book_id} added successfully!")
        else:
            print("Error: Failed to add book.")

    except ValueError:
        print("Error: Please enter a valid number for total copies.")

def search_books(library):
    print("\n========== SEARCH BOOKS ==========")

    keyword = input("Enter search keyword: ").strip()

    if not keyword:
        print("Error: Search keyword cannot be empty.")
        return

    results = library.search_books(keyword)

    if not results:
        print("No matching books found.")
        return

    print(f"\nFound {len(results)} matching book(s):")

    for book in results:
        print("\n----------------------------------")
        print(f"Book ID: {book.book_id}")
        print(f"Title: {book.title}")
        print(f"Author: {book.author}")
        print(f"Category: {book.category}")
        print(f"Total Copies: {book.total_copies}")
        print(f"Available Copies: {book.available_copies}")

    print("----------------------------------")

def view_all_books(library):
    print("\n================ ALL BOOKS ================")

    books = library.list_books()

    if not books:
        print("No books found in the library.")
        return

    print(f"\n{'ID':<8} {'Title':<35} {'Author':<25} {'Available':<12}")
    print("-" * 85)

    for book in books:
        title = book.title[:32] + "..." if len(book.title) > 35 else book.title
        author = book.author[:22] + "..." if len(book.author) > 25 else book.author
        availability = f"{book.available_copies}/{book.total_copies}"

        print(f"{book.book_id:<8} {title:<35} {author:<25} {availability:<12}")

    print("-" * 85)
    print(f"Total Book Titles: {len(books)}")

def view_book_details(library):
    print("\n========== BOOK DETAILS ==========")

    book_id = input("Enter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    print("\n----------------------------------")
    print(f"Book ID: {book.book_id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Category: {book.category}")
    print(f"Total Copies: {book.total_copies}")
    print(f"Available Copies: {book.available_copies}")
    print(f"Borrowed Copies: {book.total_copies - book.available_copies}")
    print("----------------------------------")

def update_book_information(library):
    print("\n========== UPDATE BOOK INFORMATION ==========")

    book_id = input("Enter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    print("\nCurrent Book Information:")
    print(f"Book ID: {book.book_id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Category: {book.category}")

    print("\nEnter new information (press Enter to keep current value):")

    title = input(f"Title [{book.title}]: ").strip()
    author = input(f"Author [{book.author}]: ").strip()
    category = input(f"Category [{book.category}]: ").strip()

    updates = {}

    if title and title != book.title:
        updates["title"] = title

    if author and author != book.author:
        updates["author"] = author

    if category and category != book.category:
        updates["category"] = category

    if not updates:
        print("No changes made.")
        return

    if library.update_book(book_id, **updates):
        print("Book information updated successfully!")
    else:
        print("Error: Failed to update book information.")

def add_book_copies(library):
    print("\n========== ADD BOOK COPIES ==========")

    book_id = input("Enter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    print(f"\nTitle: {book.title}")
    print(f"Current Total Copies: {book.total_copies}")
    print(f"Current Available Copies: {book.available_copies}")

    try:
        quantity = int(input("\nEnter Number of Copies to Add: ").strip())

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return

        if library.add_book_copies(book_id, quantity):
            print(f"\n{quantity} copies added successfully!")
            print(f"Updated Total Copies: {book.total_copies}")
            print(f"Updated Available Copies: {book.available_copies}")
        else:
            print("Error: Failed to add book copies.")

    except ValueError:
        print("Error: Please enter a valid number.")

def remove_book_copies(library):
    print("\n========== REMOVE BOOK COPIES ==========")

    book_id = input("Enter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    borrowed_copies = book.total_copies - book.available_copies

    print(f"\nTitle: {book.title}")
    print(f"Current Total Copies: {book.total_copies}")
    print(f"Current Available Copies: {book.available_copies}")
    print(f"Currently Borrowed Copies: {borrowed_copies}")

    try:
        quantity = int(input("\nEnter Number of Copies to Remove: ").strip())

        if quantity <= 0:
            print("Error: Quantity must be greater than zero.")
            return

        if quantity > book.available_copies:
            print("Error: Cannot remove more copies than currently available.")
            return

        if library.remove_book_copies(book_id, quantity):
            print(f"\n{quantity} copies removed successfully!")
            print(f"Updated Total Copies: {book.total_copies}")
            print(f"Updated Available Copies: {book.available_copies}")
        else:
            print("Error: Failed to remove book copies.")

    except ValueError:
        print("Error: Please enter a valid number.")

def remove_book(library):
    print("\n========== REMOVE BOOK ==========")

    book_id = input("Enter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    print("\nBook Information:")
    print(f"Book ID: {book.book_id}")
    print(f"Title: {book.title}")
    print(f"Author: {book.author}")
    print(f"Category: {book.category}")
    print(f"Total Copies: {book.total_copies}")
    print(f"Available Copies: {book.available_copies}")

    if book.total_copies != book.available_copies:
        print("\nError: Cannot remove a book with borrowed copies.")
        return

    confirmation = input(
        "\nAre you sure you want to remove this book? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Book removal cancelled.")
        return

    if library.remove_book(book_id):
        print(f"\nBook {book_id} removed successfully!")
    else:
        print("Error: Failed to remove book.")

def book_management(library):
    while True:
        display_book_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_new_book(library)

        elif choice == "2":
            search_books(library)

        elif choice == "3":
            view_all_books(library)

        elif choice == "4":
            view_book_details(library)

        elif choice == "5":
            update_book_information(library)

        elif choice == "6":
            add_book_copies(library)

        elif choice == "7":
            remove_book_copies(library)

        elif choice == "8":
            remove_book(library)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")




def display_member_menu():
    print("\n========== MEMBER MANAGEMENT ==========")
    print("1. Register New Member")
    print("2. View All Members")
    print("3. View Member Details")
    print("4. Update Member Information")
    print("5. Suspend Member")
    print("6. Activate Member")
    print("7. View Member Borrowing History")
    print("0. Back to Main Menu")

def register_new_member(library):
    print("\n========== REGISTER NEW MEMBER ==========")

    print("1. Student")
    print("2. Faculty")

    member_type = input("\nSelect Member Type: ").strip()

    if member_type not in ("1", "2"):
        print("Error: Invalid member type.")
        return

    prefix = "S" if member_type == "1" else "F"

    existing_ids = [
        int(member.member_id[1:])
        for member in library.list_members()
        if member.member_id.startswith(prefix)
        and member.member_id[1:].isdigit()
    ]

    next_id = max(existing_ids, default=0) + 1
    member_id = f"{prefix}{next_id:03d}"

    print(f"\nMember ID: {member_id} (Auto-generated)\n")

    name = input("Enter Full Name: ").strip()
    email = input("Enter Email: ").strip()
    phone = input("Enter Phone Number: ").strip()

    if not name or not email or not phone:
        print("Error: All fields are required.")
        return

    if member_type == "1":
        member = StudentMember(member_id, name, email, phone)
    else:
        member = FacultyMember(member_id, name, email, phone)

    if library.register_member(member):
        print(f"\nMember {member_id} registered successfully!")
    else:
        print("Error: Failed to register member.")

def view_all_members(library):
    print("\n================ ALL MEMBERS ================")

    members = library.list_members()

    if not members:
        print("No members found in the library.")
        return

    print(f"\n{'ID':<8} {'Name':<28} {'Type':<10} {'Email':<35} {'Status':<12}")
    print("-" * 100)

    for member in members:
        name = member.name[:25] + "..." if len(member.name) > 28 else member.name
        email = member.email[:32] + "..." if len(member.email) > 35 else member.email

        print(
            f"{member.member_id:<8} "
            f"{name:<28} "
            f"{member.member_type:<10} "
            f"{email:<35} "
            f"{member.status:<12}"
        )

    print("-" * 100)
    print(f"Total Members: {len(members)}")

def view_member_details(library):
    print("\n========== MEMBER DETAILS ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    active_loans = [
        loan for loan in library.get_member_loans(member_id)
        if loan.is_active()
    ]

    print("\n----------------------------------")
    print(f"Member ID: {member.member_id}")
    print(f"Name: {member.name}")
    print(f"Member Type: {member.member_type}")
    print(f"Email: {member.email}")
    print(f"Phone: {member.phone}")
    print(f"Join Date: {member.join_date}")
    print(f"Status: {member.status}")

    print("\nBorrowing Information:")
    print(f"Maximum Books: {member.get_max_books()}")
    print(f"Loan Duration: {member.get_loan_duration()} days")
    print(f"Fine Rate: Tk {member.get_fine_rate()}/day")
    print(f"Currently Borrowed: {len(active_loans)}")
    print("----------------------------------")

def update_member_information(library):
    print("\n========== UPDATE MEMBER INFORMATION ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    print("\nCurrent Member Information:")
    print(f"Member ID: {member.member_id}")
    print(f"Name: {member.name}")
    print(f"Member Type: {member.member_type}")
    print(f"Email: {member.email}")
    print(f"Phone: {member.phone}")
    print(f"Status: {member.status}")

    print("\nEnter new information (press Enter to keep current value):")

    name = input(f"Name [{member.name}]: ").strip()
    email = input(f"Email [{member.email}]: ").strip()
    phone = input(f"Phone [{member.phone}]: ").strip()

    updates = {}

    if name and name != member.name:
        updates["name"] = name

    if email and email != member.email:
        updates["email"] = email

    if phone and phone != member.phone:
        updates["phone"] = phone

    if not updates:
        print("No changes made.")
        return

    if library.update_member(member_id, **updates):
        print("Member information updated successfully!")
    else:
        print("Error: Failed to update member information.")

def suspend_member(library):
    print("\n========== SUSPEND MEMBER ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    print("\nMember Information:")
    print(f"Member ID: {member.member_id}")
    print(f"Name: {member.name}")
    print(f"Member Type: {member.member_type}")
    print(f"Status: {member.status}")

    if not member.is_active():
        print("\nThis member is already suspended.")
        return

    confirmation = input(
        "\nAre you sure you want to suspend this member? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Suspension cancelled.")
        return

    if library.suspend_member(member_id):
        print(f"\nMember {member_id} suspended successfully!")
    else:
        print("Error: Failed to suspend member.")

def activate_member(library):
    print("\n========== ACTIVATE MEMBER ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    print("\nMember Information:")
    print(f"Member ID: {member.member_id}")
    print(f"Name: {member.name}")
    print(f"Member Type: {member.member_type}")
    print(f"Status: {member.status}")

    if member.is_active():
        print("\nThis member is already active.")
        return

    confirmation = input(
        "\nAre you sure you want to activate this member? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Activation cancelled.")
        return

    if library.activate_member(member_id):
        print(f"\nMember {member_id} activated successfully!")
    else:
        print("Error: Failed to activate member.")

def view_member_borrowing_history(library):
    print("\n========== MEMBER BORROWING HISTORY ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    print(f"\nMember ID: {member.member_id}")
    print(f"Name: {member.name}")
    print(f"Member Type: {member.member_type}")

    loans = library.get_member_loans(member_id)

    if not loans:
        print("\nNo borrowing history found for this member.")
        return

    print(
        f"\n{'Loan ID':<10} {'Book ID':<10} {'Book Title':<27} "
        f"{'Borrowed':<13} {'Due Date':<13} "
        f"{'Returned':<13} {'Status':<10}"
    )
    print("-" * 100)

    for loan in loans:
        book = library.get_book(loan.book_id)
        title = book.title if book else "Unknown Book"

        if len(title) > 27:
            title = title[:24] + "..."

        returned = loan.return_date if loan.return_date else "-"

        print(
            f"{loan.loan_id:<10} "
            f"{loan.book_id:<10} "
            f"{title:<27} "
            f"{loan.borrow_date:<13} "
            f"{loan.due_date:<13} "
            f"{returned:<13} "
            f"{loan.status:<10}"
        )

    print("-" * 100)

    active_count = sum(1 for loan in loans if loan.is_active())
    returned_count = len(loans) - active_count

    print(f"Total Loans: {len(loans)}")
    print(f"Active Loans: {active_count}")
    print(f"Returned Loans: {returned_count}")

def member_management(library):
    while True:
        display_member_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            register_new_member(library)

        elif choice == "2":
            view_all_members(library)

        elif choice == "3":
            view_member_details(library)

        elif choice == "4":
            update_member_information(library)

        elif choice == "5":
            suspend_member(library)

        elif choice == "6":
            activate_member(library)

        elif choice == "7":
            view_member_borrowing_history(library)

        elif choice == "0":
            break

        else:
            print("Invalid choice. Please try again.")





def display_loan_menu():
    print("\n========== LOAN MANAGEMENT ==========")
    print("1. Borrow Book")
    print("2. Return Book")
    print("3. View Loan Details")
    print("4. View All Active Loans")
    print("5. View All Overdue Loans")
    print("0. Back to Main Menu")

def borrow_book(library):
    print("\n========== BORROW BOOK ==========")

    member_id = input("Enter Member ID: ").strip().upper()

    if not member_id:
        print("Error: Member ID cannot be empty.")
        return

    member = library.get_member(member_id)

    if member is None:
        print("Error: Member not found.")
        return

    print(f"\nMember: {member.name}")
    print(f"Type: {member.member_type}")
    print(f"Status: {member.status}")

    if not member.is_active():
        print("Error: Suspended members cannot borrow books.")
        return

    book_id = input("\nEnter Book ID: ").strip().upper()

    if not book_id:
        print("Error: Book ID cannot be empty.")
        return

    book = library.get_book(book_id)

    if book is None:
        print("Error: Book not found.")
        return

    print(f"\nBook: {book.title}")
    print(f"Author: {book.author}")
    print(f"Available Copies: {book.available_copies}")

    if not book.is_available():
        print("Error: No copies available.")
        return

    active_loans = [
        loan for loan in library.get_member_loans(member_id)
        if loan.is_active()
    ]

    print(f"\nCurrently Borrowed: {len(active_loans)}")
    print(f"Borrowing Limit: {member.get_max_books()}")
    print(f"Loan Duration: {member.get_loan_duration()} days")

    confirmation = input(
        "\nConfirm borrowing this book? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Borrowing cancelled.")
        return

    loan = library.borrow_book(member_id, book_id)

    if not loan:
        print(
            "Error: Borrowing failed. Check borrowing limits, "
            "existing loans, or overdue restrictions."
        )
        return

    print("\n========== BORROWING SUCCESSFUL ==========")
    print(f"Loan ID: {loan.loan_id}")
    print(f"Member ID: {loan.member_id}")
    print(f"Book ID: {loan.book_id}")
    print(f"Borrow Date: {loan.borrow_date}")
    print(f"Due Date: {loan.due_date}")
    print(f"Status: {loan.status}")
    print("==========================================")

def return_borrowed_book(library):
    print("\n========== RETURN BOOK ==========")

    loan_id = input("Enter Loan ID: ").strip().upper()

    if not loan_id:
        print("Error: Loan ID cannot be empty.")
        return

    loan = library.get_loan(loan_id)

    if loan is None:
        print("Error: Loan not found.")
        return

    if not loan.is_active():
        print("Error: This book has already been returned.")
        return

    book = library.get_book(loan.book_id)
    member = library.get_member(loan.member_id)

    print("\nLoan Information:")
    print(f"Loan ID: {loan.loan_id}")
    print(f"Book: {book.title if book else loan.book_id}")
    print(f"Member: {member.name if member else loan.member_id}")
    print(f"Borrow Date: {loan.borrow_date}")
    print(f"Due Date: {loan.due_date}")
    print(f"Overdue Days: {loan.get_overdue_days()}")
    print(f"Current Fine: Tk {loan.calculate_fine()}")

    confirmation = input(
        "\nConfirm book return? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Return cancelled.")
        return

    fine = library.return_book(loan_id)

    if fine is False:
        print("Error: Failed to return book.")
        return

    print("\n========== RETURN SUCCESSFUL ==========")
    print(f"Loan ID: {loan.loan_id}")
    print(f"Return Date: {loan.return_date}")
    print(f"Status: {loan.status}")
    print(f"Overdue Fine: Tk {fine}")
    print("=======================================")

def view_loan_details(library):
    print("\n========== LOAN DETAILS ==========")

    loan_id = input("Enter Loan ID: ").strip().upper()

    if not loan_id:
        print("Error: Loan ID cannot be empty.")
        return

    loan = library.get_loan(loan_id)

    if loan is None:
        print("Error: Loan not found.")
        return

    book = library.get_book(loan.book_id)
    member = library.get_member(loan.member_id)

    print("\n----------------------------------")
    print(f"Loan ID: {loan.loan_id}")
    print(f"Book ID: {loan.book_id}")
    print(f"Book Title: {book.title if book else 'Unknown Book'}")
    print(f"Member ID: {loan.member_id}")
    print(f"Member Name: {member.name if member else 'Unknown Member'}")
    print(f"Borrow Date: {loan.borrow_date}")
    print(f"Due Date: {loan.due_date}")
    print(f"Return Date: {loan.return_date or 'Not Returned'}")
    print(f"Status: {loan.status}")

    if loan.is_active():
        print(f"Overdue Days: {loan.get_overdue_days()}")
        print(f"Current Fine: Tk {loan.calculate_fine()}")
    else:
        print("Loan Closed: Yes")

    print("----------------------------------")

def view_all_active_loans(library):
    print("\n========== ALL ACTIVE LOANS ==========")

    loans = library.list_active_loans()

    if not loans:
        print("No active loans found.")
        return

    print(
        f"\n{'Loan ID':<10} "
        f"{'Book ID':<10} "
        f"{'Member ID':<12} "
        f"{'Borrow Date':<15} "
        f"{'Due Date':<15} "
        f"{'Status':<12}"
    )

    print("-" * 80)

    for loan in loans:
        status = "Overdue" if loan.is_overdue() else "Active"

        print(
            f"{loan.loan_id:<10} "
            f"{loan.book_id:<10} "
            f"{loan.member_id:<12} "
            f"{loan.borrow_date:<15} "
            f"{loan.due_date:<15} "
            f"{status:<12}"
        )

    print("-" * 80)
    print(f"Total Active Loans: {len(loans)}")

def view_all_overdue_loans(library):
    print("\n========== ALL OVERDUE LOANS ==========")

    loans = library.list_overdue_loans()

    if not loans:
        print("No overdue loans found.")
        return

    print(
        f"\n{'Loan ID':<9} "
        f"{'Book Title':<25} "
        f"{'Member':<22} "
        f"{'Due Date':<13} "
        f"{'Days':<7} "
        f"{'Fine (Tk)':<12}"
    )

    print("-" * 95)

    total_fines = 0

    for loan in loans:
        book = library.get_book(loan.book_id)
        member = library.get_member(loan.member_id)

        book_title = book.title if book else loan.book_id
        member_name = member.name if member else loan.member_id

        if len(book_title) > 25:
            book_title = book_title[:22] + "..."

        if len(member_name) > 22:
            member_name = member_name[:19] + "..."

        overdue_days = loan.get_overdue_days()
        fine = loan.calculate_fine()

        total_fines += fine

        print(
            f"{loan.loan_id:<9} "
            f"{book_title:<25} "
            f"{member_name:<22} "
            f"{loan.due_date:<13} "
            f"{overdue_days:<7} "
            f"{fine:<12}"
        )

    print("-" * 95)
    print(f"Total Overdue Loans: {len(loans)}")
    print(f"Total Outstanding Fines: Tk {total_fines}")

def loan_management(library):
    while True:
        display_loan_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            borrow_book(library)
        elif choice == "2":
            return_borrowed_book(library)

        elif choice == "3":
            view_loan_details(library)

        elif choice == "4":
            view_all_active_loans(library)

        elif choice == "5":
            view_all_overdue_loans(library)

        elif choice == "0":
            break

        else:
            print("Error: Invalid choice. Please try again.")




def display_reports_menu():
    print("\n========== REPORTS & STATISTICS ==========")
    print("1. Library Overview")
    print("2. Books by Category")
    print("3. Member Statistics")
    print("4. Loan Statistics")
    print("5. Most Borrowed Books")
    print("6. Overdue Loan Report")
    print("7. Inventory Report")
    print("0. Back to Main Menu")


def library_overview(library):
    print("\n========== LIBRARY OVERVIEW ==========")

    books = library.list_books()
    members = library.list_members()
    active_loans = library.list_active_loans()
    overdue_loans = library.list_overdue_loans()

    total_titles = len(books)
    total_copies = sum(book.total_copies for book in books)
    available_copies = sum(book.available_copies for book in books)
    borrowed_copies = total_copies - available_copies

    total_members = len(members)

    student_count = sum(
        1 for member in members
        if member.member_type == "Student"
    )

    faculty_count = sum(
        1 for member in members
        if member.member_type == "Faculty"
    )

    active_members = sum(
        1 for member in members
        if member.is_active()
    )

    suspended_members = total_members - active_members

    outstanding_fines = sum(
        loan.calculate_fine() for loan in overdue_loans
    )

    print("\nBOOK STATISTICS")
    print("-" * 40)
    print(f"Total Book Titles: {total_titles}")
    print(f"Total Book Copies: {total_copies}")
    print(f"Available Copies: {available_copies}")
    print(f"Borrowed Copies: {borrowed_copies}")

    print("\nMEMBER STATISTICS")
    print("-" * 40)
    print(f"Total Members: {total_members}")
    print(f"Students: {student_count}")
    print(f"Faculty: {faculty_count}")
    print(f"Active Members: {active_members}")
    print(f"Suspended Members: {suspended_members}")

    print("\nLOAN STATISTICS")
    print("-" * 40)
    print(f"Active Loans: {len(active_loans)}")
    print(f"Overdue Loans: {len(overdue_loans)}")
    print(f"Outstanding Overdue Fines: Tk {outstanding_fines}")

    print("\n======================================")


def books_by_category(library):
    print("\n========== BOOKS BY CATEGORY ==========")

    books = library.list_books()

    if not books:
        print("No books found in the library.")
        return

    categories = {}

    for book in books:
        category = book.category

        if category not in categories:
            categories[category] = {
                "titles": 0,
                "total": 0,
                "available": 0,
                "borrowed": 0
            }

        categories[category]["titles"] += 1
        categories[category]["total"] += book.total_copies
        categories[category]["available"] += book.available_copies
        categories[category]["borrowed"] += (
            book.total_copies - book.available_copies
        )

    print(
        f"\n{'Category':<25} "
        f"{'Titles':<10} "
        f"{'Copies':<10} "
        f"{'Available':<12} "
        f"{'Borrowed':<10}"
    )

    print("-" * 70)

    for category, stats in sorted(categories.items()):
        name = category[:22] + "..." if len(category) > 25 else category

        print(
            f"{name:<25} "
            f"{stats['titles']:<10} "
            f"{stats['total']:<10} "
            f"{stats['available']:<12} "
            f"{stats['borrowed']:<10}"
        )

    print("-" * 70)
    print(f"Total Categories: {len(categories)}")
    print(f"Total Book Titles: {len(books)}")


def member_statistics(library):
    print("\n========== MEMBER STATISTICS ==========")

    members = library.list_members()
    active_loans = library.list_active_loans()

    if not members:
        print("No members registered in the library.")
        return

    total_members = len(members)

    students = [
        member for member in members
        if member.member_type == "Student"
    ]

    faculty = [
        member for member in members
        if member.member_type == "Faculty"
    ]

    active_members = [
        member for member in members
        if member.is_active()
    ]

    suspended_members = [
        member for member in members
        if not member.is_active()
    ]

    borrowing_member_ids = {
        loan.member_id for loan in active_loans
    }

    currently_borrowing = sum(
        1 for member in members
        if member.member_id in borrowing_member_ids
    )

    student_borrowers = sum(
        1 for member in students
        if member.member_id in borrowing_member_ids
    )

    faculty_borrowers = sum(
        1 for member in faculty
        if member.member_id in borrowing_member_ids
    )

    borrowing_percentage = (
        currently_borrowing / total_members * 100
    )

    print("\nMEMBERSHIP OVERVIEW")
    print("-" * 45)
    print(f"Total Registered Members: {total_members}")
    print(f"Total Students: {len(students)}")
    print(f"Total Faculty: {len(faculty)}")

    print("\nMEMBERSHIP STATUS")
    print("-" * 45)
    print(f"Active Members: {len(active_members)}")
    print(f"Suspended Members: {len(suspended_members)}")

    print("\nBORROWING ACTIVITY")
    print("-" * 45)
    print(f"Members Currently Borrowing: {currently_borrowing}")
    print(f"Student Borrowers: {student_borrowers}")
    print(f"Faculty Borrowers: {faculty_borrowers}")
    print(f"Members Without Active Loans: {total_members - currently_borrowing}")
    print(f"Borrowing Participation: {borrowing_percentage:.2f}%")

    print("\n==============================================")



def loan_statistics(library):
    print("\n========== LOAN STATISTICS ==========")

    # Get all loan objects from the dictionary
    loans = list(library.loans.values())

    active_loans = library.list_active_loans()
    overdue_loans = library.list_overdue_loans()

    # Calculate loan counts
    total_loans = len(loans)
    total_active = len(active_loans)
    total_overdue = len(overdue_loans)

    total_returned = sum(
        1 for loan in loans
        if loan.status == "Returned"
    )

    on_time_active = total_active - total_overdue

    # Calculate outstanding fines
    total_fines = sum(
        loan.calculate_fine()
        for loan in overdue_loans
    )

    # Calculate return and overdue rates
    if total_loans > 0:
        return_rate = total_returned / total_loans * 100
        overdue_rate = total_overdue / total_loans * 100
    else:
        return_rate = 0
        overdue_rate = 0

    if total_active > 0:
        active_overdue_rate = total_overdue / total_active * 100
    else:
        active_overdue_rate = 0

    # Display loan overview
    print("\nLOAN OVERVIEW")
    print("-" * 45)
    print(f"Total Loans Issued: {total_loans}")
    print(f"Returned Loans: {total_returned}")
    print(f"Active Loans: {total_active}")
    print(f"Active Loans Not Overdue: {on_time_active}")
    print(f"Overdue Loans: {total_overdue}")

    # Display loan performance
    print("\nLOAN PERFORMANCE")
    print("-" * 45)
    print(f"Return Rate: {return_rate:.2f}%")
    print(f"Overdue Rate (All Loans): {overdue_rate:.2f}%")
    print(f"Overdue Rate (Active Loans): {active_overdue_rate:.2f}%")

    # Display financial overview
    print("\nFINANCIAL OVERVIEW")
    print("-" * 45)
    print(f"Current Outstanding Fines: Tk {total_fines}")

    print("\n=============================================")


def most_borrowed_books(library):
    print("\n========== MOST BORROWED BOOKS ==========")

    loans = list(library.loans.values())

    if not loans:
        print("No borrowing records found.")
        return

    borrow_counts = {}

    for loan in loans:
        book_id = loan.book_id

        borrow_counts[book_id] = (
            borrow_counts.get(book_id, 0) + 1
        )

    ranked_books = sorted(
        borrow_counts.items(),
        key=lambda item: (-item[1], item[0])
    )

    top_books = ranked_books[:10]

    print(
        f"\n{'Rank':<7} "
        f"{'Book ID':<10} "
        f"{'Book Title':<35} "
        f"{'Times Borrowed':<15}"
    )

    print("-" * 75)

    for rank, (book_id, count) in enumerate(top_books, start=1):
        book = library.get_book(book_id)

        title = book.title if book else "Unknown Book"

        if len(title) > 35:
            title = title[:32] + "..."

        print(
            f"{rank:<7} "
            f"{book_id:<10} "
            f"{title:<35} "
            f"{count:<15}"
        )

    print("-" * 75)
    print(f"Total Unique Books Borrowed: {len(borrow_counts)}")
    print(f"Total Borrowing Transactions: {len(loans)}")

def overdue_loan_report(library):
    print("\n========== OVERDUE LOAN REPORT ==========")

    overdue_loans = library.list_overdue_loans()

    if not overdue_loans:
        print("No overdue loans found.")
        return

    print(
        f"\n{'Loan ID':<9} "
        f"{'Book ID':<9} "
        f"{'Member ID':<11} "
        f"{'Type':<10} "
        f"{'Due Date':<13} "
        f"{'Days':<7} "
        f"{'Rate':<9} "
        f"{'Fine':<10}"
    )

    print("-" * 85)

    total_fines = 0
    total_overdue_days = 0

    for loan in overdue_loans:
        member = library.get_member(loan.member_id)

        member_type = member.member_type if member else "Unknown"
        overdue_days = loan.get_overdue_days()
        fine = loan.calculate_fine()

        total_overdue_days += overdue_days
        total_fines += fine

        print(
            f"{loan.loan_id:<9} "
            f"{loan.book_id:<9} "
            f"{loan.member_id:<11} "
            f"{member_type:<10} "
            f"{loan.due_date:<13} "
            f"{overdue_days:<7} "
            f"{loan.fine_rate:<9} "
            f"{fine:<10}"
        )

    average_overdue_days = (
        total_overdue_days / len(overdue_loans)
    )

    print("-" * 85)

    print(f"Total Overdue Loans: {len(overdue_loans)}")
    print(f"Average Overdue Days: {average_overdue_days:.2f}")
    print(f"Total Outstanding Fines: Tk {total_fines}")

    print("\n==========================================")


def inventory_report(library):
    print("\n========== INVENTORY REPORT ==========")

    books = library.list_books()

    if not books:
        print("No books found in the library.")
        return

    total_copies = 0
    available_copies = 0
    borrowed_copies = 0

    available_titles = 0
    low_stock_titles = 0
    out_of_stock_titles = 0

    print(
        f"\n{'Book ID':<10} "
        f"{'Book Title':<30} "
        f"{'Total':<8} "
        f"{'Available':<12} "
        f"{'Borrowed':<10} "
        f"{'Status':<15}"
    )

    print("-" * 90)

    for book in books:
        borrowed = book.total_copies - book.available_copies

        total_copies += book.total_copies
        available_copies += book.available_copies
        borrowed_copies += borrowed

        if book.available_copies == 0:
            status = "Out of Stock"
            out_of_stock_titles += 1

        elif book.available_copies == 1:
            status = "Low Stock"
            low_stock_titles += 1

        else:
            status = "Available"
            available_titles += 1

        title = book.title

        if len(title) > 30:
            title = title[:27] + "..."

        print(
            f"{book.book_id:<10} "
            f"{title:<30} "
            f"{book.total_copies:<8} "
            f"{book.available_copies:<12} "
            f"{borrowed:<10} "
            f"{status:<15}"
        )

    print("-" * 90)

    print("\nINVENTORY SUMMARY")
    print("-" * 45)
    print(f"Total Book Titles: {len(books)}")
    print(f"Total Book Copies: {total_copies}")
    print(f"Available Copies: {available_copies}")
    print(f"Borrowed Copies: {borrowed_copies}")

    print("\nSTOCK STATUS")
    print("-" * 45)
    print(f"Available Titles: {available_titles}")
    print(f"Low Stock Titles: {low_stock_titles}")
    print(f"Out of Stock Titles: {out_of_stock_titles}")

    availability_rate = (
        available_copies / total_copies * 100
        if total_copies > 0 else 0
    )

    print(f"\nInventory Availability: {availability_rate:.2f}%")
    print("\n============================================")


def reports_management(library):
    while True:
        display_reports_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            library_overview(library)

        elif choice == "2":
            books_by_category(library)

        elif choice == "3":
            member_statistics(library)

        elif choice == "4":
            loan_statistics(library)

        elif choice == "5":
            most_borrowed_books(library)

        elif choice == "6":
            overdue_loan_report(library)

        elif choice == "7":
            inventory_report(library)

        elif choice == "0":
            break

        else:
            print("Error: Invalid choice. Please try again.")






def main():
    library = Library()

    if not library.load_data():
        print("Error: Failed to load library data.")
        return

    
    while True:
        display_main_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            book_management(library)

        elif choice == "2":
            member_management(library)

        elif choice == "3":
            loan_management(library)

        elif choice == "4":
            reports_management(library)

        elif choice == "0":
            print("Thank you for using the Library Management System!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
