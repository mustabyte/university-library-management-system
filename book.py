class Book:
    def __init__(self, book_id,title,author,category,total_copies):
        if not isinstance(book_id , str) or not book_id.strip():
            raise ValueError ("Book ID cannot be empty and must be a string.")
        self.book_id= book_id.strip()

        if not isinstance(title , str) or not title.strip():
            raise ValueError ("Title cannot be empty and must be a string.")
        self.title=title.strip()

        if not isinstance(author , str) or not author.strip():
            raise ValueError ("Author cannot be empty and must be a string.")
        self.author=author.strip()

        if not isinstance(category , str) or not category.strip():
            raise ValueError ("Category cannot be empty and must be a string.")
        self.category=category.strip()

        if type(total_copies) is not int or total_copies <= 0:
            raise ValueError ("Total copies must be a positive integer.")
        self.total_copies= total_copies

        self.available_copies = self.total_copies

    def is_available(self):
        if self.available_copies>0:
            return True
        else:
            return False

    def borrow_copy(self):
        available = self.is_available()

        if available == True:
            self.available_copies-=1
            return True
        else:
            return False

    def return_copy(self):
        if self.available_copies<self.total_copies:
            self.available_copies+=1
            return True
        else:
            return False

    def add_copies(self,quantity):
        if type (quantity) is not int or quantity<=0:
            return False
        else:
            self.total_copies = self.total_copies+quantity
            self.available_copies= self.available_copies +quantity
            return True

    def remove_copies(self,quantity):
        if type (quantity) is not int or quantity<=0:
            return False
        else:
            if quantity>self.available_copies:
                return False
            else:
                if self.total_copies - quantity < 1:
                    return False
                self.total_copies = self.total_copies-quantity
                self.available_copies= self.available_copies -quantity

                return True

    def update_info(self, title=None,author=None,category=None):
        if title is not None:
            if not isinstance(title , str) or not title.strip():
                return False 

        if author is not None:
            if not isinstance(author , str) or not author.strip():
                return False 

        if category is not None:
            if not isinstance(category , str) or not category.strip():
                return False 

        if title is not None:
            self.title = title.strip()

        if author is not None:
            self.author = author.strip()

        if category is not None:
            self.category= category.strip()

        return True

    def to_dict(self):
        return {
            'book_id' : self.book_id,
            'title' : self.title,
            'author' : self.author,
            'category' : self.category,
            'total_copies' : self.total_copies,
            'available_copies' : self.available_copies
            
        }

    @classmethod
    def from_dict(cls, data):

        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary.")

        book = cls(
            data["book_id"],
            data["title"],
            data["author"],
            data["category"],
            data["total_copies"]
        )

        available = data["available_copies"]

        if type(available) is not int or not (0 <= available <= book.total_copies):
            raise ValueError("Invalid available copies.")

        book.available_copies = available 

        return book

    def __str__(self):
        return (
            f"Book ID: {self.book_id} | "
            f"Title: {self.title} | "
            f"Author: {self.author} | "
            f"Category: {self.category} | "
            f"Total Copies: {self.total_copies} | "
            f"Available Copies: {self.available_copies}"
        )

    
