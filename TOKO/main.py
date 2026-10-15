
import subprocess


def buka_tambah_produk():
    subprocess.run(["python", "tambah_produk.py"])


def buka_tampil_produk():
    subprocess.run(["python", "tampil_produk.py"])


def menu_utama():
    while True:
        print("\n" + "=" * 40)
        print(" SISTEM TOKO ONLINE ".center(40, "="))
        print("=" * 40)
        print("1. Tambah Produk")
        print("2. Tampilkan Produk")
        print("0. Keluar")
        print("=" * 40)

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            buka_tambah_produk()

        elif pilihan == "2":
            buka_tampil_produk()

        elif pilihan == "0":
            print("Terima kasih telah menggunakan toko online.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    menu_utama()
