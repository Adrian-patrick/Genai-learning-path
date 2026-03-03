"""
DDL practice
"""
CREATE DATABASE sql_practice;

USE sql_practice;

#users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#documents table
CREATE TABLE documents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
);

#inserting users
INSERT INTO users (name, email)
VALUES ('Adrian', 'adrian@example.com');

#inserting documents
INSERT INTO documents (user_id, title, content)
VALUES (1, 'GenAI Basics', 'Introduction content...');

#getting all active users
SELECT id, name, email
FROM users
WHERE is_active = TRUE;

#user 1 row sorted most recent
SELECT id, title, created_at
FROM documents
WHERE user_id = 1
ORDER BY created_at DESC;

#user and documents
SELECT u.name, d.title
FROM users u
INNER JOIN documents d
ON u.id = d.user_id
WHERE u.id = 1;

#getting all user even ones without documents
SELECT u.name, d.title
FROM users u
LEFT JOIN documents d
ON u.id = d.user_id;

#count documents pre user
SELECT u.name, COUNT(d.id) AS document_count
FROM users u
LEFT JOIN documents d
ON u.id = d.user_id
GROUP BY u.id;

#updating users
UPDATE users
SET is_active = FALSE
WHERE id = 2;

#deleting document
DELETE FROM documents
WHERE id = 3;

#basic search
SELECT *
FROM documents
WHERE title LIKE '%GenAI%';

