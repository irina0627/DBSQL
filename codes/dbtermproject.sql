-- Vendor
CREATE TABLE Vendor (
    Vendor_ID INT,
    Vendor_name VARCHAR(25) NOT NULL,
    Vendor_address TEXT NOT NULL,
    Tel_No VARCHAR(20) NOT NULL,
    Fax_No VARCHAR(20),
    CONSTRAINT Vendor_ID_pk PRIMARY KEY(Vendor_ID)
);

-- Business_Location
CREATE TABLE Business_Location (
    Location_ID INT,
    Location_name VARCHAR(50) NOT NULL,
    Location_address TEXT NOT NULL,
    Tel_No VARCHAR(20) NOT NULL,
    Fax_No VARCHAR(20),
    Owner_name VARCHAR(25),
    Owner_tel_No VARCHAR(20),
    Manager_name VARCHAR(25),
    Manager_tel_No VARCHAR(20),
    Comments TEXT,
    CONSTRAINT Location_ID_pk PRIMARY KEY(Location_ID)
);

-- Product
CREATE TABLE Product (
    Product_ID INT AUTO_INCREMENT,
    Product_name VARCHAR(50) NOT NULL,
    Unit_price DECIMAL(10, 2) NOT NULL,
    Manufacturer VARCHAR(50),
    CONSTRAINT Product_ID_pk PRIMARY KEY(Product_ID),
    CHECK (Unit_price > 0)

);

-- Machine
CREATE TABLE Machine (
    Machine_ID INT,
    Location_ID INT,
    Product_ID INT,
    Machine_condition VARCHAR(50),
    Pur_date DATE NOT NULL,
    Manufacturer VARCHAR(50),
    Cost DECIMAL(10, 2) NOT NULL,
    CONSTRAINT Machine_ID_pk PRIMARY KEY(Machine_ID),
    CONSTRAINT Machine_Location_fk FOREIGN KEY (Location_ID) REFERENCES Business_Location(Location_ID) ON DELETE CASCADE,
    CONSTRAINT Machine_Product_fk FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE,
    CHECK (Cost > 0)
);

-- Purchase_Request
CREATE TABLE Purchase_Request (
    Request_ID INT,
    Location_ID INT,
    Date DATE,
    Comments TEXT,
    CONSTRAINT Request_ID_pk PRIMARY KEY(Request_ID),
    CONSTRAINT PurchaseRequest_Location_fk FOREIGN KEY (Location_ID) REFERENCES Business_Location(Location_ID) ON DELETE CASCADE
);

-- Purchase_Request_Product_Quantity
CREATE TABLE Purchase_Request_Product_Quantity (
    Request_ID INT,
    Product_ID INT,
    Quantity INT NOT NULL,
    CONSTRAINT PRPQ_pk PRIMARY KEY(Request_ID, Product_ID),
    CONSTRAINT PRPQ_Request_fk FOREIGN KEY (Request_ID) REFERENCES Purchase_Request(Request_ID) ON DELETE CASCADE,
    CONSTRAINT PRPQ_Product_fk FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE,
    CHECK (Quantity > 0)
);

-- Purchase_Order
CREATE TABLE Purchase_Order (
    Pur_order_ID INT,
    Vendor_ID INT,
    Date DATE NOT NULL,
    CONSTRAINT Pur_order_ID_pk PRIMARY KEY(Pur_order_ID),
    CONSTRAINT PurchaseOrder_Vendor_fk FOREIGN KEY (Vendor_ID) REFERENCES Vendor(Vendor_ID) ON DELETE CASCADE
);

-- Purchase_Order_Product_Quantity
CREATE TABLE Purchase_Order_Product_Quantity (
    Pur_order_ID INT,
    Product_ID INT,
    Quantity INT NOT NULL,
    CONSTRAINT POPQ_pk PRIMARY KEY(Pur_order_ID, Product_ID),
    CONSTRAINT POPQ_Order_fk FOREIGN KEY (Pur_order_ID) REFERENCES Purchase_Order(Pur_order_ID) ON DELETE CASCADE,
    CONSTRAINT POPQ_Product_fk FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE,
    CHECK (Quantity > 0)
);

