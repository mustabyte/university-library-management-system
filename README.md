# 📚 University Library Management System

A Python-based University Library Management System featuring an interactive Streamlit web application, object-oriented programming, data visualization, and JSON-based storage.

The project provides tools for managing books, members, borrowing transactions, overdue loans, and library analytics through a centralized interface.

## ✨ Features

### 📊 Interactive Dashboard
- Library statistics and performance indicators
- Interactive charts using Plotly
- Book availability and borrowing insights
- Daily borrowing activity visualization

### 📚 Book Management
- Browse and search the book collection
- Add, edit, and remove books
- View detailed book information
- Manage available and total copies
- Filter books by relevant attributes

### 👥 Member Management
- Register and manage library members
- Support for student and faculty members
- View and update membership details
- Manage membership status

### 📖 Loan Management
- Borrow and return books
- Track active and overdue loans
- Enforce borrowing eligibility and limits
- View borrowing history and loan details
- Calculate overdue fines

### 📈 Reports & Analytics
- Book collection and category analysis
- Most borrowed books
- Member distribution and borrowing activity
- Monthly borrowing trends
- Overdue loan and fine analytics
- Export library reports as CSV files

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Object-Oriented Programming | Modular system architecture |
| Streamlit | Interactive web interface |
| Pandas | Data processing and reporting |
| Plotly | Interactive data visualizations |
| JSON | Data storage |
| Git & GitHub | Version control |

## 🏗️ Project Structure

```text
university-library-management-system/
├── app.py
├── main.py
├── book.py
├── member.py
├── loan.py
├── library.py
├── storage.py
├── data/
│   ├── books.json
│   ├── members.json
│   └── loans.json
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

**1. Clone the repository**

```bash
git clone https://github.com/mustabyte/university-library-management-system.git
cd university-library-management-system
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Run the Streamlit application**

```bash
streamlit run app.py
```

**4. Run the terminal application**

```bash
python main.py
```

## 🧠 Object-Oriented Design

The system separates responsibilities across multiple Python modules:

- `book.py` — Book entities and inventory information
- `member.py` — Library members and membership rules
- `loan.py` — Borrowing transactions and fine calculations
- `library.py` — Central library operations and business logic
- `storage.py` — JSON-based data persistence
- `main.py` — Terminal-based application
- `app.py` — Streamlit web interface

This architecture separates the application's business logic from its user interfaces.

## 💾 Data Storage

The application uses JSON files to store books, members, and borrowing transactions.

Both the terminal and Streamlit interfaces use the same underlying library logic and data structure.

**Note:** Local JSON storage is intended for learning and demonstration. Cloud deployments with ephemeral storage may not preserve updates after application restarts or redeployments. A persistent database is recommended for production use.


## 🚀 Live Demo

🌐 **[Launch University Library Management System](https://university-library-ms.streamlit.app/)**

The application is deployed on Streamlit Community Cloud.

### Features
- Interactive library dashboard
- Book and member management
- Borrowing and return management
- Overdue tracking and fine calculations
- Interactive Plotly analytics
- CSV report exports


## 🔮 Future Improvements

- Persistent database integration
- Authentication and role-based access
- Advanced search and filtering
- Automated overdue notifications
- Improved multi-user support

## 👨‍💻 Author

**Mustabshera Binte Junayed**

GitHub: [@mustabyte](https://github.com/mustabyte)

## 📄 Project Purpose

This project was developed to apply Python object-oriented programming, modular software design, data persistence, and interactive dashboard development to a practical library management scenario.
