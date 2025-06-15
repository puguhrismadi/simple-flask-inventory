from flask import Blueprint, render_template, request, redirect, session
from config.db import get_connection as get_db_connection
import hashlib

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def index():
    return "Hello, World!"

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()
        conn = get_db_connection()  # ← harus panggil function di sini
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            session['id_user'] = user['id_user']
            return redirect('/dashboard')
        else:
            return 'Login gagal!'
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