-- Invoice
CREATE TABLE Invoice (
    Invoice_ID INT,
    Pur_order_ID INT,
    Vendor_ID INT,
    Machine_ID INT,
    Invoice_date DATE NOT NULL,
    Ship_date DATE NOT NULL,
    Ship_address TEXT NOT NULL,
    Terms TEXT,
    Shipping_charge DECIMAL(10, 2) NOT NULL,
    Sales_tax DECIMAL(10, 2) NOT NULL,
    Credit_due DATE NOT NULL,
    CONSTRAINT Invoice_ID_pk PRIMARY KEY(Invoice_ID),
    CONSTRAINT Invoice_PurchaseOrder_fk FOREIGN KEY (Pur_order_ID) REFERENCES Purchase_Order(Pur_order_ID) ON DELETE CASCADE,
    CONSTRAINT Invoice_Vendor_fk FOREIGN KEY (Vendor_ID) REFERENCES Vendor(Vendor_ID) ON DELETE CASCADE,
    CONSTRAINT Invoice_Machine_fk FOREIGN KEY (Machine_ID) REFERENCES Machine(Machine_ID) ON DELETE CASCADE,
    CHECK (Shipping_charge > 0),
    CHECK (Sales_tax > 0),
    CHECK (Credit_due > 0)
);

-- Product_Invoice_Quantity
CREATE TABLE Product_Invoice_Quantity (
    Invoice_ID INT,
    Product_ID INT,
    Quantity INT NOT NULL,
    CONSTRAINT PIQ_pk PRIMARY KEY(Invoice_ID, Product_ID),
    CONSTRAINT PIQ_Invoice_fk FOREIGN KEY (Invoice_ID) REFERENCES Invoice(Invoice_ID) ON DELETE CASCADE,
    CONSTRAINT PIQ_Product_fk FOREIGN KEY (Product_ID) REFERENCES Product(Product_ID) ON DELETE CASCADE,
    CHECK (Quantity > 0)
);

-- Technician
CREATE TABLE Technician (
    Technician_ID INT,
    Technician_name VARCHAR(25) NOT NULL,
    CONSTRAINT Technician_ID_pk PRIMARY KEY(Technician_ID)
);

-- Order
CREATE TABLE `Order` (
    Order_ID INT,
    Location_ID INT,
    Technician_ID INT,
    Machine_ID INT,
    Move_type VARCHAR(50) NOT NULL,
    Move_date DATE NOT NULL,
    CONSTRAINT Order_ID_pk PRIMARY KEY(Order_ID),
    CONSTRAINT Order_Location_fk FOREIGN KEY (Location_ID) REFERENCES Business_Location(Location_ID) ON DELETE CASCADE,
    CONSTRAINT Order_Technician_fk FOREIGN KEY (Technician_ID) REFERENCES Technician(Technician_ID) ON DELETE CASCADE,
    CONSTRAINT Order_Machine_fk FOREIGN KEY (Machine_ID) REFERENCES Machine(Machine_ID) ON DELETE CASCADE
);

-- Contract
CREATE TABLE Contract (
    Contract_ID INT,
    Location_ID INT,
    Contract_start_date DATE NOT NULL,
    Contract_end_date DATE NOT NULL,
    CONSTRAINT Contract_ID_pk PRIMARY KEY(Contract_ID),
    CONSTRAINT Contract_Location_fk FOREIGN KEY (Location_ID) REFERENCES Business_Location(Location_ID) ON DELETE CASCADE
);

