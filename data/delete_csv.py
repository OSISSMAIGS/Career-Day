import os
from pathlib import Path

def delete_csv_files(directory: str) -> None:
    """
    Menghapus semua file .csv di dalam direktori yang diberikan.

    Args:
        directory (str): Path ke direktori target.
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        print(f"Tidak ditemukan direktori: {directory}")
        return

    # Cari semua file dengan ekstensi .csv
    csv_files = list(dir_path.glob("*.csv"))
    if not csv_files:
        print("Tidak ada file .csv yang ditemukan.")
        return

    # Hapus satu per satu
    for file_path in csv_files:
        try:
            file_path.unlink()
            print(f"Removed: {file_path.name}")
        except Exception as e:
            print(f"Gagal menghapus {file_path.name}: {e}")

if __name__ == "__main__":
    # Gunakan "." untuk direktori saat ini, atau ganti dengan path lain
    delete_csv_files(".")
