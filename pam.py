from flask import Flask, session,render_template, redirect, url_for, request
import re
import datetime
import logging
import sys

from couchdb import Server

app = Flask(__name__,static_url_path='/static', static_folder='static')
app.secret_key = 'your-secret-key'

# Connect to CouchDB
couch = Server('http://admin:admin@localhost:5984')
db = couch['users']

# Define a dictionary to store the failed login attempts for each user
failed_attempts = {}

# Constants for the maximum number of allowed failed attempts and the block duration
MAX_FAILED_ATTEMPTS = 3
BLOCK_DURATION_MINUTES = 5

@app.route('/', methods=['GET', 'POST'])
def index():
#    return render_template('index.html')
    return redirect('/login')

# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print(request.remote_addr)
    if(check_localhost(request)==False):
        error = 'Only localhost permitted.'
        return render_template('login.html', error=error)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        current_time = datetime.datetime.now().time()
        if not is_within_allowed_time_range(current_time):
            error = 'Access denied. Login allowed only between 17:00 and 19:00.'
            increment_failed_attempts(username)
            if is_user_blocked(username):
                error = 'Access blocked. Please try again later.1'
                return render_template('login.html', error=error)
            return render_template('login.html', error=error)
        allowed_users = read_allowed_users()
        if username not in allowed_users:
            error = 'Unauthorized user'
            increment_failed_attempts(username)
            if is_user_blocked(username):
                error = 'Access blocked. Please try again later.2'
                return render_template('login.html', error=error)
            return render_template('login.html', error=error)
        result = check_password(password)
        if result == 'Password meets the quality requirements.':
            user = User.get(username)
            if user and user.password == password:
                session['username'] = user.username
                reset_failed_attempts(username)
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid username or password'
                increment_failed_attempts(username)
                if is_user_blocked(username):
                    error = 'Access blocked. Please try again later.2'
                return render_template('login.html', error=error)
        else:
            error = result
       
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if(check_localhost(request)==False):
        error = 'Only localhost permitted.'
        return render_template('register.html', error=error)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = check_password(password)

        if result == 'Password meets the quality requirements.':
            # Check if the username is already taken
            if User.get_or_none(username=username):
                error = 'Username already taken'
                return render_template('register.html', error=error)

            # Create a new user document
            user = User(username=username, password=password)
            user.store()

            session['username'] = user.username
            return redirect(url_for('dashboard'))
        else:
            error = result
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

def check_password(password):
    if len(password) < 8:
        return 'Password must be at least 8 characters long.'

    if not re.search(r"\d", password):
        return 'Password must contain at least one number.'

    if not re.search(r"[A-Z]", password):
        return 'Password must contain at least one capital letter.'

    if re.search(r"\W", password):
        return 'Password cannot contain special characters.'

    return 'Password meets the quality requirements.'

@app.route('/dashboard')
def dashboard():
    if(check_localhost(request)==False):
        error = 'Only localhost permitted.'
        return render_template('login.html', error=error)
    if 'username' in session:
        current_time = datetime.datetime.now().time()
        if not is_within_allowed_time_range(current_time):
            session.pop('username', None)
            return redirect(url_for('login'))

        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def get(username):
        doc = db.get(username)
        if doc:
            return User(doc['username'], doc['password'])
        return None

    @staticmethod
    def get_or_none(username):
        try:
            return User.get(username)
        except db.ResourceNotFound:
            return None
    def store(self):
        doc = {'_id': self.username, 'username': self.username, 'password': self.password}
        db.save(doc)

    def save(self):
        doc = {'_id': self.username, 'username': self.username, 'password': self.password}
        db.save(doc)

def read_allowed_users():
    allowed_users = []
    with open('allowed_users.txt', 'r') as file:
        for line in file:
            allowed_users.append(line.strip())
    return allowed_users

def is_within_allowed_time_range(current_time):
    start_time = datetime.time(9, 0)  # 17:00
    end_time = datetime.time(17, 26)    # 19:00

    if start_time <= current_time <= end_time:
        return True
    return False

def check_localhost(request):
    user_ip = request.remote_addr
    if user_ip == '127.0.0.1' or user_ip == 'localhost':
        return True
    else:
        return False

def is_user_blocked(username):
    # Check if the user is currently blocked by comparing the current time with the block end time
    if username in failed_attempts:
        attempts, last_attempt_time = failed_attempts[username]
        if(attempts>=MAX_FAILED_ATTEMPTS):
            block_end_time = last_attempt_time + datetime.timedelta(minutes=BLOCK_DURATION_MINUTES)
            current_time = datetime.datetime.now()
            if current_time < block_end_time:
                return True
            else:
                # Remove the user from the failed attempts dictionary if the block period has ended
                failed_attempts.pop(username)
    return False

def increment_failed_attempts(username):
    # Increment the failed attempt count for the user and store the current time
    if username not in failed_attempts:
        failed_attempts[username] = (1, datetime.datetime.now())
    else:
        attempts, last_attempt_time = failed_attempts[username]
        failed_attempts[username] = (attempts + 1, datetime.datetime.now())

def reset_failed_attempts(username):
    # Reset the failed attempt count for the user
    if username in failed_attempts:
        failed_attempts.pop(username)