-- Contract_Machine
CREATE TABLE Contract_Machine (
    Contract_ID INT,
    Machine_ID INT,
    CONSTRAINT CM_pk PRIMARY KEY(Contract_ID, Machine_ID),
    CONSTRAINT CM_Contract_fk FOREIGN KEY (Contract_ID) REFERENCES Contract(Contract_ID) ON DELETE CASCADE,
    CONSTRAINT CM_Machine_fk FOREIGN KEY (Machine_ID) REFERENCES Machine(Machine_ID) ON DELETE CASCADE
);

SHOW TABLES;

DESC Business_Location;
DESC Contract;
DESC Contract_Machine;
DESC Invoice;
DESC Machine;
DESC `Order`;
DESC Product;
DESC Product_Invoice_Quantity;
DESC Purchase_Order;
DESC Purchase_Order_Product_Quantity;
DESC Purchase_Request;
DESC Purchase_Request_Product_Quantity;
DESC Technician;
DESC Vendor;

SELECT CONSTRAINT_NAME, CONSTRAINT_TYPE, TABLE_NAME
FROM information_schema.table_constraints
WHERE table_schema = 'Term_project';


-- Vendor
INSERT INTO Vendor (Vendor_ID, Vendor_name, Vendor_address, Tel_No, Fax_No) VALUES
(1, 'Tech Supply Co.', '123 Silicon Valley', '555-123-4567', '555-123-4568'),
(2, 'Global Electronics', '456 Circuit Rd', '555-234-5678', '555-234-5679'),
(3, 'Machinery Inc.', '789 Industry Ave', '555-345-6789', '555-345-6790'),
(4, 'Hardware Solutions', '101 Hardware Blvd', '555-456-7890', '555-456-7891'),
(5, 'Industrial Equipments', '202 Tools St', '555-567-8901', '555-567-8902'),
(6, 'Advanced Mechanics', '303 Mechanics Ln', '555-678-9012', '555-678-9013'),
(7, 'Precision Parts', '404 Precision Dr', '555-789-0123', '555-789-0124'),
(8, 'Tech Distributors', '505 Tech Park', '555-890-1234', '555-890-1235'),
(9, 'Global Tech', '606 Global Ave', '555-901-2345', '555-901-2346'),
(10, 'Automation World', '707 Automation Rd', '555-012-3456', '555-012-3457');

-- Business_Location
INSERT INTO Business_Location (Location_ID, Location_name, Location_address, Tel_No, Fax_No, Owner_name, Owner_tel_No, Manager_name, Manager_tel_No, Comments) VALUES
(1, 'Central HQ', '123 Main St', '555-100-2000', '555-100-2001', 'Alice Smith', '555-100-2002', 'Bob Johnson', '555-100-2003', 'Headquarters'),
(2, 'North Branch', '456 North St', '555-200-3000', '555-200-3001', 'Charlie Brown', '555-200-3002', 'Dana White', '555-200-3003', 'Northern office'),
(3, 'South Branch', '789 South St', '555-300-4000', '555-300-4001', 'Eve Black', '555-300-4002', 'Frank Green', '555-300-4003', 'Southern office'),
(4, 'East Branch', '101 East St', '555-400-5000', '555-400-5001', 'Grace Blue', '555-400-5002', 'Harry Red', '555-400-5003', 'Eastern office'),
(5, 'West Branch', '202 West St', '555-500-6000', '555-500-6001', 'Ivy White', '555-500-6002', 'Jack Orange', '555-500-6003', 'Western office'),
(6, 'Midtown Office', '303 Midtown St', '555-600-7000', '555-600-7001', 'Karen Yellow', '555-600-7002', 'Leo Brown', '555-600-7003', 'Midtown office'),
(7, 'Suburban Office', '404 Suburban St', '555-700-8000', '555-700-8001', 'Mona Gray', '555-700-8002', 'Nina Pink', '555-700-8003', 'Suburban office'),
(8, 'Downtown Office', '505 Downtown St', '555-800-9000', '555-800-9001', 'Oscar Silver', '555-800-9002', 'Pam Gold', '555-800-9003', 'Downtown office'),
(9, 'Uptown Office', '606 Uptown St', '555-900-1000', '555-900-1001', 'Quinn Copper', '555-900-1002', 'Rick Bronze', '555-900-1003', 'Uptown office'),
(10, 'Rural Office', '707 Rural St', '555-000-1100', '555-000-1101', 'Steve Steel', '555-000-1102', 'Tina Iron', '555-000-1103', 'Rural office');

