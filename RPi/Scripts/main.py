import Queue, threading, sys, traceback

from bluetooth_communication import *
from pc_communication import *
from arduino_communication import ArduinoApi, ArduinoReadThread, ArduinoCommandThread


try:
    if __name__ == "__main__":
        # Main Queue
        storage_queue = Queue.Queue(10)

        # Initialise bluetooth connection and thread
        bt = BluetoothAPI(storage_queue)
        bluetooth_thread = threading.Thread(target=bt.accept_connection, args=())
        bluetooth_thread.daemon = True
        bluetooth_thread.start()

        # Initialise PC connection and thread
        pc_api = PcAPI(storage_queue)
        #pc_api.wait()
        pc_thread = threading.Thread(target=pc_api.listener_thread_body, args=())
        pc_thread.daemon = True
        pc_thread.start()

        # Initialise Arduino connection & threads
        ard_api = ArduinoApi(storage_queue)
        #ard_read_thread = ArduinoReadThread(ard_api)
        ard_read_thread_object = ArduinoReadThread(ard_api)
        ard_read_thread = threading.Thread(target=ard_read_thread_object.run, args=())
        ard_read_thread.daemon = True
        ard_read_thread.start()

        #ard_command_thread = ArduinoCommandThread(ard_api)
        ard_command_thread_object = ArduinoCommandThread(ard_api)
        ard_command_thread = threading.Thread(target=ard_command_thread_object.run, args=())
        ard_command_thread.daemon = True
        ard_command_thread.start()

	# Initialise Arduino connection and thread
        #ard = ArduinoAPI(storage_queue)
        #ard_thread = threading.Thread(target=ard.__init__, args=())
        #ard_thread.daemon = True
        #ard_thread.start()	

        # Loop continuously checking for data added to the queue
        while True:
            if not storage_queue.empty():
                received_data_arr = storage_queue.get() # 0 = From ; 1 = To ; 2 Data
                # print "*********************************" + str(type(received_data_arr[2]))
                print "[Queue] Received from: " + str(received_data_arr[0]) + " - Send to: " + str(received_data_arr[1]) + " - Content: " + str(received_data_arr[2])
                if received_data_arr[1] == 'android':  # send to android
                        bt.send(received_data_arr[2])
                elif received_data_arr[1] == 'pc':  # send to PC
                        pc_api.send(received_data_arr[2])
                elif received_data_arr[1] == 'arduino':  # send to arduino
                        ard_api.send(received_data_arr[2])
                elif received_data_arr[1] == 'arduino_api':  # send to arduino API
                        ard_api.put(received_data_arr[2])
                
except:
    print '=================================================================================='
    print '>>> traceback <<<'
    traceback.print_exc()
    print '>>> end of traceback <<<'
    print '=================================================================================='
    sys.exit(1)

