# Text-to-SQL

Project of a local application that generates queries from natural language using AI (nsql-350M).

To run the code just run main.py. The others archives like AI_test.py and DB_test can be ignored.

##Creating database orders in MySQL:
```SQL
CREATE DATABASE Orders;
USE Orders;

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(50),
    Email VARCHAR(30)
);

CREATE TABLE Orders (
    OrderID INT PRIMARY KEY AUTO_INCREMENT,
    CustomerID INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT,
    ProductName VARCHAR(100),
    Price DECIMAL(10,2)
);

CREATE TABLE OrderDetails (
    DetailID INT PRIMARY KEY AUTO_INCREMENT,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```


##Creating database orders in PostgreSQL:
```SQL
CREATE DATABASE Orders;
\c Orders;

CREATE TABLE Customers (
    CustomerID SERIAL PRIMARY KEY,
    Name VARCHAR(50),
    Email VARCHAR(30)
);

CREATE TABLE Orders (
    OrderID SERIAL PRIMARY KEY,
    CustomerID INT,
    OrderDate DATE,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE Products (
    ProductID SERIAL PRIMARY KEY,
    ProductName VARCHAR(100),
    Price DECIMAL(10,2)
);

CREATE TABLE OrderDetails (
    DetailID SERIAL PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
```

##Example insert values(work for both MySQL and PostgreSQL)
```SQL
INSERT INTO Customers (Name, Email) VALUES 
('Alice Johnson', 'alice@email.com'),
('Carlos Smith', 'carlos@email.com'),
('Beatrice Brown', 'beatrice@email.com');

INSERT INTO Orders (CustomerID, OrderDate) VALUES 
(1, '2025-06-10'),
(2, '2025-06-11'),
(3, '2025-06-12');

INSERT INTO Products (ProductName, Price) VALUES 
('Laptop', 3500.00),
('Keyboard', 150.00),
('Mouse', 80.00);

INSERT INTO OrderDetails (OrderID, ProductID, Quantity) VALUES 
(1, 1, 1),
(1, 2, 2),
(2, 3, 1),
(3, 1, 1),
(3, 3, 2);
```