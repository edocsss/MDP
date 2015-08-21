#!/usr/bin/python3

import threading
import queue
import time
from SerialComm import *
from WifiComm import *

# Constants
INTER_READ_DELAY = 0.2
INTER_WRITE_DELAY = 0.2

class CommController:
    bt = None
    wifi = None
    ser = None

    # Message queue -> whenever the queue is not empty, send it to the correct device
    # Message queue is updated when RPi reads something from whichever communication link
    btQueue = queue.Queue()
    wifiQueue = queue.Queue()
    serQueue = queue.Queue()

    def __init__(self):
        # Init bt + wifi
        # self.wifi = WifiComm("IP_ADDRESS", 7777)
        
        # Change serial port when using with Raspberry Pi
        self.ser = SerialComm("/dev/ttyACM0", 9600)
        
    def serialRead(self):
        while True:
            # Data is None if there is nothing being read (empty string)
            print("Before data read!")
            data = self.ser.read()

            if data != None and len(data) > 0:
                # Do data processing here
                # Determine the targeted device and send it there

                # if data begins with 0:
                #   wifiQueue.put(data)
                # elif data begins with 1:
                #   btQueue.put(data)
                
                
                # For testing purpose -> see that the Arduino should read "A"
                self.serQueue.put("A")

            # Give time between reading
            time.sleep(INTER_READ_DELAY)

    def serialWrite(self):
        while True:
            if not self.serQueue.empty():
                # Blocking "get" -> block until an item is available
                data = self.serQueue.get()
                self.ser.write(data)
                print("Serial data writing is done!")

            # Give time between writing
            time.sleep(INTER_WRITE_DELAY)

    def wifiRead(self):
        while True:
            data = self.wifi.read()

            if data != None:
                # Do data processing here

                print("DATA READ WIFI: " + str(data))
                self.wifiQueue.put("W")

            # Give time between reading
            time.sleep(INTER_READ_DELAY)

    def wifiWrite(self):
        while True:
            if not self.wifiQueue.empty():
                # Blocking "get" -> block until an item is available
                data = self.wifiQueue.get()
                self.wifi.write(data)
                print("Serial data writing is done!")

            # Give time between writing
            time.sleep(INTER_WRITE_DELAY)

    def initialize(self):
        self.ser.start()
        # self.bt.start()
        # self.wifi.start()

        # Checking whether Android, Arduino, and Laptop are all ready
        # PING Serial
        #self.ser.write("R")
        #while self.ser.read() != "00000000":
        #    time.sleep(0.3)

        # PING Android

        # PING Laptop
        #self.wifi.write("R")
        #while self.wifi.read() != "00000010":
        #    time.sleep(0.3)
        
        print("RPi is ready for receiving and sending data!")
        print("Initialize threads!")
        
        # Thread initialization
        threading.Thread(target=self.serialRead).start()
        threading.Thread(target=self.serialWrite).start()

        #threading.thread(target=self.wifiRead).start()
        #threading.thread(target=self.wifiWrite).start()

commController = CommController()
commController.initialize()
