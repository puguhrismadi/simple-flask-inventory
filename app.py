from flask import Flask, render_template, request, redirect, session
from config.db import db

app = Flask(__name__)
app.secret_key = 'your_secret_key'
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')
        else:
            return render_template('/views/templates/login.html', error='Invalid username or password')
    else:
        return render_template('/views/templates/login.html')
@app.route('/dashboard')
def dashboard():    
    return render_template('/views/templates/dashboard.html')   
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')
@app.route('/tambah')
def tambah():
    return render_template('/views/templates/barang/tambah_barang.html')

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
        return render_template('/views/templates/barang/tambah_barang.html', supplier_list=supplier_list)
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
        return render_template('/views/templates/barang/edit_barang.html', barang=barang, supplier_list=supplier_list)
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
        return render_template('/views/templates/supplier/tambah_supplier.html')
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
        return render_template('/views/templates/supplier/edit_supplier.html', supplier=supplier)
    
@app.route('/hapus_supplier/<int:id>', methods=['POST'])
def hapus_supplier(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM supplier WHERE id_supplier=%s", (id,))
    db.commit()
    cursor.close()
    return redirect('/dashboard')