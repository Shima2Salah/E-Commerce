-- Drop database
DROP DATABASE IF EXISTS ecommerce;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS ecommerce;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost';
SET PASSWORD FOR 'hbnb_dev'@'localhost' = 'hbnb_dev_pwd';
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;

USE ecommerce;

-- Table structure for table categories

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `name` VARCHAR(255) UNIQUE NOT NULL
);
-- Table structure for table products

DROP TABLE IF EXISTS `products`;
CREATE TABLE `products` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `product_name` VARCHAR(255) NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    `description` VARCHAR(255),
    `image_url` VARCHAR(255),
    `category_id` INT NOT NULL,
    KEY `category_id` (`category_id`),
    CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES categories(`id`)
);
-- Table structure for table users

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `username` VARCHAR(255) NOT NULL,
    `contact_number` VARCHAR(100) NOT NULL,
    `email` VARCHAR(100) UNIQUE NOT NULL,
    `password_hash` VARCHAR(100) NOT NULL
);
-- Table structure for table orders

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `total_price` DECIMAL(10, 2) NOT NULL,
    KEY `user_id` (`user_id`),
    CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES users(`id`)
);
-- Table structure for table order_items

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `order_id` INT NOT NULL,
    `product_id` INT NOT NULL,
    `quantity` INT NOT NULL,
    `price` DECIMAL(10, 2) NOT NULL,
    KEY `order_id` (`order_id`),
    KEY `product_id` (`product_id`),
    CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES orders(`id`),
    CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES products(`id`)
);

-- Dummy data for categories table
INSERT INTO categories (name) VALUES
('Women'),
('Men'),
('Children');

-- Dummy data for products table
INSERT INTO products (product_name, price, description, image_url, category_id) VALUES
('Tank Top', 15.99, 'Sleeveless top for women', 'tank_top.jpg', 1),
('Corater', 29.99, 'Stylish corater for men', 'corater.jpg', 2),
('Polo Shirt', 24.99, 'Classic polo shirt for children', 'polo_shirt.jpg', 3),
('Cushion Cover Set', 19.99, 'Decorative cushion cover set', 'cushion_cover.jpg', 1),
('Throw Blanket', 39.99, 'Soft and cozy throw blanket', 'throw_blanket.jpg', 1),
('Wall Clock', 29.99, 'Modern wall clock', 'wall_clock.jpg', 1),
('Decorative Vase', 49.99, 'Elegant decorative vase', 'vase.jpg', 1),
('Area Rug', 79.99, 'Soft area rug for living room', 'area_rug.jpg', 1),
('Bedding Set', 89.99, 'Luxurious bedding set', 'bedding_set.jpg', 1),
('Curtain Panels', 29.99, 'Set of two curtain panels', 'curtain_panels.jpg', 1),
('Table Lamp', 59.99, 'Contemporary table lamp', 'table_lamp.jpg', 1),
('Dining Set', 299.99, 'Modern dining set for 4', 'dining_set.jpg', 1),
('Plant Stand', 34.99, 'Metal plant stand for indoor use', 'plant_stand.jpg', 1);

-- Dummy data for users table
INSERT INTO users (username, contact_number, email, password_hash) VALUES
('john_doe', '123456789', 'john@example.com', '123456'),
('jane_smith', '987654321', 'jane@example.com', '123456');

-- Dummy data for orders table
INSERT INTO orders (user_id, total_price) VALUES
(1, 689.92),
(2, 404.94);

-- Dummy data for order_items table
INSERT INTO order_items (order_id, product_id, quantity, price) VALUES
(1, 1, 2, 39.98),
(1, 4, 1, 49.99),
(1, 6, 1, 89.99),
(2, 2, 2, 59.98),
(2, 5, 1, 79.99),
(2, 7, 2, 59.98),
(2, 10, 1, 299.99),
(2, 11, 1, 34.99);
