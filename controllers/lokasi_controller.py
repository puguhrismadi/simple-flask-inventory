from flask import Blueprint, render_template, request, redirect, session
from config.db import get_connection as get_db_connection

lokasi_bp = Blueprint('lokasi_bp', __name__)

@lokasi_bp.route('/lokasi')
def tampil_lokasi():
    if 'username' not in session:
        return redirect('/login')
    conn=get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lokasi")
    data_lokasi = cursor.fetchall()
    return render_template('lokasi/tampil_lokasi.html', lokasi_list=data_lokasi)
