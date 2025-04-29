from flask import render_template, request, redirect, url_for, session
from models import login_user, register_user, get_habits
import sqlite3
import pandas as pd
import plotly.express as px

# Connect to database
def get_db_connection():
    conn = sqlite3.connect('habit_tracker.db')
    conn.row_factory = sqlite3.Row  # Allows dict-like access to rows
    return conn

# Route for login
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = login_user(username, password)
        if user_id:
            session['user_id'] = user_id
            return redirect(url_for('dashboard'))
        else:
            return "Login failed. Please try again."
    return render_template('login.html')

# Route for registration
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        register_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

# Route for dashboard
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    habits = get_habits(user_id)
    return render_template('dashboard.html', habits=habits)

# Route for habit visualization
def visualize():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT hc.date, h.habit_name, hc.completed
        FROM habit_completions hc
        JOIN habits h ON hc.habit_id = h.habit_id
        WHERE hc.user_id = ?
    """, (user_id,))
    habit_data = c.fetchall()
    conn.close()

    # Visualize habit completion trends
    df = pd.DataFrame(habit_data, columns=['Date', 'Habit', 'Completed'])
    fig = px.line(df, x='Date', y='Completed', color='Habit', title="Habit Completion Trends")
    fig.write_html("templates/habit_visualization.html")

    return render_template("habit_visualization.html")
