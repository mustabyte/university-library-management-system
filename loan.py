from datetime import date, timedelta


class Loan:
    def __init__(self, loan_id, book_id, member_id, loan_duration, fine_rate):
        if not isinstance(loan_id, str) or not loan_id.strip():
            raise ValueError("Loan ID cannot be empty and must be a string.")

        if not isinstance(book_id, str) or not book_id.strip():
            raise ValueError("Book ID cannot be empty and must be a string.")

        if not isinstance(member_id, str) or not member_id.strip():
            raise ValueError("Member ID cannot be empty and must be a string.")

        if type(loan_duration) is not int or loan_duration <= 0:
            raise ValueError("Loan duration must be a positive integer.")

        if type(fine_rate) is not int or fine_rate < 0:
            raise ValueError("Fine rate must be a nonnegative integer.")

        self.loan_id = loan_id.strip()
        self.book_id = book_id.strip()
        self.member_id = member_id.strip()
        self.fine_rate = fine_rate

        today = date.today()

        self.borrow_date = today.isoformat()
        self.due_date = (today + timedelta(days=loan_duration)).isoformat()
        self.return_date = None
        self.status = "Active"

    def is_active(self):
        return self.status == "Active"

    def is_overdue(self):
        return self.is_active() and date.today() > date.fromisoformat(self.due_date)

    def get_overdue_days(self):
        if not self.is_overdue():
            return 0

        return (date.today() - date.fromisoformat(self.due_date)).days

    def calculate_fine(self):
        return self.get_overdue_days() * self.fine_rate

    def return_book(self):
        if not self.is_active():
            return False

        fine = self.calculate_fine()
        self.return_date = date.today().isoformat()
        self.status = "Returned"

        return fine

    def to_dict(self):
        return {
            "loan_id": self.loan_id,
            "book_id": self.book_id,
            "member_id": self.member_id,
            "borrow_date": self.borrow_date,
            "due_date": self.due_date,
            "return_date": self.return_date,
            "fine_rate": self.fine_rate,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Loan data must be a dictionary.")

        required_fields = [
            "loan_id",
            "book_id",
            "member_id",
            "borrow_date",
            "due_date",
            "return_date",
            "fine_rate",
            "status"
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        try:
            borrow_date = date.fromisoformat(data["borrow_date"])
            due_date = date.fromisoformat(data["due_date"])
        except (TypeError, ValueError):
            raise ValueError("Invalid borrow date or due date.")

        loan_duration = (due_date - borrow_date).days

        if loan_duration <= 0:
            raise ValueError("Due date must be after borrow date.")

        if data["status"] not in ("Active", "Returned"):
            raise ValueError("Invalid loan status.")

        if data["return_date"] is not None:
            try:
                return_date = date.fromisoformat(data["return_date"])
            except (TypeError, ValueError):
                raise ValueError("Invalid return date.")

            if return_date < borrow_date:
                raise ValueError("Return date cannot be before borrow date.")

            if return_date > date.today():
                raise ValueError("Return date cannot be in the future.")

        if data["status"] == "Active" and data["return_date"] is not None:
            raise ValueError("Active loan cannot have a return date.")

        if data["status"] == "Returned" and data["return_date"] is None:
            raise ValueError("Returned loan must have a return date.")

        loan = cls(
            data["loan_id"],
            data["book_id"],
            data["member_id"],
            loan_duration,
            data["fine_rate"]
        )

        loan.borrow_date = borrow_date.isoformat()
        loan.due_date = due_date.isoformat()
        loan.return_date = data["return_date"]
        loan.status = data["status"]

        return loan

    def __str__(self):
        display_date = self.return_date if self.return_date is not None else "Not Returned"

        return (
            f"Loan ID: {self.loan_id} | "
            f"Book ID: {self.book_id} | "
            f"Member ID: {self.member_id} | "
            f"Borrow Date: {self.borrow_date} | "
            f"Due Date: {self.due_date} | "
            f"Return Date: {display_date} | "
            f"Fine Rate: ৳{self.fine_rate}/day | "
            f"Status: {self.status}"
        )