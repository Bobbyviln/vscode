import sqlite3

# Connect to the database
db_name = 'sample.db'
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create a sample table
table_name = 'sample_table'
cursor.execute(f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL
)
''')

# Insert sample data into the table
sample_data = [
    (1, 'Alice', 25),
    (2, 'Bob', 30),
    (3, 'Charlie', 35)
]
cursor.executemany(f'INSERT INTO {table_name} (id, name, age) VALUES (?, ?, ?)', sample_data)
conn.commit()

print(f"Sample SQL table created: {table_name}")

# Close the connection
conn.close()
