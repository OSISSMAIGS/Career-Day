import csv
import json

def csv_to_activities(csv_filepath, json_filepath):
    """
    Baca CSV pendaftaran seminar & workshop, keluarkan JSON:
    [
      {
        "nama": "Nama Peserta",
        "kelas": "12 IPA 1",
        "kegiatan": [
          "Judul Seminar ...",
          "Judul Workshop ..."
        ]
      },
      ...
    ]
    """
    with open(csv_filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        result = []
        for row in reader:
            # Bersihkan dan ambil field
            nama    = row.get('NAMA', '').strip()
            kelas   = row.get('KELAS', '').strip()
            seminar = row.get('SEMINAR', '').strip()
            workshop= row.get('WORKSHOP', '').strip()
            
            # Lewatkan baris tanpa nama
            if not nama:
                continue
            
            # Kumpulkan kegiatan (seminar + workshop)
            kegiatan = []
            if seminar:
                kegiatan.append(seminar)
            if workshop:
                kegiatan.append(workshop)
            
            result.append({
                "nama": nama,
                "kelas": kelas,
                "kegiatan": kegiatan
            })
    
    # Tulis ke JSON dengan indentasi 2 spasi
    with open(json_filepath, 'w', encoding='utf-8') as j:
        json.dump(result, j, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    num = 11
    csv_path  = f"data_kelas{num}.csv"    # sesuaikan path input
    json_path = f"data_kelas{num}.json" # output JSON
    csv_to_activities(csv_path, json_path)
    print(f"✅ Berhasil menulis {len(open(json_path).read().splitlines())-1} entri ke {json_path}")
