import json
import math
import threading
import time

from pymavlink import mavutil


# Some more small functions
def _connect(self, connection_string, baud, callback=None, params=None):
    #self.vehicle = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
    self.vehicle = mavutil.mavlink_connection(connection_string, baud)
    self.vehicle.wait_heartbeat()
    self.state = "conectado"
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

