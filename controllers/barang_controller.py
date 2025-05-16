from flask import Blueprint, render_template, request, redirect, session
from config.db import get_connection as get_db_connection
barang_bp = Blueprint('barang_bp', __name__)

@barang_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    conn = get_db_connection()  # ← harus panggil function di sini
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT barang.id_barang, barang.nama_barang, barang.jumlah, supplier.nama_supplier, lokasi.nama_lokasi
        FROM barang
        LEFT JOIN supplier ON barang.supplier_id = supplier.id_supplier
        LEFT JOIN lokasi ON barang.lokasi_id = lokasi.id_lokasi
    """
    cursor.execute(query)
    barang_list = cursor.fetchall()
    return render_template('dashboard.html', barang_list=barang_list)

# Tambah, Edit, Hapus barang route disini...
