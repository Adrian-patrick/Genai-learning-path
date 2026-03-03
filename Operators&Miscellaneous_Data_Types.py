"""
SQL operators
"""

"""
comparison operators
=   !=   <>   >   <   >=   <=
"""
SELECT * FROM users
WHERE id = 1;

"""
logical operators
AND
OR
NOT
"""
SELECT * FROM users
WHERE is_active = 1 AND created_at > '2024-01-01';

"""
BETWEEN
range filtering
"""
SELECT * FROM orders
WHERE amount BETWEEN 100 AND 500;

"""
IN
multi value filtering
"""
SELECT * FROM users
WHERE role IN ('admin', 'moderator');

"""
LIKE
pattern matching
"""
SELECT * FROM users
WHERE email LIKE '%@gmail.com';

"""
IS NULL
don't compare using =
"""
WHERE deleted_at IS NULL;

"""
Aggreegate operators
COUNT()
SUM()
AVG()
MIN()
MAX()
works on a singular attribute and returns single value
"""
SELECT COUNT(*) FROM users;

"""
miscellaneous data types
"""

"""
ENUM
efficient 
similar to dictionary, values have indexes
"""
status ENUM('pending', 'approved', 'rejected')

"""
JSON
specific code to handle 
"""
#Extract a value using shorthand
SELECT profile->"$.name" AS name FROM users; 
#Output: "Alice" (includes quotes)

"""
decimal vs float
float causes precision errors
decimal is more accurate
"""
DECIMAL(10,2)