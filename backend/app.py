from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
from modules import *
from logger import *
from flask_migrate import Migrate




# Initialize the Flask application
app = Flask(__name__)
CORS(app)



# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# For update the database
migrate = Migrate(app, db)
# Create the database tables
with app.app_context():
    db.create_all()
    print("Tables created!")

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    year_published = db.Column(db.String(4), nullable=False)
    kind = db.Column(db.String(20), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year_published": self.year_published,
            "kind": self.kind
        }



class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), nullable=False)
    City = db.Column(db.String(200), nullable=True)
    Age = db.Column(db.Integer, nullable=False)
    Phone_Number = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "Name": self.Name,
            "City": self.City,
            "Age": self.Age,
            "Phone_Number": self.Phone_Number
        }



class Loan(db.Model):
    CustID = db.Column(db.Integer, primary_key=True)
    BookID = db.Column(db.String(200), nullable=False)
    LoanDate = db.Column(db.Date, nullable=True)
    ReturnDate = db.Column(db.Date, nullable=False)
    Phone_Number = db.Column(db.String(200), nullable=True)
    

    def __init__(self, CustID, BookID, LoanDate=None, ReturnDate=None, Phone_Number=None, Type=0):
        self.CustID = CustID
        self.BookID = BookID
        self.LoanDate = LoanDate or datetime.today().date()
        self.ReturnDate = ReturnDate
        self.Phone_Number = Phone_Number
        self.Type = Type

    def to_dict(self):
        return {
            "CustID": self.CustID,
            "BookID": self.BookID,
            "LoanDate": self.LoanDate,
            "ReturnDate": self.ReturnDate,
            "Phone_Number": self.Phone_Number
            
        }
    



# Routes
@app.route('/')
def home():
    return 'Welcome to the Library Booking System!'

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    year_published = data.get('year_published')
    kind = data.get('kind')

    if not title or not author or not year_published or not kind:
        return jsonify({'error': 'Title, Author,  Year Published and kind are required'}), 400

    book = Book(title=title, author=author, year_published=year_published, kind = kind)
    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Book added successfully', 'book': book.to_dict()}), 201

# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200

# Read a single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book.to_dict()), 200

# Update a book
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.year_published = data.get('year_published', book.year_published)

    db.session.commit()

    return jsonify({"message": "Book updated", "id": book.id})

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 200

#CRUD for custome
#Create a customer - 
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    name = data.get('Name')
    city = data.get('City')
    age = data.get('Age')
    phone_number = data.get('Phone_Number')

    if not name or not age:
        return jsonify({'error': 'Name and Age are required'}), 400

    customer = Customer(Name=name, City=city, Age=age, Phone_Number=phone_number)
    db.session.add(customer)
    db.session.commit()

    return jsonify({'message': 'Customer added successfully', 'customer': customer.to_dict()}), 201

# Read all customers -
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers]), 200

# Read a single customer
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    return jsonify(customer.to_dict()), 200

# Update a customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json()
    customer.Name = data.get('Name', customer.Name)
    customer.City = data.get('City', customer.City)
    customer.Age = data.get('Age', customer.Age)
    customer.Phone_Number = data.get('Phone_Number', customer.Phone_Number)

    db.session.commit()

    return jsonify({"message": "Customer updated", "id": customer.id}), 200

# Delete a customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({'message': 'Customer deleted successfully'}), 200
#Crud for loan - 
# Create a new loan
@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.get_json()
    cust_id = data.get('CustID')
    book_id = data.get('BookID')
    loan_date = data.get('LoanDate')
    return_date = data.get('ReturnDate')
    phone_number = data.get('Phone_Number')

    if not cust_id or not book_id or not return_date:
        return jsonify({'error': 'CustID, BookID, and ReturnDate are required'}), 400

    loan = Loan(CustID=cust_id, BookID=book_id, LoanDate=loan_date, ReturnDate=return_date, Phone_Number=phone_number)
    db.session.add(loan)
    db.session.commit()

    return jsonify({'message': 'Loan created successfully', 'loan': loan.to_dict()}), 201
def set_return_date(self):
    """Set the ReturnDate based on the book type."""
    if self.type == 1:
        max_loan_days = 10
        self.ReturnDate = self.LoanDate + timedelta(days=max_loan_days)
        return "Need to return the book in 10 days"
    elif self.type == 2:
        max_loan_days = 5
        self.ReturnDate = self.LoanDate + timedelta(days=max_loan_days)
        return "Need to return the book in 5 days"
    elif self.type == 3:
        max_loan_days = 2
        self.ReturnDate = self.LoanDate + timedelta(days=max_loan_days)
        return "Need to return the book in 2 days"
    else:
        raise ValueError("Invalid book type")



# Read all loans
@app.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([loan.to_dict() for loan in loans]), 200

# Read a single loan
@app.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = Loan.query.get(loan_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    return jsonify(loan.to_dict()), 200

# Update a loan
@app.route('/loans/<int:cust_id>', methods=['PUT'])
def update_loan(cust_id):
    loan = Loan.query.get(cust_id)
    if not loan:
        return jsonify({"message": "Loan not found"}), 404

    data = request.get_json()
    loan.BookID = data.get('BookID', loan.BookID)
    loan.LoanDate = data.get('LoanDate', loan.LoanDate)
    loan.ReturnDate = data.get('ReturnDate', loan.ReturnDate)
    loan.Phone_Number = data.get('Phone_Number', loan.Phone_Number)

    db.session.commit()

    return jsonify({"message": "Loan updated", "id": loan.CustID}), 200

# Delete a loan
@app.route('/loans/<int:cust_id>', methods=['DELETE'])
def delete_loan(cust_id):
    loan = Loan.query.get(cust_id)
    if not loan:
        return jsonify({'error': 'Loan not found'}), 404

    db.session.delete(loan)
    db.session.commit()

    return jsonify({'message': 'Loan deleted successfully'}), 200

# Run the application
if __name__ == "__main__":
     with app.app_context():
       db.create_all()  

       
        
       
