import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk
from models import Produk

# UI untuk fitur yang memang sudah ada di program awal:
# 1. Tambah Produk
# 2. Tampilkan Produk
# 3. Refresh Data
# 4. Keluar
# Data tetap disimpan di produk.csv.

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "produk.csv")

NAVY = "#172554"
BLUE = "#2563EB"
BG = "#F3F6FB"
WHITE = "#FFFFFF"
TEXT = "#172033"
MUTED = "#64748B"
ORANGE = "#F59E0B"
BORDER = "#DCE4F0"


def rupiah(nilai):
    return "Rp" + f"{nilai:,}".replace(",", ".")


def muat_data():
    daftar_produk = []
    if not os.path.exists(CSV_PATH):
        return daftar_produk

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            if row[2].strip().lower() == "harga":
                continue
            try:
                produk = Produk(
                    nama=row[0].strip(),
                    kategori=row[1].strip(),
                    harga=int(row[2].strip()),
                    stok=int(row[3].strip())
                )
                daftar_produk.append(produk)
            except (ValueError, IndexError):
                # Mengikuti perilaku program awal: data tidak valid dilewati.
                continue
    return daftar_produk


class TokoUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Toko Online")
        self.root.geometry("1000x680")
        self.root.minsize(800, 560)
        self.root.configure(bg=BG)

        self.buat_tampilan()
        self.tampilkan_produk()

    def buat_tampilan(self):
        header = tk.Frame(self.root, bg=NAVY, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = tk.Label(
            header, text="TOKO", bg=ORANGE, fg=NAVY,
            font=("Segoe UI", 13, "bold"), padx=14, pady=10
        )
        logo.pack(side="left", padx=(26, 14), pady=22)

        judul = tk.Frame(header, bg=NAVY)
        judul.pack(side="left", pady=20)
        tk.Label(
            judul, text="Sistem Toko Online", bg=NAVY, fg=WHITE,
            font=("Segoe UI", 21, "bold")
        ).pack(anchor="w")
        tk.Label(
            judul, text="Pengelolaan data produk", bg=NAVY, fg="#D8E3F8",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(3, 0))

        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=26, pady=22)

        menu = tk.Frame(main, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        menu.pack(side="left", fill="y", padx=(0, 20))
        tk.Label(
            menu, text="MENU", bg=WHITE, fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(20, 12))

        self.tombol(menu, "＋  Tambah Produk", self.form_tambah, BLUE).pack(
            fill="x", padx=12, pady=5
        )
        self.tombol(menu, "☷  Tampilkan Produk", self.tampilkan_produk, NAVY).pack(
            fill="x", padx=12, pady=5
        )
        self.tombol(menu, "↻  Refresh Data", self.refresh_data, "#475569").pack(
            fill="x", padx=12, pady=5
        )
        self.tombol(menu, "Keluar", self.keluar, "#B91C1C").pack(
            fill="x", padx=12, pady=(22, 14)
        )

        content = tk.Frame(main, bg=BG)
        content.pack(side="left", fill="both", expand=True)

        tk.Label(
            content, text="Daftar Produk", bg=BG, fg=TEXT,
            font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")
        tk.Label(
            content, text="Data produk yang tersimpan di produk.csv",
            bg=BG, fg=MUTED, font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(4, 16))

        table_box = tk.Frame(content, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        table_box.pack(fill="both", expand=True)

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "Treeview", background=WHITE, foreground=TEXT, fieldbackground=WHITE,
            rowheight=34, font=("Segoe UI", 10), borderwidth=0
        )
        style.configure(
            "Treeview.Heading", background="#E8EEF9", foreground=NAVY,
            font=("Segoe UI", 10, "bold"), padding=10, relief="flat"
        )
        style.map("Treeview", background=[("selected", "#DCE8FF")],
                  foreground=[("selected", TEXT)])

        columns = ("nama", "kategori", "harga", "stok")
        self.tabel = ttk.Treeview(table_box, columns=columns, show="headings")
        self.tabel.heading("nama", text="Nama Produk")
        self.tabel.heading("kategori", text="Kategori")
        self.tabel.heading("harga", text="Harga (Rp)")
        self.tabel.heading("stok", text="Stok")
        self.tabel.column("nama", width=230, anchor="w")
        self.tabel.column("kategori", width=140, anchor="w")
        self.tabel.column("harga", width=140, anchor="e")
        self.tabel.column("stok", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(table_box, orient="vertical", command=self.tabel.yview)
        self.tabel.configure(yscrollcommand=scrollbar.set)
        self.tabel.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=8)

        self.status = tk.Label(
            content, text="", bg=BG, fg=MUTED,
            font=("Segoe UI", 9), anchor="w"
        )
        self.status.pack(fill="x", pady=(10, 0))

        footer = tk.Frame(self.root, bg=WHITE, height=34)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer, text="Sistem Toko Online • Python OOP",
            bg=WHITE, fg=MUTED, font=("Segoe UI", 9)
        ).pack(side="left", padx=26, pady=8)

    def tombol(self, parent, teks, perintah, warna):
        return tk.Button(
            parent, text=teks, command=perintah,
            bg=warna, fg=WHITE, activebackground=warna,
            activeforeground=WHITE, relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), anchor="w",
            padx=14, pady=12, cursor="hand2"
        )

    def tampilkan_produk(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        daftar = muat_data()
        for produk in daftar:
            self.tabel.insert(
                "", "end",
                values=(produk.nama, produk.kategori, rupiah(produk.harga), produk.stok)
            )
        self.status.config(text=f"Total Produk: {len(daftar)}")

    def refresh_data(self):
        self.tampilkan_produk()
        messagebox.showinfo("Refresh Data", "Data produk berhasil dimuat ulang.")

    def form_tambah(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Tambah Produk")
        dialog.geometry("440x440")
        dialog.resizable(False, False)
        dialog.configure(bg=BG)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog, text="Tambah Data Produk", bg=BG, fg=TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=24, pady=(22, 4))
        tk.Label(
            dialog, text="Isi semua kolom di bawah ini.", bg=BG, fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=24, pady=(0, 16))

        form = tk.Frame(dialog, bg=WHITE, highlightbackground=BORDER, highlightthickness=1)
        form.pack(fill="both", expand=True, padx=24, pady=(0, 22))
        fields = {}
        labels = [("nama", "Nama produk"), ("kategori", "Kategori"),
                  ("harga", "Harga (Rp)"), ("stok", "Stok")]
        for key, label_text in labels:
            row = tk.Frame(form, bg=WHITE)
            row.pack(fill="x", padx=16, pady=8)
            tk.Label(
                row, text=label_text, bg=WHITE, fg=TEXT,
                font=("Segoe UI", 10, "bold"), width=13, anchor="w"
            ).pack(side="left")
            entry = tk.Entry(
                row, font=("Segoe UI", 10), relief="solid",
                bd=1, highlightthickness=0
            )
            entry.pack(side="left", fill="x", expand=True, ipady=7)
            fields[key] = entry

        fields["nama"].focus_set()

        def simpan():
            nama = fields["nama"].get().strip()
            kategori = fields["kategori"].get().strip()
            harga_input = fields["harga"].get().strip()
            stok_input = fields["stok"].get().strip()

            if not nama or not kategori or not harga_input or not stok_input:
                messagebox.showwarning("Peringatan", "Semua kolom harus diisi!", parent=dialog)
                return
            try:
                harga = int(harga_input)
                stok = int(stok_input)
                if harga < 0 or stok < 0:
                    messagebox.showwarning(
                        "Peringatan", "Harga dan stok tidak boleh negatif!", parent=dialog
                    )
                    return
            except ValueError:
                messagebox.showwarning(
                    "Peringatan", "Harga dan stok harus berupa angka!", parent=dialog
                )
                return

            produk = Produk(nama, kategori, harga, stok)
            file_exists = os.path.exists(CSV_PATH)
            try:
                with open(CSV_PATH, "a", newline="", encoding="utf-8") as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(["Nama", "Kategori", "Harga", "Stok"])
                    writer.writerow(produk.to_list())
            except OSError as error:
                messagebox.showerror("Gagal", f"Data tidak dapat disimpan:\n{error}", parent=dialog)
                return

            messagebox.showinfo("Berhasil", "Produk berhasil ditambahkan.", parent=dialog)
            dialog.destroy()
            self.tampilkan_produk()

        self.tombol(form, "Simpan Produk", simpan, BLUE).pack(
            fill="x", padx=16, pady=(10, 16)
        )

    def keluar(self):
        if messagebox.askyesno("Keluar", "Yakin ingin keluar dari program?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TokoUI(root)
    root.mainloop()
