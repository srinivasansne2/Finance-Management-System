# 💰 Finance Management System (RBAC + Dashboard)

A full-stack finance management system built using **Django + Django
REST Framework** with **JWT authentication, role-based access control
(RBAC), advanced filtering, pagination, and interactive dashboard
charts**.

------------------------------------------------------------------------

## 🚀 Features

-   🔐 JWT Authentication (Login / Logout)
-   👥 Role-Based Access Control (Admin, Analyst, Data Entry, Viewer)
-   📊 Dashboard with Charts (Chart.js)
-   🔍 Global Search (category, type, note, amount)
-   📅 Date Range Filtering
-   📄 Pagination with Page Numbers
-   👤 User Management (Admin only)
-   📱 Fully Responsive UI

------------------------------------------------------------------------

## 👥 User Roles & Permissions

  Role         Dashboard   View Transactions   Add   Edit   Delete
  ------------ ----------- ------------------- ----- ------ --------
  Admin        ✅          ✅                  ✅    ✅     ✅
  Analyst      ✅          ✅                  ❌    ❌     ❌
  Data Entry   ✅          Own Data Only       ✅    ❌     ❌
  Viewer       ✅          ❌                  ❌    ❌     ❌

------------------------------------------------------------------------

## 📊 Dashboard Features

-   Total Income
-   Total Expense
-   Net Balance
-   Pie Chart → Category-wise expenses
-   Bar Chart → Income vs Expense

------------------------------------------------------------------------

## 🔍 Filtering System

-   Global search (category, type, note, amount)
-   Category filter
-   Type filter (income/expense)
-   Date range filter
-   Pagination integrated with filters

------------------------------------------------------------------------

## 🧱 Tech Stack

### Backend

-   Django
-   Django REST Framework
-   Simple JWT

### Frontend

-   Django Templates
-   Bootstrap 5
-   Chart.js

### Database

-   SQLite / PostgreSQL

------------------------------------------------------------------------

## ⚙️ Installation & Setup

``` bash
git clone https://github.com/your-username/finance-app.git
cd finance-app
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

------------------------------------------------------------------------

## 📸 Screenshots

Add your screenshots in a folder named `screenshots/`:

-   screenshots/login.png
-   screenshots/register.png
-   screenshots/dashboard.png
-   screenshots/transactions.png
-   screenshots/users.png
-   screenshots/profile.png

------------------------------------------------------------------------

## 💬 Author

**Srinivasan R**
Portfolio: https://sri.srinivasansne2.workers.dev/
------------------------------------------------------------------------

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
