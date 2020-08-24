#!/usr/bin/env python

import socket

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #allows socket to be reused in case connection drops

listener.bind(("10.0.2.4", 4444))
listener.listen(0) #backlog for how many connections to allow before stopping
print("[+] Waiting for incoming connections. . .\n")
listener.accept()
print("[+] Connection established!\n")
