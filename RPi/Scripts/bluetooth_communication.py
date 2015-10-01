import bluetooth, time 
import re

global server_uuid, server_port, android_queue, phone, nexus, mac_whitelist

school_nexus = "08:60:6E:A5:A4:44" # MAC address of our nexus 7 
mac_whitelist = [school_nexus]

server_uuid = "00001101-0000-1000-8000-00805f9b34fb"
server_port = 5

class BluetoothAPI():
    ''' Bluetooth class to talk to Nexus 7'''
    def __init__(self, storage_queue):
        global server_port, server_uuid, android_queue
        android_queue = storage_queue
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", server_port))
        self.server_sock.listen(1)
        bluetooth.advertise_service(self.server_sock, "MDP Group 7 RPi", server_uuid)
        print "[BluetoothAPI] Accepting bluetooth connection on Port %s..." % server_port

    def accept_connection(self):
        ''' Accept only specific MAC address'''
        while (True):
            self.client_sock, self.client_address = self.server_sock.accept()
            # global test_phone, nexus, test_tablet
            if self.client_address[0] in mac_whitelist:
                print "[BluetoothAPI] Bluetooth connection established on:", self.client_address
                self.receive()
            else:
                print "[BluetoothAPI] Bluetooth connection rejected: MAC Address Not Accepted."
                print "[BluetoothAPI] Awaiting bluetooth connection..."
                self.client_sock.close()
                continue

    def receive(self):
        ''' Receive connection until quit_word is received, then close all connection'''
        # Receive data until key word is received
        while (True):
            received_data = self.client_sock.recv(1024)
            self._message_reader(received_data)
            time.sleep(0.05)

    def send(self, message):
        self.client_sock.send(message)
        print "[BluetoothAPI] Sending data via Bluetooth"
       #time.sleep(0.05)

    def close_all(self):
        '''Close both client and server connection'''
        self.client_sock.close()
        self.server_sock.close()

    def _message_reader(self, message):
        ''' Reads the message received and determine who to send to'''
        global android_queue
        msg_pattern = re.compile("[0-5](.*)[\n]")
        if msg_pattern.match(message):
            if '2' in message[:1]:
                android_queue.put(['android', 'pc', message[1:].rstrip()])
            if '1' in message[:1]:
                android_queue.put(['android', 'arduino', message[1:].rstrip()])
            if '5' in message[:1]:
                android_queue.put(['android', 'arduino', message[1:].rstrip()])
                android_queue.put(['android', 'pc', message[1:].rstrip()])
