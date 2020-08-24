#!/usr/bin/env python

import socket

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.16", 4444))

connection.send("\n[+] Connection established. \n")

connection.close()
