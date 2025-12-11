CREATE TABLE IF NOT EXIST employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    department VARCHAR(50) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL
    hire_date DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO employees (name, position, department, salary) VALUES
('Alice Johnson', 'Software Engineer', 'IT', 75000),
('Bob Smith', 'Project Manager', 'IT', 85000),
('Charlie Brown', 'HR Specialist', 'Human Resources', 60000);
