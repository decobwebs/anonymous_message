from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import hashlib
import os
import uuid
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Use PostgreSQL connection string from Render
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    unique_link = db.Column(db.String(100), unique=True, nullable=False)

# Message Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=True)
    message_content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('messages', lazy=True))

# Initialize Database
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Generate unique link
        unique_link = str(uuid.uuid4())

        user = User(email=email, name=name, password_hash=password_hash, unique_link=unique_link)
        db.session.add(user)
        db.session.commit()

        flash('Signup successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and hashlib.sha256(password.encode()).hexdigest() == user.password_hash:
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['unique_link'] = user.unique_link
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))

        flash('Invalid login credentials.', 'danger')

    return render_template('login.html')

# Dashboard Route (for users to get the unique link)
# Dashboard Route (for users to see their unique link and messages)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    # Query messages for the logged-in user
    messages = Message.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', unique_link=user.unique_link, messages=messages)


# Anonymous Message Route
@app.route('/message/<string:unique_link>', methods=['GET', 'POST'])
def message(unique_link):
    user = User.query.filter_by(unique_link=unique_link).first()

    if not user:
        return 'User not found', 404

    if request.method == 'POST':
        message_content = request.form['message']
        message = Message(message_content=message_content, user_id=user.id, sender=None)
        db.session.add(message)
        db.session.commit()

        flash('Message sent anonymously.', 'success')

    return render_template('message.html', user=user)


# Admin Dashboard Route
# Admin Dashboard Route
@app.route('/admin')
def admin_dashboard():
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    # Query all messages from the database
    messages = Message.query.all()
    return render_template('admin_dashboard.html', messages=messages)


# Admin Login Route
# Admin Login Route
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'admin_password':  # Replace with secure method for production
            session['admin'] = True
            flash('Admin login successful.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin password.', 'danger')

    return render_template('admin_login.html')


# Delete Message Route (for Admin)
@app.route('/admin/delete/<int:id>', methods=['POST'])
def delete_message(id):
    if 'admin' not in session:
        return redirect(url_for('admin_login'))

    message = Message.query.get(id)
    if message:
        db.session.delete(message)
        db.session.commit()
        flash('Message deleted.', 'success')

    return redirect(url_for('admin_dashboard'))

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('unique_link', None)
    session.pop('admin', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
