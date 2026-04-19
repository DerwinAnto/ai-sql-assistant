import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    grade TEXT
)
""")

cursor.execute("INSERT INTO students (name, age, grade) VALUES ('John', 15, '10')")
cursor.execute("INSERT INTO students (name, age, grade) VALUES ('Alice', 14, '9')")
cursor.execute("""
INSERT OR IGNORE INTO students (id, name, age, grade) VALUES
(1, 'John', 15, '10'),
(2, 'Alice', 14, '9')
""")
# cursor.execute("DROP TABLE IF EXISTS students")
conn.commit()
conn.close()

print("Database created!")