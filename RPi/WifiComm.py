import socket
import threading
import atexit

class WifiComm:
    soc = None
    host = None
    port = None
    connection = None
    
    BUFFER_LENGTH_MAX = 1024
    MESSAGE_LENGTH = 8

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc.bind((self.host, self.port))
            self.soc.listen(1)
        except Exception as e:
            print("Socket error!")
            print(e)

        print("Waiting for Wi-Fi connection...")
        try:
            self.connection, self.pcAddress = self.soc.accept()
        except Exception as e:
            print("Socket cannot accept a new connection!")
            print("Error message: " + e)

        print("Connected to laptop with IP Address: " + self.pcAddress)

    def end(self):
        print("Closing socket!")
        self.connection.close()
        self.soc.close()
        print("Socket closed!")
        self.soc = None
        
    def write(self, data):
        print("Sending data via Wi-Fi: " + str(data))
        self.connection.sendall(data.encode(encoding="utf8"))
        
    def read(self):
        data = ""
        recorded = 0
        
        while recorded < MESSAGE_LENGTH:
            data += self.connection.recv(min(MESSAGE_LENGTH - recorded, BUFFER_LENGTH_MAX))
            recorded = len(data)     

        if len(data) == MESSAGE_LENGTH:
            return data
        else:
            return None
