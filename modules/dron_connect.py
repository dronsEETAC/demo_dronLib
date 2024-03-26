import json
import math
import threading
import time

from pymavlink import mavutil


def _handle_heartbeat(self):
    while True:
        msg = self.vehicle.recv_match(
            type='HEARTBEAT', blocking=True)
        print (msg)
        if msg.base_mode == 89:
            print ('Desarmado')
        elif msg.base_mode == 217:
            print('Armado')




# Some more small functions
def _connect(self, connection_string, baud, callback=None, params=None):
    #self.vehicle = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
    self.vehicle = mavutil.mavlink_connection(connection_string, baud)
    self.vehicle.wait_heartbeat()
    handleThread = threading.Thread (target = self._handle_heartbeat)
    handleThread.start()
    self.state = "conectado"
    '''frequency_hz = 1
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system, self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT,  # The MAVLink message ID
        1e6 / frequency_hz,
        # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0,  # Unused parameters
        0,
        # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )'''
    self.vehicle.mav.request_data_stream_send(
        self.vehicle.target_system, self.vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        10,
        1
    )
    if callback != None:
        if self.id == None:
            if params == None:
                callback()
            else:
                callback(params)
        else:
            if params == None:
                callback(self.id)
            else:
                callback(self.id, params)


def connect(self,
            connection_string,
            baud,
            id= None,
            blocking=True,
            callback=None,
            params = None):
    print ('id: ', id)
    self.id = id
    if blocking:
        self._connect(connection_string, baud)
    else:
        connectThread = threading.Thread(target=self._connect, args=[connection_string, baud, callback, params, ])
        connectThread.start()

def disconnect (self):
    self.state = "conectado"
    self.vehicle.mav.request_data_stream_send(
        self.vehicle.target_system, self.vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        10,
        0
    )
    self.stop_sending_telemetry_info()
    self.stop_sending_local_telemetry_info()
    self.vehicle.close()