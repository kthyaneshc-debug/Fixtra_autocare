CREATE DATABASE IF NOT EXISTS novadrive_autocare_db;
USE novadrive_autocare_db;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(25) NOT NULL,
    email VARCHAR(120),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    registration_no VARCHAR(30) NOT NULL UNIQUE,
    make VARCHAR(80) NOT NULL,
    model VARCHAR(80) NOT NULL,
    year INT,
    fuel_type ENUM('Petrol','Diesel','CNG','Electric','Hybrid','Other') DEFAULT 'Petrol',
    odometer_km INT DEFAULT 0,
    vin VARCHAR(80),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS service_catalog (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(120) NOT NULL UNIQUE,
    category VARCHAR(80) NOT NULL,
    default_price DECIMAL(10,2) DEFAULT 0,
    estimated_hours DECIMAL(5,2) DEFAULT 1
);

CREATE TABLE IF NOT EXISTS service_jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id INT NOT NULL,
    advisor_name VARCHAR(100),
    complaint TEXT,
    diagnosis TEXT,
    status ENUM('Booked','In Progress','Waiting Parts','Ready','Completed','Cancelled') DEFAULT 'Booked',
    priority ENUM('Normal','Urgent') DEFAULT 'Normal',
    check_in DATETIME DEFAULT CURRENT_TIMESTAMP,
    promised_date DATE,
    next_service_date DATE,
    next_service_km INT,
    labor_cost DECIMAL(10,2) DEFAULT 0,
    parts_cost DECIMAL(10,2) DEFAULT 0,
    discount DECIMAL(10,2) DEFAULT 0,
    tax DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) DEFAULT 0,
    payment_status ENUM('Unpaid','Partial','Paid') DEFAULT 'Unpaid',
    notes TEXT,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS job_services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    service_id INT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (job_id) REFERENCES service_jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES service_catalog(service_id)
);

CREATE TABLE IF NOT EXISTS parts (
    part_id INT AUTO_INCREMENT PRIMARY KEY,
    part_name VARCHAR(150) NOT NULL,
    part_number VARCHAR(80),
    category VARCHAR(80),
    stock_qty INT DEFAULT 0,
    reorder_level INT DEFAULT 5,
    unit_price DECIMAL(10,2) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS job_parts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    part_id INT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (job_id) REFERENCES service_jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (part_id) REFERENCES parts(part_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method ENUM('Cash','UPI','Card','Bank Transfer','Other') DEFAULT 'Cash',
    paid_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reference_no VARCHAR(100),
    FOREIGN KEY (job_id) REFERENCES service_jobs(job_id) ON DELETE CASCADE
);

INSERT IGNORE INTO service_catalog(service_name, category, default_price, estimated_hours) VALUES
('General Service','Periodic Maintenance',1500,2),
('Engine Oil & Filter','Periodic Maintenance',1200,1),
('Brake Inspection','Safety',500,1),
('Brake Pad Replacement','Brakes',2500,2),
('Wheel Alignment','Tyres & Wheels',800,1),
('Wheel Balancing','Tyres & Wheels',700,1),
('AC Service','AC & Electrical',1800,2),
('Battery Check','Electrical',300,0.5),
('Full Diagnostic Scan','Diagnostics',1000,1),
('Coolant Flush','Cooling System',1200,1),
('Transmission Service','Transmission',3500,3),
('EV Battery Health Check','EV / Hybrid',1500,1),
('Hybrid System Inspection','EV / Hybrid',1800,1.5),
('Tyre Replacement','Tyres & Wheels',0,1),
('Exterior Detailing','Detailing',2500,3);
