import serial
import thread
import socket
import time
import json
from Queue import Queue

global storage_queue, current_mode, direction
current_mode = ""
direction = ""

class ArduinoApi():
    def __init__(self, passed_queue, port='/dev/ttyACM0', data_rate=115200, timeout=0.05):     # Try 0.3, prevents stopsense hanging. Ask JS
        global storage_queue
        storage_queue = passed_queue
        self.ser = None
        self.connected = False
        self.name = "ArduinoApi"
        self.client = "Arduino"
        self._init_ard_com(port, data_rate, timeout)
        self.commands_outgoing = Queue()
        self.map_manager = None
        self.is_idle = True
        self.current_command = None
        self.receive_sensor = False
        # self.temp_output_counter = 0
        # self.temp_output = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]

    def trace(self, message):
        print "[" + self.name + "] " + message

    def _init_ard_com(self, port, data_rate, timeout):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = data_rate
        self.ser.timeout = timeout
        self.ser.open()  # TODO uncomment to make it work
        self.connected = True
        self.trace("Connected to " + self.client)

    def send(self, data):
        self.ser.write(data.encode())
        self.trace("======> Sent data(" + str(data) + ") to " + self.client)
        #time.sleep(0.05)

    def _read(self):
        while True:  # keep fetching until found
            data = self.ser.readline()

            if data is not None and data is not "":
                print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@" + str(type(data)) + ' | ' + data
                # self.temp_output[self.temp_output_counter] = data
                # self.temp_output_counter += 1
                # print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(self.temp_output)
                self.trace("Received data from " + self.client)

                global storage_queue

                # if (data is None) or (len(data) == 0):
                #     continue

                if "2" in data[:1]:
                    #self.commands_outgoing.queue.clear()
                    #self.current_command = None
                        storage_queue.put(['arduino','pc', data[1:].rstrip()])
                    #force overwrite map

                if "1" in data[:1]:
                    #self.is_idle = True
                        storage_queue.put(['arduino', 'android', data[1:].rstrip()])

                if "4" in data[:1]:
                        storage_queue.put(['arduino', 'pc', data[1:].rstrip()])
                        storage_queue.put(['arduino', 'android', data[1:].rstrip()])
                       # storage_queue.put(['arduino','map_mgr', '{"instruction":'+str(self.current_command)+'}']) #update the current position (acknowledgement successful command)
                        # storage_queue.put(['arduino_api','map_mgr', {"status": str(self.current_mode)}]) # Pass status to Map Manager to update Tablet
                       # self.current_command = None
                        global current_mode
                        if(self.commands_outgoing.empty() and current_mode == "Fastest Path Mode"):
                            storage_queue.put(['arduino_api', 'android', '{"status": "Goal Reached"}'])

                        elif(self.commands_outgoing.empty() and current_mode ==  "Going home"):
                            storage_queue.put(['arduino_api', 'android', '{"status": "Exploration Completed"}'])
                            storage_queue.put(['arduino_api', 'arduino', 'end'])
                        # else:
                        #     storage_queue.put(['arduino_api', 'android', '{"status":"' + self.current_mode + ' - ' + self.instruction_str + '"}'])

                    # time.sleep(1)

                if "," in data:
                    # self.receive_sensor = True
                    if self.commands_outgoing.empty() and self.current_command is None:
                    # if self.commands_outgoing.empty():
                        storage_queue.put(['arduino','map_mgr', data]) #update map
                        global current_mode


            time.sleep(0.05)

    def _print_outgoing_command(self):
        while not self.commands_outgoing.empty():
            try:
                elem = self.commands_outgoing.get()
                print elem
            except:
                break

    def setup(self, map_manager):
        self.map_manager = map_manager

    def is_command_empty(self):
        return self.commands_outgoing.empty()

    def put(self, input_str):
        # print "===========================> " + passed_str
        if "instruction" in input_str:
            instructions = input_str["instruction"]
            if instructions:
                self.trace("Received instuction(s) from the main. Putting them to the queue")
            for ins in instructions:
                self.commands_outgoing.put(ins)

        global current_mode
        if "status" in input_str:
            current_mode = input_str["status"]

        # if "direction" in input_str:
        #     self.instruction_str = input_str["direction"]

    def set_idle(self, stat):
        self.is_idle = stat

from threading import Thread


class ArduinoReadThread():
    def __init__(self, arduino_api):
        #super(ArduinoReadThread, self).__init__()
        self.arduino_api = arduino_api

    def run(self):
        self.arduino_api._read()

class ArduinoCommandThread():
    def __init__(self, arduino_api):
        #super(ArduinoCommandThread, self).__init__()
        self.arduino_api = arduino_api

        # text_file = open("Arduino_Movement_Command.txt", "w")
        # text_file.write("")
        # text_file.close()
        # self.output_text_counter = 2

    def run(self):
        while True:
            if self.arduino_api.is_command_empty():
                time.sleep(0.05)
                continue
            else:
                # if self.arduino_api.is_idle and self.arduino_api.receive_sensor:
                if self.arduino_api.is_idle:
                    self.arduino_api.current_command = self.arduino_api.commands_outgoing.get()
                    cur_com = self.arduino_api.current_command
                    command_str = ""
                    global direction, current_mode
                    if cur_com[0]==0.0: # move forward
                        if cur_com[1]==1.0:
                            command_str = "w"
                            direction = "Moving Forward"
                        elif cur_com[1]==-1.0:
                            command_str = "s"
                            direction = "Reversing"
                        else:
                            if cur_com[1]>0:
                                command_str = "w"+(str(cur_com[1]).split("."))[0]
                                direction = "Moving Forward"
                            else:
                                # cur_com[1] *= -1
                                command_str = "s"+(str(cur_com[1]*(-1)).split("."))[0]
                                direction = "Reversing"
                    if cur_com[0]==1.0: # turning
                        if cur_com[1]>0.0: # turn left
                            command_str = "a"
                            direction = "Turning Left"
                        else: # turn right
                            command_str = "d"
                            direction = "Turning Right"
                    if cur_com[0]==3.0: # home reached dummy command from PC
                        storage_queue.put(['arduino_api', 'android', '{"status": "Exploration Completed"}'])
                        storage_queue.put(['arduino_api', 'arduino', 'end'])

                    if(command_str!=""):
                        print "[ArduinoApi] command: " + command_str
                        storage_queue.put(['arduino', 'android', '{"status": "'+str(current_mode)+': '+str(direction)+'"}']) # Send status to Tablet
                        self.arduino_api.send(command_str)

                        output_text = "Movement Command = " + command_str + "\n"
                        storage_queue.put(['arduino', 'log', output_text])

                        # global storage_queue
                        # storage_queue.put(['arduino'])
                        # ['android', 'arduino', message]
                        # self.arduino_api.receive_sensor = False
                        self.arduino_api.is_idle = False
                else:
                    time.sleep(0.05)
                    continue

        # while True:

    # if(self.arduino_api.is_command_empty()):
    # time.sleep(0.05)
    # continue
    # else:
    # if(self.ack):
    # next_instruct = self.arduino_api.commands_outgoing.get()
    # next_instruct_json_str = json.dumps({"instruction":next_instruct})
    # self.arduino_api.send(next_instruct_json_str)
    # else:
    # time.sleep(0.05)
    # continue

