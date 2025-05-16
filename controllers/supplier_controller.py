from flask import Blueprint, render_template, request, redirect, session
from config.db import get_connection as get_db_connection

supplier_bp = Blueprint('supplier_bp', __name__)

@supplier_bp.route('/suplier')
def tampil_suplier():
    if 'username' not in session:
        return redirect('/login')
    conn = get_db_connection()  # ← harus panggil function di sini
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM supplier")
    data_suplier = cursor.fetchall()
    return render_template('suplier/tampil_suplier.html', suplier_list=data_suplier)
