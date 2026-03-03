"""
Database : container of data
one app - one database
"""

"""
Table - represents an entity
Row - one instance of an entity
Column - attribute of an entity
Schema - logical structure of database
"""

"""
Keys
primary key : unique identifier usually 'id'
foreign key : links table 
unique key : ensure no duplicates
composite key : multiple columns as primary key
"""

"""
ER model
Entity-Relationship thinking
Types :
one-to-one
one-to-many
many-to-many
"""

"""
data types
INT - ids,counters
BIGINT - large ids
DECIMAL - money
FLOAT - approx
VARCHAR - limited length
TEXT - long text
BOOLEAN/TINYINT(1) - binary
DATE/DATETIME/TIMESTAMP - logs
""" 

"""
Embedding example
embeddings
    id
    chunk_id (FK → chunks.id)
    vector
    model_name
    created_at
"""