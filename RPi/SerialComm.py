import serial
import threading
import atexit

# The send and receive thread will be in the main controller (separation of responsibility)
class SerialComm:
    ser = None
    port = None
    baudRate = None
    
    def __init__(self, port, baudRate):
        self.port = port
        self.baudRate = baudRate
        
    def end(self):
        print("Closing serial port!")
        self.ser.close()
        print("Serial port closed!")
        self.ser = None
        
    def start(self):
        # Set timeout=0 in the constructor for NON-BLOCKING read -> meaning that the read() will return immediately even without data
        # Don't think that we need to do a non-blocking read since SerialRead and SerialWrite are using different thread
        self.ser = serial.Serial(port=self.port, baudrate=self.baudRate)
        self.ser.flushInput()
        self.ser.flushOutput()
        atexit.register(self.end)

    # Data is sent as String
    def write(self, data):
        print("Sending data: " + str(data))
        self.ser.write(data.encode())

    def read(self):
        # The data sent from Arduino must be terminated by EOL -> ASCII 10 & 13
        data = []
        data += self.ser.readline()

        # Data is empty if nothing is read
        if len(data) > 0:
            # Need to convert to char since the data from Arduino is sent as Byte
            result = ""
            for n in data:
                result += chr(n)

            result = result.strip()
            print("Receiving data: " + result)
            return result
        else:
            return None
