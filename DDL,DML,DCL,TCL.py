"""
Data Definition Language
CREATE : creating tables
ALTER : modifying tables
DROP : deleting structure and data entirely
TRUNCATE : removes removes data 
"""
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

ALTER TABLE users ADD email VARCHAR(150);

DROP TABLE users;

TRUNCATE TABLE users;

"""
Data Manipulation Language
SELECT : used to retreive data
INSERT : add one or more rows
UPDATE : used to modify existing rows
DELETE : used to remove rows
"""
SELECT * FROM Employees;

INSERT INTO Employees (Name, Role) VALUES ('John Doe', 'Manager');

UPDATE Employees SET Role = 'Senior Manager' WHERE Name = 'John Doe';

DELETE FROM Employees WHERE Name = 'John Doe';

"""
Data Control Language
GRANT : granting access
REVOKE : revoking access
"""
GRANT SELECT ON genai_training.* TO 'app_user';

"""
Transaction control language
START TRANSACTION
COMMIT
ROLLBACK
example
"""
START TRANSACTION;

INSERT INTO orders ...
UPDATE accounts ...
UPDATE inventory ...

COMMIT;
#if error
ROLLBACK;
