import json
import threading

import paho.mqtt.client as mqtt
import time
def on_connect(client, userdata, flags, rc):
    global connected
    if rc==0:
        print("connected OK Returned code=",rc)
        connected = True
    else:
        print("Bad connection Returned code=",rc)



def on_message(client, userdata, message):
    global estado
    global destinoAlcanzado
    if message.topic == 'autopilotServiceDemo/consola/telemetryInfo':
        telemetry_info = json.loads(message.payload)
        print (telemetry_info)
    if message.topic == 'autopilotServiceDemo/consola/parameters':
        parameters = json.loads(message.payload)
        print('Parameters: ',parameters)
    if message.topic == 'autopilotServiceDemo/consola/connected':
        estado = 'connected'
    if message.topic == 'autopilotServiceDemo/consola/armed':
        estado = 'armed'
    if message.topic == 'autopilotServiceDemo/consola/flying':
        estado = 'flying'

estado = 'desconectado'
broker_address = "broker.hivemq.com"
broker_port = 1883

client = mqtt.Client("consola")

client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port)
client.subscribe('autopilotServiceDemo/consola/#')
client.loop_start()

print ('empiezo')

client.publish('consola/autopilotServiceDemo/connect')
time.sleep (5)
client.publish('consola/autopilotServiceDemo/startTelemetry')
while estado != 'connected':
    pass



parameters = json.dumps([
    {'ID': "RTL_ALT", 'Value': 110},
    {'ID': "PILOT_SPEED_UP", 'Value': 155},
    {'ID': "FENCE_ACTION", 'Value': 2},
])
print ('voy a escribir parámetros')
client.publish('consola/autopilotServiceDemo/setParameters', parameters)
time.sleep (5)
parameters =  json.dumps([
    "RTL_ALT",
    "PILOT_SPEED_UP",
    "FENCE_ACTION"
])
print ('voy a pedir parámetros')
client.publish('consola/autopilotServiceDemo/getParameters', parameters)
time.sleep (5)

client.publish('consola/autopilotServiceDemo/arm')
while estado != 'armed':
    pass
print ('armado')

client.publish('consola/autopilotServiceDemo/takeOff')
while estado != 'flying':
    pass
print ('volando')


time.sleep (5)

client.publish('consola/autopilotServiceDemo/Land')
while estado != 'landed':
    pass

print ('en tierra')


while True:
    pass