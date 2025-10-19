import pyinputplus as pyip
from datetime import datetime
from prettytable import PrettyTable

# --- Data Produk dan ID ---
produk = {}  # key = ID, value = dict(nama, stok, harga)
id_counter = 1  # ID unik auto-increment

# --- Data Transaksi & Pengeluaran ---
transaksi = []  # list of dict: {id, nama, jumlah, total}
pengeluaran = []  # list of dict: {jenis, jumlah}

# --- Fungsi Logging ---
def tulis_log(aksi):
    with open("log_urban_farming.txt", "a") as f:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{waktu}] {aksi}\n")

# --- Fungsi Sub-Menu ---
def tampilkan_produk():
    tulis_log("Masuk ke menu: Tampilkan Produk")
    print("\n=== Daftar Produk ===")
    if produk:
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Stok", "Harga"]
        for pid, info in produk.items():
            table.add_row([pid, info["nama"], info["stok"], info["harga"]])
        print(table)
    else:
        print("Belum ada produk.")
    input("Tekan Enter untuk kembali ke menu utama...")

def tambah_produk():
    global id_counter
    tulis_log("Masuk ke menu: Tambah Produk")
    print("\n=== Tambah Produk ===")
    nama = input("Nama produk: ")
    stok = pyip.inputNum("Stok: ", min=0)
    harga = pyip.inputNum("Harga: ", min=0)
    produk[id_counter] = {"nama": nama, "stok": stok, "harga": harga}
    tulis_log(f"Produk ditambah: ID {id_counter}, Nama: {nama}, Stok: {stok}, Harga: {harga}")
    print(f"Produk ditambahkan dengan ID: {id_counter}")
    id_counter += 1
    input("Tekan Enter untuk kembali ke menu utama...")

def update_produk():
    tulis_log("Masuk ke menu: Update Produk")
    tampilkan_produk()
    pid = pyip.inputNum("Masukkan ID produk yang ingin diubah: ", min=1)
    if pid in produk:
        print("1. Ubah Nama")
        print("2. Ubah Stok")
        print("3. Ubah Harga")
        opsi = pyip.inputNum("Pilih opsi (1-3): ", min=1, max=3)
        if opsi == 1:
            baru = input("Nama baru: ")
            tulis_log(f"Nama produk diubah: ID {pid}, {produk[pid]['nama']} -> {baru}")
            produk[pid]["nama"] = baru
        elif opsi == 2:
            stok_baru = pyip.inputNum("Stok baru: ", min=0)
            tulis_log(f"Stok produk diubah: ID {pid}, {produk[pid]['stok']} -> {stok_baru}")
            produk[pid]["stok"] = stok_baru
        elif opsi == 3:
            harga_baru = pyip.inputNum("Harga baru: ", min=0)
            tulis_log(f"Harga produk diubah: ID {pid}, {produk[pid]['harga']} -> {harga_baru}")
            produk[pid]["harga"] = harga_baru
    else:
        print("Produk tidak ditemukan.")
    input("Tekan Enter untuk kembali ke menu utama...")

def hapus_produk():
    tulis_log("Masuk ke menu: Hapus Produk")
    tampilkan_produk()
    pid = pyip.inputNum("Masukkan ID produk yang ingin dihapus: ", min=1)
    if pid in produk:
        tulis_log(f"Produk dihapus: ID {pid}, Nama: {produk[pid]['nama']}")
        produk.pop(pid)
        print("Produk berhasil dihapus.")
    else:
        print("Produk tidak ditemukan.")
    input("Tekan Enter untuk kembali ke menu utama...")

def transaksi_penjualan():
    tulis_log("Masuk ke menu: Transaksi Penjualan")
    print("\n=== Transaksi Penjualan ===")

    keranjang = []  # daftar item sementara untuk transaksi saat ini
    total_semua = 0

    while True:
        tampilkan_produk()
        pid = pyip.inputNum("Masukkan ID produk yang dijual (0 untuk selesai): ", min=0)
        if pid == 0:
            break
        if pid not in produk:
            print("Produk tidak ditemukan.")
            continue

        jumlah = pyip.inputNum("Jumlah: ", min=1)
        if jumlah > produk[pid]["stok"]:
            print("Stok tidak cukup.")
            continue

        total = jumlah * produk[pid]["harga"]
        total_semua += total
        keranjang.append({
            "id": pid,
            "nama": produk[pid]["nama"],
            "jumlah": jumlah,
            "total": total
        })

        produk[pid]["stok"] -= jumlah
        print(f"{produk[pid]['nama']} ditambahkan ke keranjang (Subtotal: {total}).")
        tambah_lagi = input("Tambah produk lain? (y/n): ").lower()
        if tambah_lagi != "y":
            break

    if not keranjang:
        print("Tidak ada produk dalam transaksi.")
        return

    print("\n=== Rincian Transaksi ===")
    table = PrettyTable()
    table.field_names = ["ID", "Nama", "Jumlah", "Total"]
    for item in keranjang:
        table.add_row([item["id"], item["nama"], item["jumlah"], item["total"]])
    print(table)
    print(f"Total keseluruhan: {total_semua}")

    tunai = pyip.inputNum("Masukkan jumlah uang diterima: ", min=total_semua)
    kembalian = tunai - total_semua
    waktu_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Transaksi berhasil. Kembalian: {kembalian}\n")

    # Simpan semua item transaksi dengan waktu transaksi
    for item in keranjang:
        transaksi.append({
            "waktu": waktu_transaksi,
            "id": item["id"],
            "nama": item["nama"],
            "jumlah": item["jumlah"],
            "total": item["total"],
            "tunai": tunai
        })

    tulis_log(f"Transaksi selesai: Total {total_semua}, Tunai {tunai}, Kembalian {kembalian}")
    input("Tekan Enter untuk kembali ke menu utama...")

