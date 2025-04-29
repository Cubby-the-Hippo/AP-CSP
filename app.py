from flask import Flask
from views import login, register, dashboard, visualize
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY  # Secret key for session management

# Register routes from views.py
app.add_url_rule('/login', 'login', login, methods=['GET', 'POST'])
app.add_url_rule('/register', 'register', register, methods=['GET', 'POST'])
app.add_url_rule('/dashboard', 'dashboard', dashboard)
app.add_url_rule('/visualize', 'visualize', visualize)

if __name__ == "__main__":
    app.run(debug=True)
