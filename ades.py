import sys
import time
import threading
import webbrowser
import win32gui, win32con

from http.server import HTTPServer, SimpleHTTPRequestHandler


def start_server():
    server_address = (ip, port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    httpd.serve_forever()

    
ip = "127.0.0.1"
port = 8000
url = f"http://{ip}:{port}/main.html"

threading.Thread(target=start_server).start()
webbrowser.open_new(url)

the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)