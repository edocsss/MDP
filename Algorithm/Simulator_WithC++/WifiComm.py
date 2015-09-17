import socket
import time

__author__ = 'ECAND_000'

class WifiComm:
    soc = None
    host = None
    port = None
    INTER_WRITING_DELAY = 0.1

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Connecting to RPi...")
            self.soc.connect((self.host, self.port))
            print("Connected to RPi!")

        except Exception as e:
            print("Laptop socket error!")
            print("Error: " + e)

    def end(self):
        print("Closing socket...")
        self.soc.close()
        print("Laptop Socket closed!")
        self.soc = None

    def write(self, data):
        print("Sending data from Laptop to RPi: " + str(data))

        try:
            # Assume that the terminator is "\n" --> so that the Arduino / Android / RPi knows when to stop reading
            self.soc.sendall((data + "\n").encode())
            time.sleep(self.INTER_WRITING_DELAY)

        except socket.error as e:
            print("Connection lost during writing!")
            print(e)

            print("Reconnecting to the socket...")
            self.end()
            self.start()

            # In case there is a disconnection, the RPi will go into socket.error Exception too
            # In that Exception handler, it should discard whatever has been read up to that point in time
            # Laptop will resend the whole data
            self.write(data)

    def read(self):
        data = ""
        print("Laptop is waiting for an incoming message...")
        c = ""

        while c != '\n':
            # This is a blocking READ operation
            # USE BLOCKING SINCE WE NEED TO READ THE WHOLE SENSOR READING BEFORE PROCEEDING WITH THE ALGORITHM EXECUTION
            try:
                c = self.soc.recv(1).decode()
                data += c

            except socket.error as e:
                print("Connection lost during reading!")
                print(e)

                print("Reconnecting to the socket...")
                self.end()
                self.start()

                # In case there is a disconnection, the RPi will go into socket.error Exception too
                # In that Exception handler, it should resend the data again
                data = c = ""

        # Remove any trailing newline character
        data = data.strip()

        if len(data) > 0:
            return data
        else:
            return None

