# ============================================
# PROGRAM STEGANOGRAFI (Metode LSB) - Standalone
# Nama : Nikita Putri Prabowo
# NPM  : 140810230010
# Tugas 5 - Praktikum Kriptografi (FINAL)
# ============================================

from PIL import Image
import numpy as np
import os
import time

# -------------------------------------------
# Fungsi bantu
# -------------------------------------------
def to_bin(data):
    """Ubah data ke representasi biner"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int):
        return format(data, "08b")
    else:
        raise TypeError("Tipe data tidak didukung.")

# -------------------------------------------
# Fungsi Encode
# -------------------------------------------
def encode_image(image_path, secret_message, output_path):
    """Menyembunyikan pesan rahasia ke dalam gambar (tanpa overflow)"""
    print("⏳ Membuka gambar...")
    image = Image.open(image_path).convert("RGB")
    
    # Resize otomatis biar proses cepat
    max_size = (400, 400)
    if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
        print(f"⚙️  Gambar terlalu besar ({image.size}), sedang diperkecil...")
        image = image.resize(max_size)
        print(f"✅ Gambar diperkecil menjadi {image.size}")

    arr = np.array(image, dtype=np.uint8)
    secret_message += "###"  # penanda akhir pesan
    binary_msg = ''.join(format(ord(i), '08b') for i in secret_message)

    flat = arr.flatten()
    data_len = len(binary_msg)

    if data_len > len(flat):
        print("❌ Pesan terlalu panjang untuk gambar ini.")
        return False

    print("🔍 Menyisipkan pesan ke dalam pixel...")
    for i in range(data_len):
        flat[i] = flat[i] - (flat[i] % 2) + int(binary_msg[i])

    arr2 = flat.reshape(arr.shape)
    encoded_img = Image.fromarray(arr2)

    print("💾 Menyimpan gambar hasil...")
    encoded_img.save(output_path)
    encoded_img.close()
    image.close()
    print(f"✅ Pesan berhasil disembunyikan di {output_path}")
    return True

# -------------------------------------------
# Fungsi Decode
# -------------------------------------------
def decode_image(stego_path):
    """Mengambil pesan dari gambar stego"""
    print("⏳ Membuka gambar stego...")
    image = Image.open(stego_path).convert("RGB")
    arr = np.array(image, dtype=np.uint8)
    flat = arr.flatten()

    binary_data = ''.join([str(pixel % 2) for pixel in flat])
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    
    decoded = ""
    for byte in all_bytes:
        decoded += chr(int(byte, 2))
        if decoded[-3:] == "###":
            break
    image.close()
    return decoded[:-3]

# -------------------------------------------
# MENU UTAMA
# -------------------------------------------
while True:
    print("\n=== PROGRAM STEGANOGRAFI (Metode LSB) ===")
    print("1. Encode (Sembunyikan Pesan)")
    print("2. Decode (Ambil Pesan)")
    print("3. Keluar dari Program")
    pilihan = input("Pilih menu (1/2/3): ")

    if pilihan == "1":
        img_name = input("Masukkan path gambar cover (misal: cover.png): ")
        if not os.path.exists(img_name):
            print("⚠️ File tidak ditemukan. Coba lagi.")
            continue

        pesan = input("Masukkan pesan rahasia: ")
        output_name = input("Masukkan nama file output (misal: stego_image.bmp): ")

        start = time.time()
        berhasil = encode_image(img_name, pesan, output_name)
        end = time.time()
        print(f"⏱️ Waktu proses encode: {end - start:.2f} detik")

        if berhasil:
            print(f"📦 File tersimpan sebagai: {output_name}")

    elif pilihan == "2":
        stego_name = input("Masukkan path gambar stego: ")
        if not os.path.exists(stego_name):
            print("⚠️ File tidak ditemukan. Coba lagi.")
            continue

        start = time.time()
        hasil = decode_image(stego_name)
        end = time.time()

        print("\n🕵️‍♀️ Pesan yang tersembunyi:")
        print("💬", hasil)
        print(f"⏱️ Waktu proses decode: {end - start:.2f} detik")

    elif pilihan == "3":
        print("👋 Program selesai. Terima kasih, Nikita!")
        break

    else:
        print("⚠️ Pilihan tidak valid. Silakan pilih 1, 2, atau 3.") 
