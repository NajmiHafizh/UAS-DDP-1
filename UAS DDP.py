import time
from prettytable import PrettyTable
import random
from datetime import timedelta, datetime

akun = {
    "Najmi": {"password": "abcd1", "role": "Biasa", "terkunci": False},
    "Hafizh": {"password": "1234z", "role": "VIP", "terkunci": False},
}

saldo_emoney = {
    "Najmi": 100000,
    "Hafizh": 200000,
}

skin_barang = {
    "pagi": {
        "pakaian": [("Kemeja Taktikal", 1000), ("Celana Pendek Militer", 1200), ("Jaket Survival", 1400)],
        "senjata": [("AKM Desert", 1600), ("M416 Glacier", 1800), ("UMP Urban", 2000)],
    },
    "siang": {
        "pakaian": [("Hoodie Hitam", 1100), ("Jeans Kasual", 1300), ("Rompi Taktik", 1500)],
        "senjata": [("SCAR-L Sandstorm", 1700), ("Kar98k Arctic", 1900), ("Vector Tech", 2100)],
    },
    "malam": {
        "pakaian": [("Coat Phantom", 1000), ("Celana Elite", 1100), ("Topi Operator", 1200)],
        "senjata": [("Groza Shadow", 1300), ("AWM Volcano", 1400), ("Shotgun Viper", 1500)],
    },
    "khusus_vip": {
        "pakaian": [("Armor Eksklusif VIP", 3000)],
        "senjata": [("Senapan Sniper VIP", 4500)],
    },
}

class Voucher:
    def __init__(self, kode, jumlah_diskon, tanggal_kedaluwarsa, tipe_pengguna):
        self.kode = kode
        self.jumlah_diskon = jumlah_diskon
        self.tanggal_kedaluwarsa = tanggal_kedaluwarsa
        self.tipe_pengguna = tipe_pengguna

vouchers_aktif = []

def buat_voucher_otomatis(jumlah_diskon, tipe_pengguna, masa_berlaku_hari=30):
    kode_voucher = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(8))
    tanggal_kedaluwarsa = datetime.now() + timedelta(days=masa_berlaku_hari)
    voucher_baru = Voucher(kode_voucher, jumlah_diskon, tanggal_kedaluwarsa, tipe_pengguna)
    vouchers_aktif.append(voucher_baru)
    return voucher_baru.kode

def cek_validitas_voucher(kode, peran):
    for voucher in vouchers_aktif:
        if voucher.kode == kode and datetime.now() < voucher.tanggal_kedaluwarsa and voucher.tipe_pengguna == peran:
            vouchers_aktif.remove(voucher)
            return voucher
    return None

def login():
    for percobaan in range(3):
        username = input("Masukkan nama pengguna: ")
        password = input("Masukkan kata sandi: ")
        if username in akun:
            if akun[username]["terkunci"]:
                print("Akun Anda terkunci! Hubungi admin.")
                return None
            if akun[username]["password"] == password:
                print(f"Login berhasil! Selamat datang di toko PUBG Mobile, {username}.")
                return akun[username]["role"], username
            else:
                print("Kata sandi salah!")
        else:
            print("Nama pengguna tidak ditemukan!")
    
    akun[username]["terkunci"] = True
    print("Akun Anda terkunci setelah 3 kali percobaan salah!")
    return None

def tampilkan_barang(peran):
    jam_sekarang = time.localtime().tm_hour
    if 6 <= jam_sekarang < 12:
        periode = "pagi"
    elif 12 <= jam_sekarang < 18:
        periode = "siang"
    else:
        periode = "malam"

    tabel = PrettyTable()
    tabel.field_names = ["No", "Kategori", "Barang", "Harga (UC)"]

    index = 1
    for kategori, daftar_barang in skin_barang[periode].items():
        for nama, harga in daftar_barang:
            tabel.add_row([index, kategori.capitalize(), nama, harga])
            index += 1

    if peran == 'VIP':
        for kategori, daftar_barang in skin_barang["khusus_vip"].items():
            for nama, harga in daftar_barang:
                tabel.add_row([index, f"{kategori.capitalize()} Khusus VIP", nama, harga])
                index += 1

    print(f"\nDaftar barang tersedia ({periode}):")
    print(tabel)
    return periode

def cetak_invoice(nama_pengguna, daftar_pembelian, saldo_awal, saldo_akhir):
    tabel = PrettyTable()
    tabel.field_names = ["Nama Barang", "Harga (UC)"]
    total_harga = 0
    for barang, harga in daftar_pembelian:
        tabel.add_row([barang, harga])
        total_harga += harga

    print("\n--- INVOICE TRANSAKSI ---")
    print(f"Nama Pengguna: {nama_pengguna}")
    print(f"Saldo Awal: {saldo_awal} UC")
    print(f"Saldo Akhir: {saldo_akhir} UC")
    print("Rincian Pembelian:")
    print(tabel)
    print(f"Total Pengeluaran: {total_harga} UC")
    print("-------------------------")

