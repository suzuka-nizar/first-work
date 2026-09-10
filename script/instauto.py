from instagrapi import Client
import os
import pyfiglet
import schedule
import time

header = pyfiglet.figlet_format("INSTAUTO", font="standard")
print(header)

user_name = input("Masukkan Username Anda:\n")
file_sesi = f"session_{user_name}.json"
CL = Client()

#otomatisasi login
if os.path.exists(file_sesi):
  print("Mencoba login menggunakan file sesi...")
  try:
    CL.load_settings(file_sesi)
    CL.login(user_name, "")
    CL.get_timeline_feed()
    print("[+]File sesi valid! bot siap digunakan.")
  except Exception:
    print("[-]File sesi telah kadaluwarsa! menghapus file sesi...")
    os.remove(file_sesi)
    print("-" * 50 + ">")

#file sesi tidak ada/dihapus karena kadaluwarsa
if not os.path.exists(file_sesi):
  print("File sesi tidak ditemukan, silahkan login terlebih dahulu.")
  pass_word = input(f"Masukkan password @{user_name} untuk login:\n")
  print("sedang melakukan login ke server instagram...")
  try:
    login_sukses = CL.login(user_name, pass_word)
    if login_sukses:
      print("⟨✓⟩LOGIN SUKSES!\nmenyimpan sesi baru ke file json.")
      CL.dump_settings(file_sesi)
      print(f"Sesi berhasil disimpan: {file_sesi}")
  except Exception as e:
    print(f"⟨x⟩LOGIN GAGAL!\nrespon server {e}")
    exit()
print("-" * 50 + ">")

#media yang akan diunggah
file_foto = input("Masukkan nama file foto:\n")
caption = input("Masukkan caption untuk postingan:\n")
if not os.path.exists(file_foto):
  print(f"[!]ERROR! file foto{file_foto} tidak ditemukan.")
  exit()

#jadwal upload & fungsi penjadwalan
waktu_upload = input("Sesuaikan pukul berapa akan mengunggah:\n")
def unggahan():
  print("waktu mengunggah terpenuhi!\nsedang mengunggah postingan ke instagram...")
#rincian postingan yang berhasil diunggah
  try:
    media_terunggah = CL.photo_upload(file_foto, caption)
    print("=" * 50)
    print("Postingan berhasil diunggah!")
    print(f"ID postingan : {media_terunggah}.id")
    print(f"URL postingan : https://instagram.com{media_terunggah.code}/")
    print("=" * 50)

    print("TUGAS SELESAI.\nbot diberhentikan...")
    os._exit(0)
    
  except Exception as e:
    print(f"Postingan gagal diunggah!\nrespon server: {e}")
    print("mencoba mengunggah kembali atau periksa koneksi anda")

#eksekusi bot sesuai waktu
schedule.every().day.at(waktu_upload).do(unggahan)
print(f"[#] Bot akan dijalankan pada pukul {waktu_upload} untuk mengunggah media.\nharap jangan tutup program ini.")

#loop pengecek waktu
while True:
  schedule.run_pending()
  time.sleep(1)