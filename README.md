# Career-Day

Aplikasi web absensi dan pencarian data siswa untuk acara Binus Career Day di SMA IGS. Aplikasi ini memudahkan panitia untuk mencari data siswa, melihat kegiatan yang diikuti, dan mengelola status kehadiran (absen) secara real-time.

## Fitur Utama

- **Pencarian Siswa:** Cari data lengkap siswa berdasarkan nama.
- **Absensi Online:** Update status kehadiran siswa secara langsung.
- **Konversi Data:** Mendukung konversi data dari CSV ke JSON dan SQLite.
- **Pengelolaan Data:** Hapus duplikat, bersihkan data, dan kelola database kegiatan siswa.

## Struktur Direktori

- `main.py` — Aplikasi utama berbasis Flask (web server).
- `data/` — Berisi data mentah, script konversi, dan file hasil konversi.
  - `converter.py` — Konversi data CSV ke JSON.
  - `delete_csv.py` — Menghapus file CSV yang tidak diperlukan.
  - `data_kelas11.csv/json`, `data_kelas12.json` — Data siswa per kelas.
  - `ss.xlsx` — Data mentah (opsional).
- `data.json` — Data utama siswa dan kegiatan (format JSON).
- `find_dupes.py` — Script untuk menghapus data duplikat.
- `json_to_sqlite.py` — Konversi data JSON ke database SQLite.
- `static/` — File statis (CSS, JS, gambar/logo).
- `templates/` — Template HTML untuk tampilan web.
- `requirements.txt` — Daftar dependensi Python.

## Cara Instalasi & Menjalankan

1. **Clone repository ini**
2. **Install dependensi**
   ```bash
   pip install -r requirements.txt
   ```
3. **Jalankan aplikasi**
   ```bash
   python main.py
   ```
   Aplikasi akan berjalan di `http://localhost:5000`

4. **(Opsional) Konversi data**
   - Untuk mengubah data CSV ke JSON:
     ```bash
     python data/converter.py
     ```
   - Untuk menghapus duplikat:
     ```bash
     python find_dupes.py
     ```
   - Untuk konversi ke SQLite:
     ```bash
     python json_to_sqlite.py
     ```

## Teknologi yang Digunakan

- Python 3.x
- Flask
- SQLite (opsional, untuk database)
- HTML, CSS, JavaScript (Frontend)