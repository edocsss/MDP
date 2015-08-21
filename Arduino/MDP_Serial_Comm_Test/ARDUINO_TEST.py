import serial
import threading
import time

ser = serial.Serial("COM4", 9600)
time.sleep(3)

print("Number of chars in buffer: " + str(ser.inWaiting()))
data = ""
while ser.inWaiting() > 0:
    data += ser.readline() ## Try with ser.read() too
    print(data)

    print("Number of chars in buffer: " + str(ser.inWaiting()))
    time.sleep(0.5)

print("Python is going to write!")
time.sleep(1)
ser.write("TESTING".encode())
print("Python writing is done")
ser.close()
