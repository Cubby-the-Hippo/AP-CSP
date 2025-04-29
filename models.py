import sqlite3
from hashlib import sha256

# Function to hash passwords before storing
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Register a new user
def register_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists.")
    conn.close()

# Login user
def login_user(username, password):
    hashed_password = hash_password(password)
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None  # Return user_id if found

# Get the habits for a user
def get_habits(user_id):
    conn = sqlite3.connect('habit_tracker.db')
    c = conn.cursor()
    c.execute("SELECT * FROM habits WHERE user_id = ?", (user_id,))
    habits = c.fetchall()
    conn.close()
    return habits
