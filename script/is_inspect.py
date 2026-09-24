import requests

def cek_header(url):
  respon = requests.get(url, timeout=5)
  # mengirim request http get
  try:
    print(f"[+] Status code : {respon.status_code}")
    print("||[HTTP HEADER]||")
    # loop seluruh header yang dikirim server
    for header, value in respon.headers.items():
      print(f"{header} : {value}")
      # kebocoran versi server
      if header.lower() == 'server':
        print(f"server version : {value}")

  except requests.exceptions.RequestException as e:
    print(f"[-] error while connecting to {url} : {e}")

if __name__ == "__main__":
  url_target = input("[+] ENTER TARGET URL: ")
  cek_header(url_target)