-- Product
INSERT INTO Product (Product_ID, Product_name, Unit_price, Manufacturer) VALUES
(1, 'Widget A', 15.99, 'WidgetCorp'),
(2, 'Gadget B', 23.49, 'Gadgetron'),
(3, 'Thingamajig C', 9.99, 'ThingsCo'),
(4, 'Doodad D', 14.49, 'Doodad Inc'),
(5, 'Device E', 19.89, 'DeviceWorks'),
(6, 'Apparatus F', 29.99, 'Apparatus Ltd'),
(7, 'Contraption G', 34.99, 'Contraptioneers'),
(8, 'Machine H', 49.99, 'MachineMakers'),
(9, 'Tool I', 12.49, 'ToolTown'),
(10, 'Implement J', 27.99, 'Implement Industries');

-- Machine
INSERT INTO Machine (Machine_ID, Location_ID, Product_ID, Machine_condition, Pur_date, Manufacturer, Cost) VALUES
(1, 1, 1, 'New', '2023-01-01', 'WidgetCorp', 1500.00),
(2, 2, 2, 'Used', '2023-02-01', 'Gadgetron', 1200.00),
(3, 3, 3, 'Refurbished', '2023-03-01', 'ThingsCo', 800.00),
(4, 4, 4, 'New', '2023-04-01', 'Doodad Inc', 1300.00),
(5, 5, 5, 'Used', '2023-05-01', 'DeviceWorks', 900.00),
(6, 6, 6, 'Refurbished', '2023-06-01', 'Apparatus Ltd', 1000.00),
(7, 7, 7, 'New', '2023-07-01', 'Contraptioneers', 1700.00),
(8, 8, 8, 'Used', '2023-08-01', 'MachineMakers', 1100.00),
(9, 9, 9, 'Refurbished', '2023-09-01', 'ToolTown', 600.00),
(10, 10, 10, 'New', '2023-10-01', 'Implement Industries', 1600.00);

-- Purchase_Request
INSERT INTO Purchase_Request (Request_ID, Location_ID, Date, Comments) VALUES
(1, 1, '2021-02-15', 'Urgent replacement needed for broken machine.'),
(2, 2, '2021-05-20', 'Scheduled maintenance parts request.'),
(3, 3, '2021-08-10', 'New machine request for increased production.'),
(4, 4, '2021-11-05', 'Replacement parts for old machinery.'),
(5, 5, '2022-01-22', 'Request for additional safety equipment.'),
(6, 6, '2022-04-14', 'Urgent repair kit needed.'),
(7, 7, '2022-07-19', 'New product trial equipment request.'),
(8, 8, '2022-10-25', 'Expansion project equipment request.'),
(9, 9, '2023-01-30', 'Replacement of obsolete machinery.'),
(10, 10, '2023-04-13', 'Regular maintenance supplies request.'),
(11, 1, '2023-07-05', 'Emergency parts order for breakdown.'),
(12, 2, '2023-09-18', 'Year-end upgrade for critical machines.'),
(13, 3, '2023-12-09', 'New equipment for safety compliance.'),
(14, 4, '2024-02-15', 'Spare parts for high-usage machines.'),
(15, 5, '2024-03-07', 'Request for testing new machinery models.'),
(16, 6, '2024-04-20', 'Order for replacement motors.'),
(17, 7, '2024-05-11', 'Upgrade for outdated equipment.'),
(18, 8, '2024-06-01', 'Parts for routine inspection and maintenance.'),
(19, 9, '2024-06-07', 'Replacement of worn-out tools.'),
(20, 10, '2024-06-14', 'Order for additional production line machines.');

