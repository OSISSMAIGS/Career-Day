import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    """
    Mengubah file JSON menjadi CSV dengan transformasi:
    - absen "true" -> "hadir"
    - absen "false" -> "tidak hadir"
    - kegiatan array dijoinkan dengan " | "
    """
    
    try:
        # Membaca file JSON
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        
        # Jika data bukan list, wrap dalam list
        if not isinstance(data, list):
            data = [data]
        
        # Membuka file CSV untuk ditulis
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            # Header CSV
            fieldnames = ['nama', 'kelas', 'kegiatan', 'status_kehadiran']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            
            # Menulis header
            writer.writeheader()
            
            # Memproses setiap record
            for record in data:
                # Transformasi status absen
                if record['absen'] == 'true':
                    status = 'hadir'
                elif record['absen'] == 'false':
                    status = 'tidak hadir'
                else:
                    status = record['absen']  # fallback untuk nilai lain
                
                # Menggabungkan kegiatan dengan separator " | "
                kegiatan_str = ' | '.join(record['kegiatan'])
                
                # Menulis row ke CSV
                writer.writerow({
                    'nama': record['nama'],
                    'kelas': record['kelas'],
                    'kegiatan': kegiatan_str,
                    'status_kehadiran': status
                })
        
        print(f"Berhasil mengkonversi {json_file_path} ke {csv_file_path}")
        
    except FileNotFoundError:
        print(f"Error: File {json_file_path} tidak ditemukan!")
    except json.JSONDecodeError:
        print(f"Error: File {json_file_path} bukan format JSON yang valid!")
    except Exception as e:
        print(f"Error: {str(e)}")

def preview_csv(csv_file_path, num_rows=5):
    """
    Menampilkan preview CSV file
    """
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            print(f"\n=== Preview {csv_file_path} ===")
            for i, row in enumerate(reader):
                if i >= num_rows + 1:  # +1 untuk header
                    break
                print(f"Row {i}: {row}")
                
    except FileNotFoundError:
        print(f"File {csv_file_path} tidak ditemukan!")
    except Exception as e:
        print(f"Error saat preview: {str(e)}")

# Contoh penggunaan
if __name__ == "__main__":
    # Ganti path sesuai dengan lokasi file Anda
    input_json = "data.json"  # Path ke file JSON input
    output_csv = "output.csv"  # Path ke file CSV output
    
    # Konversi JSON ke CSV
    json_to_csv(input_json, output_csv)
    
    # Preview hasil
    preview_csv(output_csv)