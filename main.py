from flask import Flask, render_template, request, jsonify
import json
import os
from difflib import SequenceMatcher

app = Flask(__name__)

# Fungsi untuk memuat data dari file JSON
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return "data tidak ditemukan"

# Fungsi untuk menyimpan data ke file JSON
def save_data(data):
    try:
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

# Load data kelompok
data_kelompok = load_data()

def similarity(a, b):
    """Menghitung similarity antara dua string"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def cari_siswa(nama_input):
    """Mencari siswa berdasarkan input nama pada struktur JSON baru"""
    hasil = []

    # Pastikan iterasi pada list siswa
    siswa_list = []
    if isinstance(data_kelompok, dict):
        # JSON berupa dict, iterasi pada values jika values dict berisi siswa
        # jika data_kelompok langsung list, gunakan itu
        # jika dict dengan key 'siswa', gunakan list di dalamnya
        if 'siswa' in data_kelompok and isinstance(data_kelompok['siswa'], list):
            siswa_list = data_kelompok['siswa']
        else:
            siswa_list = list(data_kelompok.values())
    elif isinstance(data_kelompok, list):
        siswa_list = data_kelompok
    else:
        return []

    for siswa in siswa_list:
        # Pastikan siswa adalah dict
        if not isinstance(siswa, dict):
            continue
        nama = siswa.get('nama', '')
        if nama_input.lower() in nama.lower():
            score = similarity(nama_input, nama)
            hasil.append({
                'nama_lengkap': nama,
                'kelas': siswa.get('kelas'),
                'kegiatan': siswa.get('kegiatan', []),
                'absen': siswa.get('absen'),
                'similarity': score
            })

    # Urutkan berdasarkan similarity tertinggi, lalu alfabet
    hasil.sort(key=lambda x: (-x['similarity'], x['nama_lengkap']))
    return hasil

def update_absen_siswa(nama_lengkap, absen_status):
    """Update status absen siswa di data JSON"""
    global data_kelompok
    
    try:
        # Reload data terbaru
        data_kelompok = load_data()
        print(f"DEBUG: Loaded data type: {type(data_kelompok)}")
        
        if data_kelompok == "data tidak ditemukan":
            print("ERROR: Data file tidak ditemukan")
            return False
        
        # Tentukan struktur data
        siswa_list = []
        if isinstance(data_kelompok, dict):
            if 'siswa' in data_kelompok and isinstance(data_kelompok['siswa'], list):
                siswa_list = data_kelompok['siswa']
                print(f"DEBUG: Using data_kelompok['siswa'], found {len(siswa_list)} students")
            else:
                siswa_list = list(data_kelompok.values())
                print(f"DEBUG: Using dict values, found {len(siswa_list)} items")
        elif isinstance(data_kelompok, list):
            siswa_list = data_kelompok
            print(f"DEBUG: Using direct list, found {len(siswa_list)} students")
        else:
            print("ERROR: Data format tidak dikenal")
            return False
        
        # Cari dan update siswa
        for i, siswa in enumerate(siswa_list):
            if isinstance(siswa, dict) and siswa.get('nama') == nama_lengkap:
                print(f"DEBUG: Found student {nama_lengkap} at index {i}")
                print(f"DEBUG: Current absen status: {siswa.get('absen')}")
                siswa['absen'] = absen_status
                print(f"DEBUG: Updated absen status to: {absen_status}")
                
                success = save_data(data_kelompok)
                print(f"DEBUG: Save result: {success}")
                return success
        
        print(f"ERROR: Student {nama_lengkap} not found in data")
        return False
        
    except Exception as e:
        print(f"EXCEPTION in update_absen_siswa: {str(e)}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cari', methods=['POST'])
def cari():
    nama = request.form.get('nama', '').strip()
    
    if not nama:
        return jsonify({'error': 'Nama tidak boleh kosong'})
    
    hasil = cari_siswa(nama)
    
    if not hasil:
        return jsonify({'error': f'Tidak ditemukan siswa dengan nama "{nama}"'})
    
    return jsonify({'hasil': hasil})

@app.route('/update_absen', methods=['POST'])
def update_absen():
    try:
        nama = request.form.get('nama', '').strip()
        absen_status = request.form.get('absen', '').strip()
        
        print(f"DEBUG: Received request - nama: {nama}, absen: {absen_status}")
        
        if not nama:
            print("ERROR: Nama kosong")
            return jsonify({'error': 'Nama tidak boleh kosong', 'success': False}), 400
        
        if not absen_status:
            print("ERROR: Status absen kosong")
            return jsonify({'error': 'Status absen tidak valid', 'success': False}), 400
        
        # Update absen di data JSON
        success = update_absen_siswa(nama, absen_status)
        
        if success:
            print(f"SUCCESS: Absen {nama} berhasil diupdate")
            return jsonify({'success': True, 'message': f'Absen {nama} berhasil diupdate'})
        else:
            print(f"ERROR: Gagal mengupdate absen {nama}")
            return jsonify({'error': 'Gagal mengupdate data absen', 'success': False}), 500
            
    except Exception as e:
        print(f"EXCEPTION in update_absen: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}', 'success': False}), 500

if __name__ == '__main__':
    app.run(debug=True)