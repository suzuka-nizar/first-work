import curses
import random
import time

#pengaturan game
fps = 15
lebar_jalan = 35
offset_y_player = 12
spawn_interval = 29

#bentuk mobil
mobil_player = [
   " ︽",
   "∣||∣",
   "〘〙",
   "∣==∣",
   " ︺ "
]

mobil_lawan = [
  " ︹",
  "∣==∣",
  " ∏∏",
  "∣==∣",
  "‾‾‾‾"
]

#fungsi utama
def game(stdscr):
  curses.curs_set(0)
  stdscr.nodelay(True)
  stdscr.timeout(0)

  #ukuran terminal/layar
  tinggi, lebar = stdscr.getmaxyx()
  jalan_kiri = (lebar - lebar_jalan) // 2
  jalan_kanan = jalan_kiri + lebar_jalan
  player_y = tinggi - offset_y_player
  player_x = lebar // 2

  #data game
  musuh = []
  offset_jalan = 0
  frame = 0
  skor = 0
  game_running = True

  #game loop
  while game_running:
    start_time = time.time()

    #update ukuran terminal/layar
    lebar, tinggi = stdscr.getmaxyx()
    jalan_kiri = (lebar - lebar_jalan) // 2
    jalan_kanan = jalan_kiri + lebar_jalan
    player_y = tinggi - offset_y_player

    #input keyboard, kiri & kanan
    key = stdscr.getch()
    if key == curses.KEY_LEFT:
      player_x -= 2
    elif key == curses.KEY_RIGHT:
      player_x += 2
    elif key == ord("q"):
      break

    #mobil tetap di dalam jalan
    minimum_x = jalan_kiri + 3
    maximum_x = jalan_kanan - 7 

    if player_x < minimum_x:
      player_x = minimum_x
    if player_x > maximum_x:
      player_x = maximum_x 
      
    #animasi garis jalan
    offset_jalan += 1
    if offset_jalan >= 4:
      offset_jalan = 0

    #spawn mobil musuh
    frame += 1
    if frame % spawn_interval == 0:
      enemy_x = random.randrange(
        jalan_kiri + 2,
        jalan_kanan - 6,
        2
      )
      enemy = {
        "x": enemy_x,
        "y": 1
      }
      musuh.append(enemy)

    #gerak mobil musuh
    for enemy in musuh:
      enemy["y"] += 1

    musuh = [
      enemy
      for enemy in musuh
      if enemy["y"] < tinggi
    ]

    #deteksi musuh
    for enemy in musuh:
      enemy_x = enemy["x"]
      enemy_y = enemy["y"]
      
      #hitbox
      if (
        abs(enemy_x - player_x) < 5
        and
        abs(enemy_y - player_y) < 3
      ):
        game_running = False


      skor += 1
       
      stdscr.erase() 

    #info game
    info = f"Skor: {skor}   ← →: kontrol   Q: quit"
    try:
      stdscr.addstr(
        0,
        max(0, (lebar - len(info)) // 2),
        info
      )
    except curses.error:
      pass

    #pembatas jalan
    for y in range(1, tinggi):
      try:
        stdscr.addch(
          y,
          jalan_kiri,
          "Ξ"
        )
        stdscr.addch(
          y,
          jalan_kanan,
          "Ξ"
        )
      except curses.error:
        pass

    #garis jalan bergerak
    jalan_tengah = (jalan_kiri + jalan_kanan) // 2
    for y in range(1, tinggi):
      
      if (y + offset_jalan) % 7 < 2:
        try:
          stdscr.addch(
            y,
            jalan_tengah,
            "∣"
          )
        except curses.error:
          pass

    #mobil musuh
    for enemy in musuh:
      enemy_x = enemy["x"]
      enemy_y = enemy["y"]

      for i, line in enumerate(mobil_lawan):
        try:
          stdscr.addstr(
            enemy_y + i,
            enemy_x,
            line
          )
        except curses.error:
          pass

    #mobil player
    for i, line in enumerate(mobil_player):
      try:
        stdscr.addstr(
          player_y + i,
          player_x,
          line
        )
      except curses.error:
        pass

    #update layar
    stdscr.refresh()

    #kontrol fps
    elapsed = time.time() - start_time
    delay = (1 / fps) - elapsed
    if delay > 0:
      time.sleep(delay)

  #game over
  stdscr.nodelay(False)
  stdscr.erase()
  message = "GAME OVER!"
  score_message = f"SKOR AKHIR: {skor}"
  restart_message = "Tekan R untuk main lagi atau Q untuk keluar"

  try:
    stdscr.addstr(
      tinggi // 2 - 2,
      (lebar - len(message)) // 2,
      message
    )
    stdscr.addstr(
      tinggi // 2,
      (lebar - len(score_message)) // 2,
      score_message
    )
    stdscr.addstr(
      tinggi // 2 + 2,
      (lebar - len(restart_message)),
      restart_message
    )
  except curses.error:
    pass

  stdscr.refresh()

  while True:
    key = stdscr.getch()
    if key in [ord("q"), ord("Q")]:
      break
    elif key in [ord("r"), ord("R")]:  
      game(stdscr)
      break


curses.wrapper(game)