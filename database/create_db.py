import sqlite3

conn = sqlite3.connect('habit_tracker.db')
c = conn.cursor()

# Create users table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Create habits table
c.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        habit_name TEXT NOT NULL,
        completed BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )
''')

# Create habit completions table
c.execute('''
    CREATE TABLE IF NOT EXISTS habit_completions (
        completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        date TEXT,
        completed BOOLEAN,
        FOREIGN KEY (habit_id) REFERENCES habits(habit_id)
    )
''')

conn.commit()
conn.close()

print("Database created successfully!")
