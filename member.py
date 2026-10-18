from datetime import date


class Member:
    def __init__(self,  member_id, name, email, phone):
        if not isinstance(member_id , str) or not member_id.strip():
            raise ValueError (" Member ID cannot be empty and must be a string.")
        self.member_id= member_id.strip()

        if not isinstance(name , str) or not name.strip():
            raise ValueError (" Name cannot be empty and must be a string.")
        self.name= name.strip()

        if not isinstance(email , str) or not email.strip():
            raise ValueError (" Email cannot be empty and must be a string.")
        self.email= email.strip()

        if not isinstance(phone , str) or not phone.strip():
            raise ValueError (" Phone cannot be empty and must be a string.")
        self.phone= phone.strip()

        self.join_date= date.today().isoformat()
        self.status = "Active"


    def is_active(self):
        if self.status == 'Active':
            return True
        else:
            return False


    def suspend(self):
        if self.is_active():
            self.status = 'Suspended'
            return True
        else:
            return False

    def activate(self):
        if not self.is_active():
            self.status = 'Active'
            return True
        else:
            return False

    def update_info(self, name=None,email=None,phone=None):
            if name is not None:
                if not isinstance(name , str) or not name.strip():
                    return False 
    
            if email is not None:
                if not isinstance(email , str) or not email.strip():
                    return False 
    
            if phone is not None:
                if not isinstance(phone , str) or not phone.strip():
                    return False 
    
            if name is not None:
                self.name = name.strip()
    
            if email is not None:
                self.email = email.strip()
    
            if phone is not None:
                self.phone= phone.strip()
    
            return True

    def get_max_books(self):
        raise NotImplementedError("Subclasses must implement get_max_books().")

    def get_loan_duration(self):
        raise NotImplementedError("Subclasses must implement get_loan_duration().")

    def get_fine_rate(self):
        raise NotImplementedError("Subclasses must implement get_fine_rate().")
    

    def to_dict(self):
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "join_date": self.join_date,
            "status": self.status,
            "member_type": self.member_type
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")

        member_type = data["member_type"]

        if member_type == "Student":
            member_class = StudentMember
        elif member_type == "Faculty":
            member_class = FacultyMember
        else:
            raise ValueError("Invalid member type.")

        member = member_class(
            data["member_id"],
            data["name"],
            data["email"],
            data["phone"]
        )

        join_date = data["join_date"]
        status = data["status"]

        if not isinstance(join_date, str):
            raise ValueError("Invalid joining date.")

        try:
            date.fromisoformat(join_date)
        except ValueError:
            raise ValueError("Invalid joining date.")

        if not isinstance(status, str) or status not in ("Active", "Suspended"):
            raise ValueError("Invalid member status.")

        member.join_date = join_date
        member.status = status

        return member

    def __str__(self):
        return (
            f"Member ID: {self.member_id} | "
            f"Name: {self.name} | "
            f"Member Type: {self.member_type} | "
            f"Email: {self.email} | "
            f"Phone: {self.phone} | "
            f"Join Date: {self.join_date} | "
            f"Status: {self.status}"
        )
    
class StudentMember(Member):
    def __init__(self,  member_id, name, email, phone):
        super().__init__(member_id, name, email, phone)
        self.member_type = "Student"

    def get_max_books(self):
        return 3

    def get_loan_duration(self):
        return 14


    def get_fine_rate(self):
        return 10

    def get_borrowing_policy(self):
        return {
            "max_books": self.get_max_books(),
            "loan_duration": self.get_loan_duration(),
            "fine_rate": self.get_fine_rate()
        }


class FacultyMember(Member):
    def __init__(self,  member_id, name, email, phone):
        super().__init__(member_id, name, email, phone)
        self.member_type = "Faculty"

    def get_max_books(self):
        return 5

    def get_loan_duration(self):
        return 30


    def get_fine_rate(self):
        return 5

    def get_borrowing_policy(self):
        return {
            "max_books": self.get_max_books(),
            "loan_duration": self.get_loan_duration(),
            "fine_rate": self.get_fine_rate()
        }

    


    