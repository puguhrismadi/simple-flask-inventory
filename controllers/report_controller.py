from flask import Blueprint, render_template, send_file
from config.db import get_connection as get_db_connection
from fpdf import FPDF
import os
import xlsxwriter
from io import BytesIO
report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total_arsip FROM arsip")
    total_arsip = cursor.fetchone()['total_arsip']

    # Hitung size dari direktori /static/uploads/arsip/
    folder_path = os.path.join('static', 'uploads', 'arsip')
    total_size = 0
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            total_size += os.path.getsize(file_path)
    total_size = total_size / (1024 * 1024)  # MB

    cursor.execute("""
        SELECT kategori_arsip.nama_kategori, COUNT(arsip.id_arsip) AS jumlah
        FROM kategori_arsip
        LEFT JOIN arsip ON arsip.kategori_id = kategori_arsip.id_kategori
        GROUP BY kategori_arsip.id_kategori
    """)
    kategori_data = cursor.fetchall()

    conn.close()
    return render_template('/report/dashboard.html', total_arsip=total_arsip, total_size=total_size, kategori_data=kategori_data)

@report_bp.route('/dashboard/export/pdf')
def export_dashboard_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_arsip FROM arsip")
    total_arsip = cursor.fetchone()['total_arsip']

    folder_path = os.path.join('static', 'uploads', 'arsip')
    total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    total_size = total_size / (1024 * 1024)

    pdf.cell(200, 10, txt="Dashboard Arsip", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(0, 10, txt=f"Total Arsip: {total_arsip}", ln=True)
    pdf.cell(0, 10, txt=f"Total Storage: {total_size:.2f} MB", ln=True)
    pdf.ln(10)

    cursor.execute("""
        SELECT kategori_arsip.nama_kategori, COUNT(arsip.id_arsip) AS jumlah
        FROM kategori_arsip
        LEFT JOIN arsip ON arsip.kategori_id = kategori_arsip.id_kategori
        GROUP BY kategori_arsip.id_kategori
    """)
    kategori_data = cursor.fetchall()

    pdf.cell(0, 10, txt="Arsip per Kategori:", ln=True)
    for k in kategori_data:
        pdf.cell(0, 10, txt=f"{k['nama_kategori']}: {k['jumlah']}", ln=True)

    conn.close()

    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_output)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="dashboard_arsip.pdf", mimetype='application/pdf')

@report_bp.route('/dashboard/export/excel')
def export_dashboard_excel():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_arsip FROM arsip")
    total_arsip = cursor.fetchone()['total_arsip']

    folder_path = os.path.join('static', 'uploads', 'arsip')
    total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    total_size = total_size / (1024 * 1024)

    worksheet.write('A1', 'Total Arsip')
    worksheet.write('B1', total_arsip)
    worksheet.write('A2', 'Total Storage (MB)')
    worksheet.write('B2', total_size)

    cursor.execute("""
        SELECT kategori_arsip.nama_kategori, COUNT(arsip.id_arsip) AS jumlah
        FROM kategori_arsip
        LEFT JOIN arsip ON arsip.kategori_id = kategori_arsip.id_kategori
        GROUP BY kategori_arsip.id_kategori
    """)
    kategori_data = cursor.fetchall()

    worksheet.write('A4', 'Kategori')
    worksheet.write('B4', 'Jumlah Arsip')

    row = 4
    for k in kategori_data:
        worksheet.write(row, 0, k['nama_kategori'])
        worksheet.write(row, 1, k['jumlah'])
        row += 1

    workbook.close()
    output.seek(0)

    conn.close()

    return send_file(output, as_attachment=True, download_name="dashboard_arsip.xlsx", mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@report_bp.route('/laporan-aktivitas')
def laporan_aktivitas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Data aktivitas (misal log upload/view)
    cursor.execute("""
        SELECT log_aktivitas.id_log, log_aktivitas.aktivitas, log_aktivitas.waktu, pengguna.username
        FROM log_aktivitas
        JOIN pengguna ON log_aktivitas.user_id = pengguna.id_user
        ORDER BY log_aktivitas.waktu DESC
    """)
    aktivitas_data = cursor.fetchall()

    conn.close()
    return render_template('laporan_aktivitas.html', aktivitas_data=aktivitas_data)


@report_bp.route('/statistik-penyimpanan')
def statistik_penyimpanan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Total arsip
    cursor.execute("SELECT COUNT(*) AS total_arsip FROM arsip")
    total_arsip = cursor.fetchone()['total_arsip']

   

    conn.close()
    return render_template('statistik_penyimpanan.html', total_arsip=total_arsip)
@report_bp.route('/dashboard/export/formal_pdf')
def export_formal_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Logo
    logo_path = os.path.join('static', 'uploads', 'logo.png')  # pastikan file logo.png ada di sini
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=20)  # posisi X=10, Y=8, lebar=20 mm

    # Nama Instansi
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "DINAS KEARSIPAN DAN PERPUSTAKAAN", ln=True, align="C")
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 7, "Jl. Contoh No. 123, Kota Contoh", ln=True, align="C")
    pdf.ln(5)  # jarak bawah header

    # Judul Laporan
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "LAPORAN DASHBOARD ARSIP", ln=True, align="C")
    pdf.ln(10)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS total_arsip FROM arsip")
    total_arsip = cursor.fetchone()['total_arsip']

    folder_path = os.path.join('static', 'uploads', 'arsip')
    total_size = sum(os.path.getsize(os.path.join(folder_path, f)) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)))
    total_size = total_size / (1024 * 1024)

    # Data ringkasan
    pdf.set_font("Arial", '', 11)
    pdf.cell(60, 8, "Total Arsip", border=1)
    pdf.cell(0, 8, str(total_arsip), border=1, ln=True)
    pdf.cell(60, 8, "Total Storage", border=1)
    pdf.cell(0, 8, f"{total_size:.2f} MB", border=1, ln=True)
    pdf.ln(8)

    # Tabel kategori
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(90, 8, "Kategori Arsip", border=1, align="C")
    pdf.cell(40, 8, "Jumlah Arsip", border=1, align="C")
    pdf.ln()

    cursor.execute("""
        SELECT kategori_arsip.nama_kategori, COUNT(arsip.id_arsip) AS jumlah
        FROM kategori_arsip
        LEFT JOIN arsip ON arsip.kategori_id = kategori_arsip.id_kategori
        GROUP BY kategori_arsip.id_kategori
    """)
    kategori_data = cursor.fetchall()

    pdf.set_font("Arial", '', 11)
    for k in kategori_data:
        pdf.cell(90, 8, k['nama_kategori'], border=1)
        pdf.cell(40, 8, str(k['jumlah']), border=1, ln=True)

    conn.close()

    # Output ke BytesIO
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_output)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name="dashboard_arsip.pdf", mimetype='application/pdf')
