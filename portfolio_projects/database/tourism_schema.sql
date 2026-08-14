CREATE DATABASE Tourism;
USE Tourism;

-- Таблица услуг
CREATE TABLE Services (
    service_id INT PRIMARY KEY AUTO_INCREMENT,
    service_name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL
);

-- Таблица туров
CREATE TABLE Tours (
    tour_id INT PRIMARY KEY AUTO_INCREMENT,
    tour_name VARCHAR(100) NOT NULL,
    duration INT NOT NULL,
    location VARCHAR(100) NOT NULL
);

-- Таблица клиентов
CREATE TABLE Clients (
    client_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15)
);

-- Таблица заказов
CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    client_id INT,
    tour_id INT,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (tour_id) REFERENCES Tours(tour_id)
);

-- Таблица заказанных услуг
CREATE TABLE Ordered_Services (
    ordered_service_id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    service_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (service_id) REFERENCES Services(service_id)
);