def catat_pengeluaran():
    tulis_log("Masuk ke menu: Catat Pengeluaran")
    print("\n=== Catat Pengeluaran ===")
    jenis = input("Jenis pengeluaran: ")
    jumlah = pyip.inputNum("Jumlah: ", min=0)
    pengeluaran.append({"jenis": jenis, "jumlah": jumlah})
    tulis_log(f"Pengeluaran dicatat: {jenis}, Jumlah: {jumlah}")
    print("Pengeluaran berhasil dicatat.")
    input("Tekan Enter untuk kembali ke menu utama...")

def laporan_keuangan():
    tulis_log("Masuk ke menu: Laporan Keuangan")
    print("\n=== LAPORAN KEUANGAN ===")

    # Pilihan filter bulan
    print("1. Tampilkan semua bulan")
    print("2. Tampilkan berdasarkan bulan tertentu (1-12)")
    opsi = pyip.inputNum("Pilih opsi (1/2): ", min=1, max=2)

    bulan_filter = None
    if opsi == 2:
        bulan_filter = pyip.inputNum("Masukkan nomor bulan (1 = Jan, 12 = Des): ", min=1, max=12)

    # --- Bagian 1: Laporan Aset Produk ---
    print("\n--- Aset Produk ---")
    table_produk = PrettyTable()
    table_produk.field_names = ["ID", "Nama", "Stok", "Harga", "Total Nilai"]
    total_aset = 0
    for pid, info in produk.items():
        total_value = info["stok"] * info["harga"]
        total_aset += total_value
        table_produk.add_row([pid, info["nama"], info["stok"], info["harga"], total_value])
    print(table_produk)
    print(f"Total Nilai Aset Produk: Rp {total_aset:,}")

    # --- Bagian 2: Laporan Transaksi Penjualan ---
    print("\n--- Riwayat Transaksi Penjualan ---")
    if transaksi:
        table_transaksi = PrettyTable()
        table_transaksi.field_names = ["Waktu", "ID Produk", "Nama Produk", "Jumlah", "Total", "Tunai"]
        total_penjualan = 0

        for t in transaksi:
            bulan_transaksi = int(datetime.strptime(t["waktu"], "%Y-%m-%d %H:%M:%S").month)
            if bulan_filter is None or bulan_transaksi == bulan_filter:
                table_transaksi.add_row([t["waktu"], t["id"], t["nama"], t["jumlah"], t["total"], t["tunai"]])
                total_penjualan += t["total"]

        if total_penjualan > 0:
            print(table_transaksi)
            print(f"Total Penjualan Bulan Ini: Rp {total_penjualan:,}")
        else:
            print("Tidak ada transaksi pada bulan tersebut.")
    else:
        print("Belum ada transaksi penjualan.")

    # --- Bagian 3: Laporan Pengeluaran ---
    print("\n--- Daftar Pengeluaran ---")
    if pengeluaran:
        table_pengeluaran = PrettyTable()
        table_pengeluaran.field_names = ["Jenis", "Jumlah"]
        total_pengeluaran = sum(p["jumlah"] for p in pengeluaran)
        for p in pengeluaran:
            table_pengeluaran.add_row([p["jenis"], p["jumlah"]])
        print(table_pengeluaran)
        print(f"Total Pengeluaran: Rp {total_pengeluaran:,}")
    else:
        total_pengeluaran = 0
        print("Belum ada data pengeluaran.")

    # --- Bagian 4: Ringkasan Keuangan ---
    pendapatan_bersih = (sum(t["total"] for t in transaksi)) - total_pengeluaran
    print("\n--- Ringkasan Keuangan ---")
    print(f"Total Penjualan   : Rp {sum(t['total'] for t in transaksi):,}")
    print(f"Total Pengeluaran : Rp {total_pengeluaran:,}")
    print(f"Pendapatan Bersih : Rp {pendapatan_bersih:,}")

    input("\nTekan Enter untuk kembali ke menu utama...")

# --- Loop Menu Utama ---
while True:
    print("\n=== PASAR URBAN FARMING ===")
    print("1. Data Produk")
    print("2. Tambah Produk")
    print("3. Update Produk")
    print("4. Hapus Produk")
    print("5. Transaksi Penjualan")
    print("6. Catat Pengeluaran")
    print("7. Laporan Keuangan")
    print("8. Keluar")

    menu = pyip.inputNum("Pilih menu (1-8): ", min=1, max=8)
    tulis_log(f"Memilih menu utama: {menu}")

    if menu == 1:
        tampilkan_produk()
    elif menu == 2:
        tambah_produk()
    elif menu == 3:
        update_produk()
    elif menu == 4:
        hapus_produk()
    elif menu == 5:
        transaksi_penjualan()
    elif menu == 6:
        catat_pengeluaran()
    elif menu == 7:
        laporan_keuangan()
    elif menu == 8:
        tulis_log("Keluar dari program")
        print("Terima kasih telah menggunakan Pasar Urban Farming.")
        break
