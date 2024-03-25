import time
from pymavlink import mavutil
from Dron import Dron


class Dron2:
    def connect(self,connection_string, baud, callback=None, params=None):

        #self.vehicle = mavutil.mavlink_connection('tcp:127.0.0.1:5762')
        self.vehicle = mavutil.mavlink_connection(connection_string, baud)
        self.vehicle.wait_heartbeat()

    def send_local_telemetry_info(self):


        ''' self.vehicle.mav.request_data_stream_send(
            self.vehicle.target_system,  self.vehicle.target_component,
            mavutil.mavlink.MAV_DATA_STREAM_POSITION,
            100,
            1
        )'''

        while True:
            msg = self.vehicle.recv_match(type='LOCAL_POSITION_NED', blocking=True)
            if True:
                local_telemetry_info = {
                    'posX': msg.x ,
                    'posY': msg.y,
                    'posZ': -msg.z,
                }
            print ('version 1 ',local_telemetry_info)






def showLocalTelemetryInfo ( telemetry_info):
    print ('Telemetria: ', telemetry_info)

dron2 = Dron()
connection_string = 'tcp:127.0.0.1:5763'
baud = 115200
#_connect(connection_string, baud)

#print ('conectado')
#_send_local_telemetry_info()
'''frequency_hz = 1
vehicle.mav.request_data_stream_send(
    vehicle.target_system, vehicle.target_component,
    mavutil.mavlink.MAV_DATA_STREAM_POSITION,
    100,
    1
)
sendLocalTelemetryInfo = True
while sendLocalTelemetryInfo:
    msg = vehicle.recv_match(type='LOCAL_POSITION_NED', blocking=True)
    if True:
        local_telemetry_info = {
            'posX': msg.x,
            'posY': msg.y,
            'posZ': -msg.z,
        }
        print('version 2 ',msg.x, msg.y, msg.z)
    time.sleep (1)'''

dron2.connect (connection_string, baud)
dron2.send_local_telemetry_info(showLocalTelemetryInfo)
while True:
    pass