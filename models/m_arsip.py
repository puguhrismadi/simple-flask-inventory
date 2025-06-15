from config.db import get_connection

def get_all_arsip():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            a.id_arsip, 
            a.nama_arsip, 
            a.keterangan, 
            k.nama_kategori 
        FROM arsip a 
        LEFT JOIN kategori_arsip k ON a.kategori_id = k.id_kategori
        ORDER BY a.id_arsip DESC
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

def get_arsip_by_id(id_arsip):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = """
        SELECT 
            a.id_arsip, 
            a.nama_arsip, 
            a.keterangan, 
            k.nama_kategori 
        FROM arsip a 
        LEFT JOIN kategori_arsip k ON a.kategori_id = k.id_kategori
        WHERE a.id_arsip = %s
    """
    cursor.execute(query, (id_arsip,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_files_by_arsip(id_arsip):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM arsip_file WHERE arsip_id = %s", (id_arsip,))
    result = cursor.fetchall()
    conn.close()
    return result

def get_all_kategori():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM kategori_arsip ORDER BY nama_kategori ASC")
    result = cursor.fetchall()
    conn.close()
    return result
