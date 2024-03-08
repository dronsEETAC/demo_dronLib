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
dron.arm()
print ('armado')
dron.send_telemetry_info(showTelemetryInfo)
#volando = False
#dron.takeOff(15, blocking=False, callback=informar, params='EN EL AIRE')
dron.takeOff (15)
print ('en el aire')
while True:
    print ('Hago cosas')
    time.sleep(2)