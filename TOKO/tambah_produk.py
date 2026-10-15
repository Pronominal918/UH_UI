
import csv
import os
from models import Produk


def simpan_produk():
    print("\n=== TAMBAH DATA PRODUK ===")

    nama = input("Nama produk : ").strip()
    kategori = input("Kategori    : ").strip()
    harga_input = input("Harga (Rp)  : ").strip()
    stok_input = input("Stok        : ").strip()

    if not nama or not kategori or not harga_input or not stok_input:
        print("\n[PERINGATAN] Semua kolom harus diisi!\n")
        return

    try:
        harga = int(harga_input)
        stok = int(stok_input)

        if harga < 0 or stok < 0:
            print("\n[PERINGATAN] Harga dan stok tidak boleh negatif!\n")
            return

    except ValueError:
        print("\n[PERINGATAN] Harga dan stok harus berupa angka!\n")
        return

    produk = Produk(nama, kategori, harga, stok)
    file_exists = os.path.exists("produk.csv")

    with open("produk.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Nama", "Kategori", "Harga", "Stok"])

        writer.writerow(produk.to_list())

    print("\n[BERHASIL] Produk berhasil ditambahkan.\n")


def main():
    while True:
        print("=== MENU TAMBAH PRODUK ===")
        print("1. Tambah Produk")
        print("0. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            simpan_produk()

        elif pilihan == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid.\n")


if __name__ == "__main__":
    main()
