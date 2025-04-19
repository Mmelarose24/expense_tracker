# 💸 Simple Expense Tracker

A web-based Expense Tracker built with **Django** and styled using **Tailwind CSS via CDN Play**. This app helps users manage their daily expenses, categorize them, and stay on top of their budget goals.

---

## 🚀 Features

- User authentication (login/logout)
- Add, edit, and delete expenses
- Categorize expenses
- Dashboard with total expenses and filters
- Responsive design using **Tailwind CSS via CDN**

---

## 🛠️ Tech Stack

- **Backend:** Django
- **Frontend:** HTML, Tailwind CSS via [Play CDN](https://cdn.tailwindcss.com/)
- **Database:** SQLite
- **Templates:** Django Templates Engine

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mmelarose24/expense_tracker.git
   extract and open the cloned file in vscode

   python -m venv venv
   source venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver

http://127.0.0.1:8000/


📁 Project Structure
simple-expense-tracker/
├── expenses/              # Core expense tracking app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
├── templates/             # Base templates
├── manage.py
└── requirements.txt


🎨 Design
Tailwind CSS is integrated using CDN Play:
<script src="https://cdn.tailwindcss.com"></script>


