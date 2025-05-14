from flask import Flask, render_template, request, redirect, session
from config.db import db
import hashlib
app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return "Hello, World!"
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hash password MD5
        hashed_password = hashlib.md5(password.encode('utf-8')).hexdigest()

        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_password))
        user = cursor.fetchone()

        if user:
            # Simpan session username dan id_user
            session['username'] = user['username']
            session['id_user'] = user['id_user']  # kalau ada id_user di tabel
            return redirect('/dashboard')
        else:
            return 'Login gagal, cek username atau password!'
    return render_template('login.html')
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            barang.id_barang, 
            barang.nama_barang, 
            barang.jumlah, 
            supplier.nama_supplier, 
            lokasi.nama_lokasi
        FROM barang
        LEFT JOIN supplier ON barang.supplier_id = supplier.id_supplier
        LEFT JOIN lokasi ON barang.lokasi_id = lokasi.id_lokasi
    """
    cursor.execute(query)
    barang_list = cursor.fetchall()
    #print(data_dashboard)
    return render_template('dashboard.html', barang_list=barang_list)
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')
@app.route('/tambah')
def tambah():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM supplier")
    supplier_list = cursor.fetchall()
    cursor.execute("SELECT * FROM lokasi")
    lokasi_list = cursor.fetchall()
    cursor.close()

    return render_template('barang/tambah_barang.html', supplier_list=supplier_list,lokasi_list=lokasi_list)

@app.route('/tambah_barang')
def tambah_barang():
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nama_barang = request.form['nama_barang']
        stok = request.form['stok']
        id_supplier = request.form['id_supplier']
        cursor.execute("INSERT INTO barang (nama_barang, stok, id_supplier) VALUES (%s, %s, %s)", (nama_barang, stok, id_supplier))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        cursor.execute("SELECT * FROM supplier")
        supplier_list = cursor.fetchall()
        cursor.close()
        return render_template('barang/tambah_barang.html', supplier_list=supplier_list)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cursor = db.cursor(dictionary=True)
    if request.method == 'POST':
        nama_barang = request.form['nama_barang']
        stok = request.form['stok']
        id_supplier = request.form['id_supplier']
        cursor.execute("UPDATE barang SET nama_barang=%s, stok=%s, id_supplier=%s WHERE id_barang=%s", (nama_barang, stok, id_supplier, id))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        cursor.execute("SELECT * FROM barang WHERE id_barang=%s", (id,))
        barang = cursor.fetchone()
        cursor.execute("SELECT * FROM supplier")
        supplier_list = cursor.fetchall()
        cursor.close()
        return render_template('barang/edit_barang.html', barang=barang, supplier_list=supplier_list)
@app.route('/hapus/<int:id>', methods=['POST'])
def hapus(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM barang WHERE id_barang=%s", (id,))
    db.commit()
    cursor.close()
    return redirect('/dashboard')

@app.route('/tambah_supplier', methods=['GET', 'POST'])
def tambah_supplier():
    if request.method == 'POST':
        nama_supplier = request.form['nama_supplier']
        alamat = request.form['alamat']
        cursor = db.cursor()
        cursor.execute("INSERT INTO supplier (nama_supplier, alamat) VALUES (%s, %s)", (nama_supplier, alamat))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        return render_template('supplier/tambah_supplier.html')
@app.route('/edit_supplier/<int:id>', methods=['GET', 'POST'])
def edit_supplier(id):
    if request.method == 'POST':
        nama_supplier = request.form['nama_supplier']
        alamat = request.form['alamat']
        cursor = db.cursor()
        cursor.execute("UPDATE supplier SET nama_supplier=%s, alamat=%s WHERE id_supplier=%s", (nama_supplier, alamat, id))
        db.commit()
        cursor.close()
        return redirect('/dashboard')
    else:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM supplier WHERE id_supplier=%s", (id,))
        supplier = cursor.fetchone()
        cursor.close()
        return render_template('supplier/edit_supplier.html', supplier=supplier)
    
@app.route('/hapus_supplier/<int:id>', methods=['POST'])
def hapus_supplier(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM supplier WHERE id_supplier=%s", (id,))
    db.commit()
    cursor.close()
    return redirect('/dashboard')

# Tampil Barang
@app.route('/barang')
def tampil_barang():
    if 'username' not in session:
        return redirect('/login')

    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT barang.id_barang, barang.nama_barang, barang.stok, suplier.nama_suplier 
        FROM barang 
        LEFT JOIN suplier ON barang.id_suplier = suplier.id_suplier
    """)
    data_barang = cursor.fetchall()
    return render_template('barang/tampil_barang.html', barang_list=data_barang)


# Tampil Suplier
@app.route('/suplier')
def tampil_suplier():
    if 'username' not in session:
        return redirect('/login')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM suplier")
    data_suplier = cursor.fetchall()
    return render_template('suplier/tampil_suplier.html', suplier_list=data_suplier)


# Tampil Lokasi
@app.route('/lokasi')
def tampil_lokasi():
    if 'username' not in session:
        return redirect('/login')

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lokasi")
    data_lokasi = cursor.fetchall()
    return render_template('lokasi/tampil_lokasi.html', lokasi_list=data_lokasi)

app.run(debug=True)
