import threading
import time
from pymavlink import mavutil

def _goDown(self, mode, callback=None, params = None):

    # Get mode ID
    mode_id = self.vehicle.mode_mapping()[mode]
    self.vehicle.mav.set_mode_send(
        self.vehicle.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    #arm_msg = self.vehicle.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    #
    while True:
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
        if msg:
            msg = msg.to_dict()
            alt = float(msg['relative_alt'] / 1000)
            if alt < 0.2:
                break
            time.sleep(2)

    self.vehicle.motors_disarmed_wait()
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


def RTL (self, blocking=True, callback=None, params = None):
    self.state = 'retornando'
    if blocking:
        self._goDown('RTL')
    else:
        goingDownThread = threading.Thread(target=self._goDown, args=['RTL', callback, params])
        goingDownThread.start()

def Land (self, blocking=True, callback=None, params = None):
    self.state = 'aterrizando'
    if blocking:
        self._goDown('LAND')
    else:
        print ('pongo el thread')
        goingDownThread = threading.Thread(target=self._goDown, args=['LAND', callback, params])
        goingDownThread.start()


