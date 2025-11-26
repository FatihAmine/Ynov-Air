# Ynov-Air Project ✈️

## Description
**Ynov-Air** is a Django-based flight management project that allows users to manage flights, passengers, bookings, and airlines.  
The project also includes analytics to monitor flight performance, booking trends, and airline statistics.

**Features:**
- List flights by airline and date  
- Manage passengers and bookings  
- Analyze flight and booking statistics  
- Custom features for airline management  

---

## Table of Contents
1. [Installation](#installation)  
2. [Running the Project](#running-the-project)  
3. [Project Structure](#project-structure)  
4. [Database & Sample Data](#database--sample-data)  
5. [SQL Queries](#sql-queries)  
6. [Admin Panel](#admin-panel)  
7. [Technologies Used](#technologies-used)  

---

## Installation

1. **Clone the project**
```bash
git clone YNOV air
cd ynovair

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver
```

Access the website: http://127.0.0.1:8000/

Access the admin panel: http://127.0.0.1:8000/admin

ynovair/
├── flights/         # Main app for flights, bookings, and passengers
├── ynov_air/        # Django project settings
├── templates/       # HTML templates
├── static/          # CSS, JS, images
├── db.sqlite3       # SQLite database
├── manage.py        # Django management script
└── README.md        # Project documentationa
