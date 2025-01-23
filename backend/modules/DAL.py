



class LibraryDAL:
    def __init__(self):
        self.books = []
        self.customers = []
        self.loans = []

    def add_customer(self, customer):
        self.customers.append(customer)

    def add_book(self, book):
        self.books.append(book)

    def loan_book(self, loan):
        self.loans.append(loan)

    def return_book(self, book_id, customer_id):
        self.loans = [loan for loan in self.loans if not (loan['book_id'] == book_id and loan['customer_id'] == customer_id)]

    def get_all_books(self):
        return self.books

    def get_all_customers(self):
        return self.customers

    def get_all_loans(self):
        return self.loans

    def get_late_loans(self):
        return [loan for loan in self.loans if loan.get('late', False)]

    def find_book_by_name(self, name):
        return [book for book in self.books if name.lower() in book['name'].lower()]

    def find_customer_by_name(self, name):
        return [customer for customer in self.customers if name.lower() in customer['name'].lower()]

    def remove_book(self, book_id):
        self.books = [book for book in self.books if book['id'] != book_id]

    def remove_customer(self, customer_id):
        self.customers = [customer for customer in self.customers if customer['id'] != customer_id]


