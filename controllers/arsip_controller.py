from flask import request, redirect, url_for, render_template, Blueprint, current_app
from werkzeug.utils import secure_filename
import os
import models.m_arsip as arsip_model
arsip_bp = Blueprint('arsip_bp', __name__, template_folder='../templates/arsip')

# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf', 'mp3', 'wav', 'mp4', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# helper file check
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png', 'pdf', 'mp3', 'wav', 'mp4'}

@arsip_bp.route('/arsip/upload', methods=['GET', 'POST'])
def upload_arsip():
    # Ambil list kategori
    conn = db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori")
    kategori_list = cursor.fetchall()

    if request.method == 'POST':
        nama_arsip = request.form['nama_arsip']
        kategori_id = request.form['kategori_id']
        keterangan = request.form['keterangan']

        # Simpan arsip ke database
        insert_arsip_query = "INSERT INTO arsip (nama_arsip, kategori_id, keterangan) VALUES (%s, %s, %s)"
        cursor.execute(insert_arsip_query, (nama_arsip, kategori_id, keterangan))
        conn.commit()

        arsip_id = cursor.lastrowid  # ambil id arsip terakhir

        files = request.files.getlist('files')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = current_app.config['UPLOAD_FOLDER']
                file.save(os.path.join(upload_folder, filename))

                ext = filename.rsplit('.', 1)[1].lower()
                file_type = 'image' if ext in ['jpg', 'jpeg', 'png'] else \
                            'pdf' if ext == 'pdf' else \
                            'audio' if ext in ['mp3', 'wav'] else 'video'

                # Simpan file ke tabel arsip_file
                insert_file_query = "INSERT INTO arsip_file (arsip_id, file_path, file_type) VALUES (%s, %s, %s)"
                cursor.execute(insert_file_query, (arsip_id, filename, file_type))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('arsip_bp.index_arsip'))

    cursor.close()
    conn.close()
    return render_template('arsip/upload.html', kategori_list=kategori_list)
@arsip_bp.route('/arsip')
def index_arsip():
    arsip_list = arsip_model.get_all_arsip()
    return render_template('arsip/index.html', arsip_list=arsip_list)

@arsip_bp.route('/arsip/<int:id_arsip>')
def detail_arsip(id_arsip):
    conn = db()
    cursor = conn.cursor(dictionary=True)

    # Ambil data arsip
    cursor.execute("SELECT * FROM arsip WHERE id_arsip = %s", (id_arsip,))
    arsip = cursor.fetchone()

    # Ambil file-file arsip terkait
    cursor.execute("SELECT * FROM arsip_file WHERE arsip_id = %s", (id_arsip,))
    file_list = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('arsip/detail.html', arsip=arsip, file_list=file_list)