-- Purchase_Request_Product_Quantity
INSERT INTO Purchase_Request_Product_Quantity (Request_ID, Product_ID, Quantity) VALUES
(1, 1, 10),
(2, 2, 20),
(3, 3, 15),
(4, 4, 25),
(5, 5, 30),
(6, 6, 5),
(7, 7, 12),
(8, 8, 18),
(9, 9, 22),
(10, 10, 17),
(11, 2, 14),
(12, 3, 16),
(13, 4, 19),
(14, 5, 8),
(15, 6, 20),
(16, 7, 24),
(17, 8, 11),
(18, 9, 13),
(19, 10, 21),
(20, 1, 9);

-- Purchase_Order
INSERT INTO Purchase_Order (Pur_order_ID, Vendor_ID, Date) VALUES
(210110001, 3, '2021-01-10'),
(210717001, 2, '2021-07-17'),
(211220001, 10, '2021-12-20'),
(220125001, 4, '2022-01-25'),
(220219001, 1, '2022-02-19'),
(220505001, 9, '2022-05-05'),
(220911001, 7, '2022-09-11'),
(230209001, 2, '2023-02-09'),
(230320001, 8, '2023-03-20'),
(230321001, 4, '2023-03-21'),
(230410001, 9, '2023-04-10'),
(230425001, 4, '2023-04-25'),
(230622001, 6, '2023-06-22'),
(230825001, 1, '2023-08-25'),
(231130001, 9, '2023-11-30'),
(240104001, 5, '2024-01-04'),
(240210001, 7, '2024-02-10'),
(240312001, 3, '2024-03-12'),
(240413001, 2, '2024-04-13'),
(240516001, 1, '2024-05-06');

-- Purchase_Order_Product_Quantity (continuation)
INSERT INTO Purchase_Order_Product_Quantity (Pur_order_ID, Product_ID, Quantity) VALUES
(210110001, 1, 50),
(210717001, 3, 12),
(211220001, 7, 75),
(220125001, 5, 60),
(220219001, 2, 95),
(220505001, 6, 28),
(220911001, 7, 10),
(230209001, 8, 5),
(230320001, 9, 7),
(230321001, 10, 9),
(230410001, 1, 5),
(230425001, 6, 9),
(230622001, 8, 10),
(230825001, 4, 15),
(231130001, 2, 60),
(240104001, 3, 90),
(240210001, 4, 12),
(240312001, 8, 10),
(240413001, 7, 8),
(240516001, 9, 7);

-- Invoice
INSERT INTO Invoice (Invoice_ID, Pur_order_ID, Vendor_ID, Machine_ID, Invoice_date, Ship_date, Ship_address, Terms, Shipping_charge, Sales_tax, Credit_due) VALUES
(1, 210110001, 3, 1, '2023-01-11', '2023-01-12', '123 Main St', 'Net 30', 50.00, 5.00, '2023-02-11'),
(2, 210717001, 2, 2, '2023-01-16', '2023-01-17', '456 North St', 'Net 30', 60.00, 6.00, '2023-02-16'),
(3, 211220001, 10, 3, '2023-01-21', '2023-01-22', '789 South St', 'Net 30', 70.00, 7.00, '2023-02-21'),
(4, 220125001, 4, 4, '2023-01-26', '2023-01-27', '101 East St', 'Net 30', 80.00, 8.00, '2023-02-26'),
(5, 220219001, 1, 5, '2023-01-31', '2023-02-01', '202 West St', 'Net 30', 90.00, 9.00, '2023-03-01'),
(6, 220505001, 9, 6, '2023-02-06', '2023-02-07', '303 Midtown St', 'Net 30', 100.00, 10.00, '2023-03-06'),
(7, 220911001, 7, 7, '2023-02-11', '2023-02-12', '404 Suburban St', 'Net 30', 110.00, 11.00, '2023-03-11'),
(8, 230209001, 2, 8, '2023-02-16', '2023-02-17', '505 Downtown St', 'Net 30', 120.00, 12.00, '2023-03-16'),
(9, 230320001, 8, 9, '2023-02-21', '2023-02-22', '606 Uptown St', 'Net 30', 130.00, 13.00, '2023-03-21'),
(10, 230321001, 4, 10, '2023-02-26', '2023-02-27', '707 Rural St', 'Net 30', 140.00, 14.00, '2023-03-26');

