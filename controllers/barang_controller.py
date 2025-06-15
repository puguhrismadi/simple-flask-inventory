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
@barang_bp.route('/tambah')
def tambah():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM supplier")
    supplier_list = cursor.fetchall()
    cursor.execute("SELECT * FROM lokasi")
    lokasi_list = cursor.fetchall()
    cursor.close()

    return render_template('barang/tambah_barang.html', supplier_list=supplier_list,lokasi_list=lokasi_list)

@barang_bp.route('/tambah_barang',methods=['GET', 'POST'])
def tambah_barang():
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nama_barang = request.form['nama_barang']
        stok = request.form['stok']
        id_supplier = request.form['id_supplier']
        id_lokasi = request.form['id_lokasi']
        cursor.execute("INSERT INTO barang (nama_barang, jumlah, supplier_id, lokasi_id) VALUES (%s, %s, %s, %s)", (nama_barang, stok, id_supplier, id_lokasi))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        cursor.execute("SELECT * FROM supplier")
        supplier_list = cursor.fetchall()
        cursor.close()
        return render_template('barang/tambah_barang.html', supplier_list=supplier_list)
@barang_bp.route('/barang/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nama_barang = request.form['nama_barang']
        stok = request.form['stok']
        id_supplier = request.form['id_supplier']
        id_lokasi = request.form['id_lokasi']
        cursor.execute("UPDATE barang SET nama_barang=%s, jumlah=%s, supplier_id=%s, lokasi_id=%s WHERE id_barang=%s", (nama_barang, stok, id_supplier, id_lokasi, id))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (id,))
        barang = cursor.fetchone()
        cursor.execute("SELECT * FROM supplier")
        supplier_list = cursor.fetchall()
        cursor.close()
        print(supplier_list)
        return render_template('barang/edit_barang.html', barang=barang, supplier_list=supplier_list)
@barang_bp.route('/barang/hapus/<int:id>', methods=['GET'])
def hapus(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM barang WHERE id_barang=%s", (id,))
    db.commit()
    cursor.close()
    return redirect('/dashboard')
