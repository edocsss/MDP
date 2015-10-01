import traceback
import socket
import thread
import time
import sys
import ast
import re

global storage_queue

class PcAPI(object):
    def __init__(self, passed_storage):
        global storage_queue
        storage_queue = passed_storage
        self.SERVER_HOST = '0.0.0.0'
        self.PORT = 5005
        self.BUFFER_SIZE = 20 #Normally 1024
        self.connected = False
        self.myHandle = None  # Interface to send command to self own socket
        self.peerHandle = None  # Interface to send command to peer (client)
        self.name = "PcAPI"
        self.client = "PC"
        self.currentMode = ""
        self.instruction_str = ""

    def trace(self, message):
        print "[" + self.name + "] " + message

    def _when_hungup_handler(self):
        self.trace("Connection lost, closing connection")

    # Server waiting for client
    def wait(self):
        # Blocking wait
        self.myHandle = self._server_wait(self.SERVER_HOST, self.PORT)
        self.peerHandle, addr = self._server_accept(self.myHandle)
        #addr = self.peerHandle
        self.connected = True
        self._start_listener_thread(self.peerHandle, addr)

    def is_connected(self):
        return self.connected

    def send(self, data):
        if (self.peerHandle == None):
            self.trace("Can't send to " + self.client + ", no handle. Hanging up")
            self._hang_up()
        else:
            self.trace("Sending data to " + self.client)
            data += '\n'
            self._send(self.peerHandle, data)
            #time.sleep(0.05)
        #self.trace("Sending data to " + self.client)
        #clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #clientsocket.connect(('192.168.7.155', 5005))
        #self.socket.send(data)
        #self.trace("sent")
        #i = 0
        #while i < len(data):
        #    clientsocket.sendall(data[i])
        #    i += 1
        #time.sleep(0.05)


    def _hang_up(self):
        self._when_hungup_handler()
        self.connected = False
        self._stop_listener_thread()

        if (self.peerHandle != None):
            self._close(self.peerHandle)
            self.peerHandle = None
        if (self.myHandle != None):
            self._close(self.myHandle)
            self.myHandle = None

    def _start_listener_thread(self, handle, addr):
        thread.start_new_thread(self._listener_thread_body, (handle, addr))

    def _stop_listener_thread(self):
        self.trace("Stopping listener thread")
        # TODO
        pass

    def listener_thread_body(self):
        self.myHandle = self._server_wait(self.SERVER_HOST, self.PORT)
        self.peerHandle, addr = self._server_accept(self.myHandle)
        self.connected = True
        msg_pattern = re.compile("[0-5](.*)[\n]")
        while True:
            try:
                data = self._read(self.peerHandle)
                if data == None or len(data) == 0:
                    self.trace("Received data from " + self.client + "is empty")
                    self._hang_up()
                    break
                else:
                    self.trace("Received data from " + self.client)
                    if msg_pattern.match(data):
                        data = data
                    else:
                        time.sleep(0.05)
                        continue

                    global storage_queue
                    try:
#                        msg_dict = ast.literal_eval(data)
                        if "0" in data[:1]: #Send to android
                            storage_queue.put(['pc', 'android', data[1:].rstrip()])
                            continue
                        elif "1" in data[:1]: #Send to Arduino
                            storage_queue.put(['pc', 'arduino', data[1:].rstrip()])
                            continue
                        elif "3" in data[:1]:
                            storage_queue.put(['pc', 'arduino', data[1:].rstrip()])
                            storage_queue.put(['pc', 'android', data[1:].rstrip()])
                            continue
                    except ValueError as e:
                        self.trace("Error in decoding the data - " + str(e.message))

            except:
                # print "Unexpected error:", sys.exc_info()[0]
                print '=================================================================================='
                print '>>> traceback <<<'
                traceback.print_exc()
                print '>>> end of traceback <<<'
                print '=================================================================================='
                # self.trace("something wrong with reading from wifi port")
                # self._hang_up()
                # return
                sys.exit(1)

    def _server_wait(self, addr, port):
        self.trace("Waiting for connection")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #enable to reuse address
        s.bind((addr, port))
        s.listen(1)
        return s

    def get_current_mode(self):
        return self.currentMode

    def _server_accept(self, handle):
        self.trace("Accepting connection")
        handle2, addr = handle.accept()
        self.trace("Connected with:" + str(addr))
        return handle2, addr


    def _close(self, handle):
        handle.close()


    def _send(self, handle, data):
        handle.sendall(data)
        time.sleep(0.05)  # Adjusts thread scheduling and allows the socket I/O to finish FLUSH


    def _read(self, handle):
        self.trace("Waiting for data from PC")
        data = handle.recv(self.BUFFER_SIZE)
        if (data == None):
            raise "lost connection"
        return data

