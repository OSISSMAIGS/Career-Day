import json
import sqlite3
import os
from typing import List, Dict, Any

def create_database(db_name: str = "siswa_kegiatan.db"):
    """
    Membuat database SQLite dan tabel yang diperlukan
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Buat tabel siswa
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            absen TEXT NOT NULL
        )
    ''')
    
    # Buat tabel kegiatan
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS kegiatan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            siswa_id INTEGER,
            kegiatan_text TEXT NOT NULL,
            FOREIGN KEY (siswa_id) REFERENCES siswa (id)
        )
    ''')
    
    conn.commit()
    return conn

def insert_data_to_db(conn: sqlite3.Connection, data: List[Dict[str, Any]]):
    """
    Memasukkan data dari JSON ke dalam database SQLite
    """
    cursor = conn.cursor()
    
    for siswa in data:
        # Insert data siswa
        cursor.execute('''
            INSERT INTO siswa (nama, kelas, absen) 
            VALUES (?, ?, ?)
        ''', (siswa['nama'], siswa['kelas'], siswa['absen']))
        
        # Dapatkan ID siswa yang baru diinsert
        siswa_id = cursor.lastrowid
        
        # Insert kegiatan untuk siswa tersebut
        for kegiatan in siswa['kegiatan']:
            cursor.execute('''
                INSERT INTO kegiatan (siswa_id, kegiatan_text) 
                VALUES (?, ?)
            ''', (siswa_id, kegiatan))
    
    conn.commit()

def json_to_sqlite(json_file_path: str, db_name: str = "siswa_kegiatan.db"):
    """
    Fungsi utama untuk mengkonversi JSON file ke SQLite database
    """
    try:
        # Baca file JSON
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Hapus database lama jika ada (opsional)
        if os.path.exists(db_name):
            os.remove(db_name)
            print(f"Database lama '{db_name}' telah dihapus.")
        
        # Buat database dan tabel
        conn = create_database(db_name)
        print(f"Database '{db_name}' berhasil dibuat.")
        
        # Insert data
        insert_data_to_db(conn, data)
        print(f"Data berhasil dimasukkan ke database '{db_name}'.")
        
        # Tutup koneksi
        conn.close()
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{json_file_path}' tidak ditemukan.")
        return False
    except json.JSONDecodeError:
        print(f"Error: File '{json_file_path}' bukan format JSON yang valid.")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def view_data_from_db(db_name: str = "siswa_kegiatan.db"):
    """
    Fungsi untuk melihat data yang telah dimasukkan ke database
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Query untuk melihat semua data siswa beserta kegiatannya
        cursor.execute('''
            SELECT s.id, s.nama, s.kelas, s.absen, k.kegiatan_text
            FROM siswa s
            LEFT JOIN kegiatan k ON s.id = k.siswa_id
            ORDER BY s.id, k.id
        ''')
        
        results = cursor.fetchall()
        
        print("\n=== DATA DALAM DATABASE ===")
        print("ID | Nama | Kelas | Absen | Kegiatan")
        print("-" * 80)
        
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error saat membaca database: {str(e)}")

def create_sample_json(filename: str = "sample_data.json"):
    """
    Membuat file JSON contoh untuk testing
    """
    sample_data = []
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(sample_data, file, ensure_ascii=False, indent=2)
    
    print(f"File contoh '{filename}' berhasil dibuat.")

# Contoh penggunaan
if __name__ == "__main__":
    # Buat file JSON contoh (opsional)
    create_sample_json("data_siswa.json")
    
    # Konversi JSON ke SQLite
    json_file = "data.json"  # Ganti dengan path file JSON Anda
    db_file = "data.db"
    
    if json_to_sqlite(json_file, db_file):
        print("Konversi berhasil!")
        # Tampilkan data untuk verifikasi
        view_data_from_db(db_file)
    else:
        print("Konversi gagal!")