def transaksi(peran, periode, saldo_uc, nama_pengguna):
    saldo_awal = saldo_uc
    daftar_pembelian = []

    while True:
        print(f"\nSaldo Anda: {saldo_uc} UC")
        tampilkan_barang(peran)

        try:
            pilihan_barang = int(input("Pilih nomor barang yang ingin dibeli: ")) - 1
        except ValueError:
            print("Masukkan nomor yang valid!")
            continue

        semua_barang = []

        for daftar_barang in skin_barang[periode].values():
            semua_barang.extend(daftar_barang)

        if peran == 'VIP':
            for daftar_barang in skin_barang["khusus_vip"].values():
                semua_barang.extend(daftar_barang)

        if pilihan_barang < 0 or pilihan_barang >= len(semua_barang):
            print("Pilihan tidak valid.")
            continue

        barang_dipilih = semua_barang[pilihan_barang]
        harga = barang_dipilih[1]

        kode_voucher = input("Masukkan kode voucher untuk diskon (atau tekan Enter untuk melewati): ")
        diskon = 0
        if kode_voucher:
            voucher_valid = cek_validitas_voucher(kode_voucher, peran)
            if voucher_valid:
                diskon = voucher_valid.jumlah_diskon
                harga = max(0, harga - diskon)
                print(f"Voucher digunakan! Diskon: {diskon} UC.")
            else:
                print("Kode voucher tidak valid, sudah digunakan, atau tidak cocok dengan tipe pengguna!")

        if harga > saldo_uc:
            print("Saldo tidak mencukupi untuk membeli item ini.")
            print("\nApakah Anda ingin melakukan top-up UC? (y/n): ")
            jawaban_topup = input().strip().lower()
            if jawaban_topup == 'y':
                saldo_uc = top_up_uc(nama_pengguna, saldo_uc)
                continue 
            else:
                print("Kembali ke menu utama.")
                break

        saldo_uc -= harga
        daftar_pembelian.append((barang_dipilih[0], harga))
        print(f"Pembelian sukses! Anda membeli {barang_dipilih[0]} seharga {harga} UC. Sisa saldo: {saldo_uc} UC")

        lagi = input("Apakah Anda ingin membeli item lain? (y/n): ").strip().lower()
        if lagi != 'y':
            break

    if daftar_pembelian:
        cetak_invoice(nama_pengguna, daftar_pembelian, saldo_awal, saldo_uc)
    return saldo_uc, daftar_pembelian


def cek_saldo(nama_pengguna, saldo_uc):
    print(f"\nSaldo saat ini:")
    print(f"- E-Money: Rp{saldo_emoney[nama_pengguna]:,}")
    print(f"- UC: {saldo_uc} UC")

def top_up_emoney(nama_pengguna):
    try:
        jumlah = int(input("Masukkan jumlah top-up e-money (Rp): "))
        if jumlah <= 0:
            print("Jumlah tidak valid!")
            return
        saldo_emoney[nama_pengguna] += jumlah
        print(f"Top-up e-money berhasil! Saldo e-money sekarang: Rp{saldo_emoney[nama_pengguna]:,}")
    except ValueError:
        print("Input tidak valid!")

def top_up_uc(nama_pengguna, saldo_uc):
    try:
        print("\nPaket Top-up UC:")
        tabel = PrettyTable()
        tabel.field_names = ["Paket", "Jumlah UC", "Harga (Rp)"]
        tabel.add_row(["1", "100 UC", "Rp10.000"])
        tabel.add_row(["2", "300 UC", "Rp30.000"])
        tabel.add_row(["3", "1000 UC", "Rp100.000"])
        tabel.add_row(["4", "2000 UC", "Rp200.000"])
        print(tabel)

        pilihan = input("Pilih paket (1-4): ")
        paket_uc = {
            '1': (100, 10000),
            '2': (300, 30000),
            '3': (1000, 100000),
            '4': (2000, 200000),
        }

        if pilihan not in paket_uc:
            print("Pilihan tidak valid!")
            return saldo_uc

        uc, harga = paket_uc[pilihan]
        if saldo_emoney[nama_pengguna] < harga:
            print("Saldo e-money tidak mencukupi!")
            return saldo_uc

        saldo_emoney[nama_pengguna] -= harga
        saldo_uc += uc
        print(f"Top-up UC berhasil! Anda mendapatkan {uc} UC. Saldo UC sekarang: {saldo_uc} UC.")
        return saldo_uc
    except ValueError:
        print("Input tidak valid!")
        return saldo_uc

def main():
    kode_voucher_member = buat_voucher_otomatis(200, "Member")
    kode_voucher_vip = buat_voucher_otomatis(500, "VIP")
    print(f"Voucher Member: {kode_voucher_member} (Diskon 200 UC)")
    print(f"Voucher VIP: {kode_voucher_vip} (Diskon 500 UC)")

    while True:
        print("Selamat datang di Toko PUBG Mobile!")
        hasil_login = login()
        if not hasil_login:
            continue

        peran, nama_pengguna = hasil_login
        saldo_uc = 5000  
        saldo_emoney_awal = saldo_emoney[nama_pengguna]  

        print(f"\nSaldo awal Anda:")
        print(f"- E-Money: Rp{saldo_emoney_awal:,}")
        print(f"- UC: {saldo_uc} UC\n")

        while True:
            print("\nMenu:")
            print("1. Lihat barang tersedia")
            print("2. Lakukan transaksi")
            print("3. Cek saldo e-money dan UC")
            print("4. Top-up e-money")
            print("5. Top-up UC")
            print("6. Keluar")
            pilihan = input("Pilih menu: ")

            if pilihan == '1':
                periode = tampilkan_barang(peran)
            elif pilihan == '2':
                if 'periode' not in locals():
                    print("Lihat daftar barang terlebih dahulu!")
                    continue
                saldo_uc, item_dibeli = transaksi(peran, periode, saldo_uc, nama_pengguna)
            elif pilihan == '3':
                cek_saldo(nama_pengguna, saldo_uc)
            elif pilihan == '4':
                top_up_emoney(nama_pengguna)
            elif pilihan == '5':
                saldo_uc = top_up_uc(nama_pengguna, saldo_uc)
            elif pilihan == '6':
                print("Terima kasih telah menggunakan Toko PUBG Mobile!")
                break
            else:
                print("Pilihan tidak valid!")

if __name__ == "__main__":
    main()
