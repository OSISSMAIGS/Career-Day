import json
from collections import defaultdict

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_duplicate_groups(data):
    """
    Kembalikan dict: nama -> list of indices
    """
    nama_indices = defaultdict(list)
    for idx, entry in enumerate(data):
        nama = entry.get('nama', '').strip()
        nama_indices[nama].append(idx)
    # hanya kembalikan yang >1
    return {nama: idxs for nama, idxs in nama_indices.items() if len(idxs) > 1}

def remove_duplicates_keep_latest(data):
    """
    Membangun list baru yang:
    - semua nama unik (hanya satu entri)
    - untuk nama duplikat, hanya entri dengan index paling besar (terakhir) yang dipertahankan
    """
    # Temukan kelompok duplikat
    dup_groups = find_duplicate_groups(data)

    # Hitung index terakhir untuk tiap nama yang duplikat
    last_index = {nama: idxs[-1] for nama, idxs in dup_groups.items()}

    # Buat filtered list
    cleaned = []
    for idx, entry in enumerate(data):
        nama = entry.get('nama', '').strip()
        if nama in last_index:
            # hanya tambahkan jika idx == last_index[nama]
            if idx == last_index[nama]:
                cleaned.append(entry)
        else:
            # nama unik, selalu tambahkan
            cleaned.append(entry)

    return cleaned

def save_data(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def print_summary(original, cleaned):
    dup = find_duplicate_groups(original)
    if not dup:
        print("Tidak ada nama duplikat. Data tidak berubah.")
    else:
        print(f"Ditemukan {len(dup)} nama duplikat:")
        for nama, idxs in dup.items():
            print(f"- \"{nama}\" pada indices {idxs}, dipertahankan index terakhir: {idxs[-1]}")
        print(f"\nSebelum: {len(original)} entri")
        print(f"Sesudah: {len(cleaned)} entri (duplikat dihapus)")

if __name__ == "__main__":
    # Ganti dengan path file JSON Anda
    input_path = 'data.json'
    output_path = 'cleaned_data.json'

    # 1. Load
    data = load_data(input_path)

    # 2. Hapus duplikat (keep latest)
    cleaned_data = remove_duplicates_keep_latest(data)

    # 3. Simpan hasil
    save_data(cleaned_data, output_path)

    # 4. Cetak ringkasan
    print_summary(data, cleaned_data)
