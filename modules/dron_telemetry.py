import json
import math
import threading
import time

from pymavlink import mavutil


def _send_telemetry_info2(self, process_telemetry_info):
    frequency_hz = 1
    self.vehicle.mav.command_long_send(
        self.vehicle.target_system,  self.vehicle.target_component,
        mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL, 0,
        mavutil.mavlink.MAVLINK_MSG_ID_GLOBAL_POSITION_INT, # The MAVLink message ID
        1e6 / frequency_hz, # The interval between two messages in microseconds. Set to -1 to disable and 0 to request default rate.
        0, 0, 0, 0, # Unused parameters
        0, # Target address of message stream (if message has target address fields). 0: Flight-stack default (recommended), 1: address of requestor, 2: broadcast.
    )
    self.alt = 0
    self.sendTelemetryInfo = True
    while self.sendTelemetryInfo:
        #msg = self.vehicle.recv_match(type='AHRS2', blocking= True).to_dict()
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking= False)
        if msg:
            msg = msg.to_dict()
            self.lat = float(msg['lat'] / 10 ** 7)
            self.lon = float(msg['lon'] / 10 ** 7)
            self.alt = float(msg['relative_alt']/1000)
            self.heading = float(msg['hdg'] / 100)

            vx =  float(msg['vx'])
            vy = float(msg['vy'])
            self.groundSpeed = math.sqrt( vx*vx+vy*vy)/100
            telemetry_info = {
                'lat': self.lat,
                'lon': self.lon,
                'alt': self.alt,
                'groundSpeed':  self.groundSpeed,
                'heading': self.heading,
                'state': self.state
            }

            if self.id == None:
                process_telemetry_info (telemetry_info)
            else:
                process_telemetry_info (self.id, telemetry_info)


        time.sleep(1)

def _send_telemetry_info(self, process_telemetry_info):

    frequency_hz = 1
    self.vehicle.mav.request_data_stream_send(
        self.vehicle.target_system,  self.vehicle.target_component,
        mavutil.mavlink.MAV_DATA_STREAM_POSITION,
        10,
        1
    )

    self.alt = 0
    self.sendTelemetryInfo = True
    while self.sendTelemetryInfo:
        msg = self.vehicle.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            msg = msg.to_dict()
            self.lat = float(msg['lat'] / 10 ** 7)
            self.lon = float(msg['lon'] / 10 ** 7)
            self.alt = float(msg['relative_alt'] / 1000)
            self.heading = float(msg['hdg'] / 100)

            vx = float(msg['vx'])
            vy = float(msg['vy'])
            self.groundSpeed = math.sqrt(vx * vx + vy * vy) / 100
            telemetry_info = {
                'lat': self.lat,
                'lon': self.lon,
                'alt': self.alt,
                'groundSpeed': self.groundSpeed,
                'heading': self.heading,
                'state': self.state
            }

            if self.id == None:
                process_telemetry_info(telemetry_info)
            else:
                process_telemetry_info(self.id, telemetry_info)


def send_telemetry_info(self, process_telemetry_info):
    telemetryThread = threading.Thread(target=self._send_telemetry_info, args=[process_telemetry_info,])
    telemetryThread.start()

def stop_sending_telemetry_info(self):
    self.sendTelemetryInfo = False