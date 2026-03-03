"""
ORDER BY
used to sort results
"""
SELECT * FROM users
ORDER BY created_at DESC;

"""
ASC vs DESC
"""
ORDER BY id ASC;   #-- default
ORDER BY id DESC;  #-- most recent first

"""
multiple column sorting
"""
ORDER BY role ASC, created_at DESC;

"""
performance awareness
frequently sorted columns must be indexed
"""

"""
JOINs
"""

"""
INNER JOIN
join on foreign key and primary key(ids) of both the table
"""
SELECT users.name, documents.title
FROM users
INNER JOIN documents
ON users.id = documents.user_id;

"""
LEFT JOIN
left table completely only the matched ones in the right table
"""
SELECT users.name, documents.title
FROM users
LEFT JOIN documents
ON users.id = documents.user_id;

"""
RIGHT JOIN
right table completely only the matched one in the left table
"""
SELECT users.name, documents.title
FROM users
RIGHT JOIN documents
ON users.id = documents.user_id;
