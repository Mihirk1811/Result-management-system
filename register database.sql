USE register;

CREATE TABLE employee (
    id INT AUTO_INCREMENT PRIMARY KEY,
    f_name VARCHAR(50),
    l_name VARCHAR(50),
    contact VARCHAR(15),
    email VARCHAR(100) UNIQUE,
    question VARCHAR(200),
    answer VARCHAR(200),
    password VARCHAR(100)
);