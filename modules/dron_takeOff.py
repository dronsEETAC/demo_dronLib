import threading
import time
from pymavlink import mavutil

def _takeOff(self, aTargetAltitude,callback=None, params = None):
    print ('empiezo a despegar')
    self.state = "despegando"
    self.vehicle.mav.command_long_send(self.vehicle.target_system, self.vehicle.target_component,
                                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)

    while True:
<<<<<<< HEAD
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
=======
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=False)
>>>>>>> 20b3b69fafb27e1b439ca79c23128582cc426bc8
        #print('meg ', msg)
        if msg:
            msg = msg.to_dict()

            alt = float(msg['relative_alt'] / 1000)
<<<<<<< HEAD
            print ('altitud ', alt)
=======
            #print ('altitud ', alt)
>>>>>>> 20b3b69fafb27e1b439ca79c23128582cc426bc8
            if alt >= aTargetAltitude * 0.90:
                print("Reached target altitude")
                break
        time.sleep(2)



    self.state = "volando"
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



def takeOff(self, aTargetAltitude, blocking=True, callback=None, params = None):
    if blocking:
        self._takeOff(aTargetAltitude)
    else:
        takeOffThread = threading.Thread(target=self._takeOff, args=[aTargetAltitude, callback, params])
        takeOffThread.start()

