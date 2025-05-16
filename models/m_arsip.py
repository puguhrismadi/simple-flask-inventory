from config.db import get_connection as db
def get_all_arsip():
    conn = db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM arsip")
    result = cursor.fetchall()
    conn.close()
    return result

def get_arsip_by_id(id_arsip):
    conn = db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM arsip WHERE id_arsip = %s", (id_arsip,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_files_by_arsip(id_arsip):
    conn = db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM arsip_file WHERE arsip_id = %s", (id_arsip,))
    result = cursor.fetchall()
    conn.close()
    return result