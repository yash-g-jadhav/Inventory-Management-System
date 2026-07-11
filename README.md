# 🚀 Quick Commerce Inventory Management System

A desktop-based Inventory Management System inspired by quick commerce platforms like **Blinkit**, **Zepto**, and **Instamart**. The application provides a modern graphical interface to manage products, inventory, and customer orders using a **MySQL** backend.

---

## 📖 Project Overview

The **Quick Commerce Inventory Management System** is a database-driven desktop application developed as part of the **Database Management Systems (DBMS)** coursework. The project demonstrates the practical implementation of relational database concepts, including **ER Modeling**, **Normalization (3NF)**, **SQL operations**, and **GUI integration**.

The application enables users to efficiently manage products, inventory across warehouses, and customer orders while maintaining data integrity through MySQL.

---

## ✨ Features

- 🔐 Secure Login Screen
- 📊 Dashboard Overview
- 📦 Product Management
  - View Products
  - Add Products
  - Delete Products
  - Search Products
- 📦 Inventory Management
  - View Inventory
  - Update Stock
  - Low Stock Alerts
- 🛒 Order Management
  - Place New Orders
  - View Order History
- 🗄️ MySQL Database Integration
- 🎨 User-friendly Tkinter GUI

---

## 🛠️ Tech Stack

- **Programming Language:** Python
- **GUI Framework:** Tkinter
- **Database:** MySQL
- **Database Connector:** mysql-connector-python

---

## 📂 Project Structure

```text
Quick-Commerce-Inventory-System/
│
├── screenshots/
│   ├── login.png
│   ├── Dashboard.png
│   ├── Products.png
│   ├── Inventory.png
│   └── order.png
│
├── quick_commerce_gui.py
├── db_connection.py
├── schema.sql
├── config.py.example
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📋 Prerequisites

Before running the project, ensure you have:

- Python 3.10 or later
- MySQL Server
- MySQL Workbench (Recommended)
- Git (Optional)

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Quick-Commerce-Inventory-System.git
```

Replace `YOUR_USERNAME` with your GitHub username.

---

### 2️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Import the Database

Open **MySQL Workbench** and execute:

```
schema.sql
```

to create the database and tables.

---

### 4️⃣ Configure Database Credentials

Rename

```
config.py.example
```

to

```
config.py
```

Update the file with your MySQL credentials.

```python
HOST = "localhost"
USER = "root"
PASSWORD = "your_mysql_password"
DATABASE = "quickcommercedb"
```

---

### 5️⃣ Run the Application

```bash
python quick_commerce_gui.py
```

---

## 🔑 Demo Credentials

Use the following credentials to log in:

| Username | Password |
|----------|----------|
| **admin** | **admin** |

> **Note:** These credentials are hardcoded for demonstration purposes and can be modified in the source code.

---

## 📸 Application Screenshots

### 🔐 Login

![Login](screenshots/login.png)

---

### 📊 Dashboard

![Dashboard](screenshots/Dashboard.png)

---

### 📦 Product Management

![Products](screenshots/Products.png)

---

### 📦 Inventory Management

![Inventory](screenshots/Inventory.png)

---

### 🛒 Order Management

![Orders](screenshots/order.png)

---

## 🌐 Demo

**GitHub Repository:**

> **Repository Link:** **[Add your GitHub repository link here]**

**Desktop Application**

This project is a desktop application and can be run locally by following the installation steps above.

---

## 🚀 Future Enhancements

- Customer Management Module
- Supplier Management Module
- Warehouse Management
- Barcode Scanner Integration
- Export Reports to Excel/PDF
- Sales Analytics Dashboard
- Role-Based Authentication
- Cloud Database Support
- Docker Deployment
- REST API Integration

---

## 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- Relational Database Design
- Entity Relationship Modeling
- Database Normalization (up to 3NF)
- SQL (DDL, DML, Joins, Aggregation)
- CRUD Operations
- Database Connectivity using Python
- GUI Development with Tkinter

---

## 👨‍💻 Author

**Arjun**

Computer Engineering Student

Feel free to connect or provide feedback!

---

## 📄 License

This project was developed for educational purposes as part of the **Database Management Systems (DBMS)** course.

---

⭐ If you found this project useful, consider giving it a star!