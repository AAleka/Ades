#!/usr/bin/python

import pystray
import time
import threading
import webbrowser
import os
import win32gui, win32con
import PIL.Image
import signal

from http.server import HTTPServer, SimpleHTTPRequestHandler
from glob import glob


def get_images():
    wallpapers_path = './src/wallpapers'
    wallpapers = glob(wallpapers_path + '/*')

    with open('./src/configs/images.txt', 'w') as file:
        for i, wallpaper in enumerate(wallpapers):
            file.write(wallpaper.replace('\\', '/') + ';')


def start_server():
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


def on_clicked(systray, item):
    if str(item) == "Open":
        url = f"http://{ip}:{port}/main.html"
        webbrowser.open(url)

    if str(item) == 'Exit':
        systray.stop()
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    get_images()

    ip = "127.0.0.1"
    port = 8000
    url = f"http://{ip}:{port}/main.html"

    # the_program_to_hide = win32gui.GetForegroundWindow()
    # win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

    http_thread = threading.Thread(target=start_server)
    http_thread.start()

    webbrowser.open(url)

    image = PIL.Image.open('./src/icon.ico')
    icon = pystray.Icon('Ades', image, menu=pystray.Menu(
        pystray.MenuItem("Open", on_clicked),
        pystray.MenuItem("Exit", on_clicked)
    ))
    icon.run()

    while True:
        time.sleep(0.0000001)
