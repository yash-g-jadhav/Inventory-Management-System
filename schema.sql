CREATE DATABASE QuickCommerceDB;
USE QuickCommerceDB;
SHOW DATABASES;
USE quickcommercedb;
CREATE TABLE Category (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL
);
CREATE TABLE Supplier (
    supplier_id INT PRIMARY KEY,
    supplier_name VARCHAR(100),
    contact_no VARCHAR(15)
);

CREATE TABLE Warehouse (
    warehouse_id INT PRIMARY KEY,
    location VARCHAR(100),
    capacity INT
);

CREATE TABLE Customer (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    email VARCHAR(100),
    address VARCHAR(200),
    city VARCHAR(50)
);

CREATE TABLE Delivery_Partner (
    partner_id INT PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(15),
    vehicle_no VARCHAR(20)
);

CREATE TABLE Product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100),
    price DECIMAL(10,2),
    category_id INT,
    supplier_id INT,

    FOREIGN KEY (category_id)
        REFERENCES Category(category_id),

    FOREIGN KEY (supplier_id)
        REFERENCES Supplier(supplier_id)
);

CREATE TABLE Inventory (
    inventory_id INT PRIMARY KEY,
    warehouse_id INT,
    product_id INT,
    stock_quantity INT,
    last_updated DATE,

    FOREIGN KEY (warehouse_id)
        REFERENCES Warehouse(warehouse_id),

    FOREIGN KEY (product_id)
        REFERENCES Product(product_id)
);

CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    warehouse_id INT,
    partner_id INT,
    order_date DATE,
    order_status VARCHAR(50),
    total_amount DECIMAL(10,2),

    FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id),

    FOREIGN KEY (warehouse_id)
        REFERENCES Warehouse(warehouse_id),

    FOREIGN KEY (partner_id)
        REFERENCES Delivery_Partner(partner_id)
);

CREATE TABLE Order_Items (
    order_item_id INT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),

    FOREIGN KEY (order_id)
        REFERENCES Orders(order_id),

    FOREIGN KEY (product_id)
        REFERENCES Product(product_id)
);

CREATE TABLE Payment (
    payment_id INT PRIMARY KEY,
    order_id INT UNIQUE,
    payment_method VARCHAR(50),
    payment_status VARCHAR(50),
    amount DECIMAL(10,2),

    FOREIGN KEY (order_id)
        REFERENCES Orders(order_id)
);

SHOW TABLES

SELECT * FROM Product;
SELECT * FROM Inventory;
SELECT * FROM Orders;