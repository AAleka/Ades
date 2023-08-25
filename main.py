#!/usr/bin/python

import pystray
import time
import threading
import webbrowser
import os
import win32gui, win32con
import PIL.Image
import signal
import socketserver
import urllib.parse

from http.server import HTTPServer, SimpleHTTPRequestHandler
from glob import glob
from datetime import date


class requestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.find('addTaskButton=true') != -1:
            task = self.path.split('taskText=', 1)[1].split('&', 1)[0]
            if task != '':
                task = urllib.parse.unquote(task.replace('+', ' '))

                with open("./src/configs/tasks.txt", "r") as file:
                    lines = file.readlines()

                task_id = str(int(lines[-1].split('|')[0]) + 1)

                with open("./src/configs/tasks.txt", "a") as file:
                    file.write('\n' + task_id + '|' + task + '|' + str(date.today()) + '|0' + ';')

        elif self.path.find("taskToCheck=") != -1:
            task = urllib.parse.unquote(self.path.replace('+', ' ')).split('\n')[1] + ';'
            with open("./src/configs/tasks.txt", "r") as file:
                lines = file.readlines()

            for i in range(len(lines)):
                lines[i] = lines[i].replace('\n', '')
                if lines[i] == task:
                    lines[i] = '1'.join(lines[i].rsplit('0', 1))

            with open("./src/configs/tasks.txt", "w") as file:
                for i, line in enumerate(lines):
                    file.write(line + ('\n' if i < len(lines)-1 else ''))

        elif self.path.find('addAffirmationButton=true') != -1:
            affirmation = self.path.split('affirmationText=', 1)[1].split('&', 1)[0]
            if affirmation != '':
                affirmation = urllib.parse.unquote(affirmation.replace('+', ' '))

                with open("./src/configs/affirmations.txt", "r") as file:
                    lines = file.readlines()

                affirmation_id = str(int(lines[-1].split('|')[0]) + 1)

                with open("./src/configs/affirmations.txt", "a") as file:
                    file.write('\n' + affirmation_id + '|' + affirmation + '|' + str(date.today()) + ';')

        elif self.path.find("affirmationToCheck=") != -1:
            affirmation = urllib.parse.unquote(self.path.replace('+', ' ')).split('\n')[1] + ';'
            with open("./src/configs/affirmations.txt", "r") as file:
                lines = file.readlines()

            if affirmation in lines:
                lines.remove(affirmation)
            else:
                lines.remove(affirmation + '\n')

            with open("./src/configs/affirmations.txt", "w") as file:
                for i in range(len(lines)):
                    if i < len(lines)-1:
                        file.write(lines[i])
                    else:
                        file.write(lines[i].replace('\n', ''))

        elif self.path.find('addPlanButton=true') != -1:
            plan = self.path.split('planText=', 1)[1].split('&', 1)[0]
            if plan != '':
                plan = urllib.parse.unquote(plan.replace('+', ' '))

                with open("./src/configs/plans.txt", "r") as file:
                    lines = file.readlines()

                plan_id = str(int(lines[-1].split('|')[0]) + 1)

                with open("./src/configs/plans.txt", "a") as file:
                    file.write('\n' + plan_id + '|' + plan + '|' + str(date.today()) + ';')

        elif self.path.find("planToCheck=") != -1:
            plan = urllib.parse.unquote(self.path.replace('+', ' ')).split('\n')[1] + ';'
            with open("./src/configs/plans.txt", "r") as file:
                lines = file.readlines()

            if plan in lines:
                lines.remove(plan)
            else:
                lines.remove(plan + '\n')

            with open("./src/configs/plans.txt", "w") as file:
                for i in range(len(lines)):
                    if i < len(lines)-1:
                        file.write(lines[i])
                    else:
                        file.write(lines[i].replace('\n', ''))

        return super().do_GET()


def get_images():
    wallpapers_path = './src/wallpapers'
    wallpapers = glob(wallpapers_path + '/*')

    with open('./src/configs/images.txt', 'w') as file:
        for i, wallpaper in enumerate(wallpapers):
            file.write(wallpaper.replace('\\', '/') + ';')


def remove_tasks():
    with open('./src/configs/tasks.txt', 'r') as file:
        current_date = str(date.today())
        lines = file.readlines()

    with open('./src/configs/tasks.txt', 'w') as file:
        file.write(lines[0])
        for i in range(1, len(lines)):
            if lines[i].split('|')[2] == current_date:
                file.write(lines[i])


def start_server():
    server_address = (ip, port)
    httpd = socketserver.TCPServer(server_address, requestHandler)
    httpd.serve_forever()


def on_clicked(systray, item):
    if str(item) == "Open":
        link = f"http://{ip}:{port}/main.html"
        webbrowser.open(link)

    if str(item) == 'Exit':
        systray.stop()
        os.kill(os.getpid(), signal.SIGINT)


if __name__ == "__main__":
    get_images()
    remove_tasks()

    ip = "localhost"
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
        time.sleep(0.1)
