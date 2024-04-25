import json
import time

from Dron import Dron

def showTelemetryInfo (id, telemetry_info):
    print ('Telemetria: ', telemetry_info)


def informar (id, mensaje):
    global volando
    print ('Mensaje del dron '+ str(id) + ': ' +mensaje)
    volando = True

dron = Dron()
connection_string = 'tcp:127.0.0.1:5763'
baud = 115200
print ('voy a conectarme')
dron.connect (connection_string, baud, id = 1)
print ('conectado')
geofence = [
    {'lat':   41.2763410, 'lon':  1.9888285},
    {'lat': 41.27637, 'lon': 1.9889},
    {'lat': 41.27635, 'lon': 1.9882},
]
print ('voy con el geofence')
dron.setGEOFence(json.dumps(geofence))
print ('ya esta')

print ('conectado')
'''dron.arm()
print ('armado')'''
dron.send_telemetry_info(showTelemetryInfo)
plan =   {
        "takeOffAlt": 5,
        "waypoints":
            [
                {
                    'lat': 41.2763410,
                    'lon': 1.9888285,
                    'alt': 12
                },
                {
                    'lat': 41.27623,
                    'lon': 1.987,
                    'alt': 14
                }
            ]

    }
dron.executeMission(plan, blocking=False, callback=informar, params ='YA HEMOS ACABADO LA MISION')
print ('ya hemos iniciado la mision')
#volando = False
#dron.takeOff(15, blocking=False, callback=informar, params='EN EL AIRE')
#dron.takeOff (15)
print ('en el aire')
while True:
    print ('Hago cosas')
    time.sleep(2)