-- Product_Invoice_Quantity
INSERT INTO Product_Invoice_Quantity (Invoice_ID, Product_ID, Quantity) VALUES
(1, 1, 50),
(2, 2, 100),
(3, 3, 75),
(4, 4, 60),
(5, 5, 90),
(6, 6, 120),
(7, 7, 110),
(8, 8, 85),
(9, 9, 70),
(10, 10, 95);

-- Technician
INSERT INTO Technician (Technician_ID, Technician_name) VALUES
(1, 'David Doe'),
(2, 'Jane Smith'),
(3, 'Kate Brown'),
(4, 'Bill Taylor'),
(5, 'Ann White'),
(6, 'Liam Green'),
(7, 'Perry Black'),
(8, 'Janet Grey'),
(9, 'Rachel Blue'),
(10, 'Michael Pink');

-- Order
INSERT INTO `Order` (Order_ID, Location_ID, Technician_ID, Machine_ID, Move_type, Move_date) VALUES
('210115001', 5, 3, 5, 'Install', '2021-01-15'),
('210321001', 7, 3, 4, 'Remove', '2021-03-22'),
('210627001', 1, 3, 9, 'Install', '2021-07-28'),
('210627002', 3, 7, 2, 'Remove', '2021-09-05'),
('211009001', 9, 5, 3, 'Install', '2021-12-19'),
('220118001', 4, 1, 8, 'Remove', '2022-02-20'),
('220225001', 6, 10, 2, 'Install', '2022-03-14'),
('220619001', 2, 4, 7, 'Remove', '2022-07-07'),
('220628001', 8, 6, 6, 'Install', '2022-07-23'),
('220827001', 10, 9, 5, 'Remove', '2022-09-10'),
('220828001', 3, 1, 1, 'Install', '2022-09-18'),
('220910001', 7, 3, 9, 'Remove', '2022-09-20'),
('221028001', 4, 10, 4, 'Install', '2022-11-28'),
('221208001', 2, 8, 7, 'Remove', '2022-12-15'),
('230226001', 6, 8, 2, 'Install', '2023-02-27'),
('230308001', 1, 8, 3, 'Remove', '2023-05-19'),
('230324001', 9, 2, 8, 'Install', '2023-08-25'),
('240121001', 5, 4, 6, 'Remove', '2024-02-14'),
('240423001', 10, 9, 1, 'Install', '2024-05-01'),
('240614001', 8, 6, 10, 'Remove', '2024-08-20');

-- Contract
INSERT INTO Contract (Contract_ID, Location_ID, Contract_start_date, Contract_end_date) VALUES
(1, 1, '2021-01-01', '2023-12-31'),
(2, 2, '2021-01-05', '2022-07-31'),
(3, 3, '2022-01-01', '2023-12-31'),
(4, 4, '2022-01-01', '2024-06-30'),
(5, 5, '2022-07-10', '2023-12-31'),
(6, 6, '2022-10-15', '2022-12-31'),
(7, 7, '2023-01-01', '2023-12-31'),
(8, 8, '2023-03-01', '2023-10-31'),
(9, 9, '2024-01-01', '2024-12-31'),
(10, 10, '2024-06-01', '2024-12-31');

-- Contract_Machine
INSERT INTO Contract_Machine (Contract_ID, Machine_ID) VALUES
(1, 1),
(2, 4),
(3, 8),
(4, 2),
(5, 9),
(6, 10),
(7, 7),
(8, 10),
(9, 8),
(10, 10);