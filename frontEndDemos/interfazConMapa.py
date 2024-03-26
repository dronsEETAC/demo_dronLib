import math
import tkinter as tk
from Dron import Dron
from tkinter import messagebox

class Conversor:
    # La conversion entre posiciones y coordenadas tiene esta dificultad: las coordenadas
    # corresponden al plano XY. Desplazamientos en la dimensión X corresponden a movimiento Este-Oeste
    # mientras que desplazamientos en la dimensión Y corresponden a movimiento en el eje norte-sur
    # En cambio la posición en la que está el dron está en formato NED, es decir posicion[0] es el desplazamiento
    # en el eje Norte-sur respecto al home y posicion[1] es desplazamiento en eje este-oeste y posicion[2] es
    # desplazamiento en el eje down-up
    def setUp(self, metrosX, metrosY, pixelsX, pixelsY):
        self.metrosX = metrosX
        self.metrosY = metrosY
        self.pixelsX = pixelsX
        self.pixelsY = pixelsY
        self.center = (pixelsX//2, pixelsY//2)
    def convertToPosition (self, x,y):
        difX = x - self.center[0]
        difY = self.center[1] -y
        posY = (difX*self.metrosX)/self.pixelsX
        posX = (difY*self.metrosY)/self.pixelsY
        return posX, posY

    def convertToCoord (self, posX, posY):
        x = (self.pixelsX*posY)/self.metrosX + self.center[0]
        y = (self.pixelsY*posX)/self.metrosY - self.center[1]
        return int(x), -int (y)
def informar (mensaje):
    global dron
    print (mensaje)
def volando ():
    global mapa, dronIcon, dronHeading, takeOffBtn
    mapa.itemconfig(dronIcon, fill='green')
    mapa.itemconfig(dronHeading, fill='green')
    takeOffBtn ['bg']='green'
    takeOffBtn ['text']='volando'
    takeOffBtn ['fg']='white'



def showLocalTelemetryInfo (local_telemetry_info):
    global heading, altitude, groundSpeed, state
    global altShowLbl, headingShowLbl, speedShowLbl
    altShowLbl['text'] = round (local_telemetry_info['posX'],2)
    headingShowLbl['text'] =  round (local_telemetry_info['posY'],2)
    speedShowLbl['text'] = round (local_telemetry_info['posZ'],2)

def enDestino ():
    global mapa, destination
    mapa.delete (destination)
def goHere (event):
    global conversor
    global dronIcon, mapa, iconSize
    global dron, area
    global menu, destination
    menu.post(event.x_root, event.y_root)

    posX,posY = conversor.convertToPosition(event.x, event.y)

    if not dron.moveto ((posX,posY, dron.alt), blocking = False, callback = enDestino):
        mapa.itemconfig(area, outline='red', width=10)
    else:
        mapa.itemconfig(area, outline='grey', width=10)
        destination = mapa.create_oval(event.x - 5, event.y -5 , event.x + 5, event.y + 5 , fill='blue')



def crearEspacio ():
    global dimXSldr, dimYSldr, dimZSldr, alturaSldr, takeOffAltSldr
    global ventana
    global mapa, dronIcon, iconSize, arrow
    global conversor
    global menu
    global height
    global dron
    global canvasSize, area

    dimE_O = int (dimXSldr.get())
    dimN_S = int (dimYSldr.get())
    altura = int (dimZSldr.get())
    dron.setLocalGeofence(dimN_S,dimE_O,altura)
    alturaSldr.config(from_=altura, to=0)
    alturaSldr.grid(row=0, column=0, padx=5,pady=3, sticky=tk.N + tk.S + tk.E + tk.W)
    takeOffAltSldr.config(from_=0, to=altura)
    takeOffAltSldr.set(3)
    takeOffAltSldr.grid(row=6, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)


    iconSize = 20
    height = (canvasSize*dimN_S)//dimE_O
    area = mapa.create_rectangle(0, 0, canvasSize, height, fill='gray')
    menu = tk.Menu(ventana, tearoff=0)
    menu.add_command(label="Vuela aquí")
    mapa.bind('<Button-3>', goHere)
    homeIcon = mapa.create_oval(canvasSize//2-iconSize//2, height//2 - iconSize//2, canvasSize//2+iconSize//2, height//2 + iconSize//2, outline='red',  width=2)
    conversor = Conversor()
    conversor.setUp (dimE_O, dimN_S, canvasSize, height)



def dibuja_dron ():
    global height, iconSize, arrowLength
    global dronIcon, dronHeading

    x, y = canvasSize//2, height//2
    arrowLength = 40
    dronIcon = mapa.create_oval(x - iconSize // 2, y - iconSize // 2, x + iconSize // 2,
                                y + iconSize // 2, fill='red')

    dronHeading= mapa.create_line(
        x, y, x, y + arrowLength,
        fill="red", arrow=tk.LAST)

def mueve_dron (x,y):
    global mapa, dronIcon, iconSize, dronHeading
    mapa.coords(dronIcon, x - iconSize // 2, y - iconSize // 2, x + iconSize // 2,
                                y + iconSize // 2)
    x1, y1, x2, y2 = mapa.coords(dronHeading)
    dx = x - x1
    dy = y - y1
    mapa.move(dronHeading, dx, dy)


def cambiar_orientacion(angulo):
    global mapa, arrowLength, dronHeading
    x, y, x2, y2 = mapa.coords(dronHeading)
    # Convertir el ángulo de grados a radianes
    angulo_rad = math.radians(angulo)

    # Calcular las coordenadas del punto final de la línea
    x_final = x + arrowLength * math.sin(angulo_rad)
    y_final = y - arrowLength * math.cos(angulo_rad)
    mapa.coords(dronHeading, x, y, x_final, y_final)

def process_local_telemetry_info (local_telemetry_info):
    global mapa, dronIcon, alturaSldr, iconSize, headingArrow
    posX = round (local_telemetry_info['posX'],2)
    posY = round (local_telemetry_info['posY'],2)
    posZ = round (local_telemetry_info['posZ'],2)
    alt = math.ceil(-posZ*10)/10
    alturaSldr.set (alt)
    x, y = conversor.convertToCoord(posX, posY)
    mueve_dron (x,y)


def process_telemetry_info (telemetry_info):
    global mapa, arrow
    heading = round(telemetry_info['heading'],2)
    cambiar_orientacion(heading)



def connect ():
    global dron, stepSldr, alturaSldr
    global height, arrow, mapa, dronIcon, dronHeading, connectBtn
    global connectorEntry
    if connectBtn ['text'] == 'Conectar':
        connector = connectorEntry.get()
        if connector == 'sim':
            connection_string ='tcp:127.0.0.1:5763'
            baud = 115200
        else:
            connection_string = connector
            baud = 57600
        dron.connect(connection_string,baud)
        dibuja_dron()

        stepSldr.set (0.5)

        alturaSldr.set (0)
        navSpeedSldr.set (1)
        dron.setNavSpeed(1)
        dron.send_local_telemetry_info(process_local_telemetry_info)
        dron.send_telemetry_info(process_telemetry_info)
        connectBtn ['bg']='green'
        connectBtn ['text']='Desconectar'
        connectBtn ['fg']='white'
    else:
        dron.disconnect()
        mapa.delete (dronIcon)
        mapa.delete (dronHeading)
        connectBtn['bg'] = 'orange'
        connectBtn['text'] = 'Conectar'
        connectBtn['fg'] = 'black'
        connectorEntry.delete(0, tk.END)
        connectorEntry.insert (0,'sim')



def arm ():
    global dron, mapa, dronIcon, dronHeading, armBtn
    dron.arm()
    mapa.itemconfig(dronIcon, fill='yellow')
    mapa.itemconfig(dronHeading, fill='yellow')
    armBtn['bg'] = 'green'
    armBtn['text'] = 'Armado'
    armBtn['fg'] = 'white'






def takeoff ():
    global dron, mapa, dronIcon, dronHeading, takeOffAltSldr
    dron.takeOff (takeOffAltSldr.get(), blocking = False,  callback = volando)
    mapa.itemconfig(dronIcon, fill='orange')
    mapa.itemconfig(dronHeading, fill='orange')

def enTierra ():
    global mapa, dronIcon, dronHeading, landBtn, armBtn, takeOffBtn, RTLBtn
    mapa.itemconfig(dronIcon, fill='red')
    mapa.itemconfig(dronHeading, fill='red')
    landBtn['bg'] = 'orange',
    landBtn['text'] = 'Aterrizar',
    landBtn['fg'] = 'black'

    RTLBtn['bg'] = 'orange',
    RTLBtn['text'] = 'RTL',
    RTLBtn['fg'] = 'black'

    armBtn['bg'] = 'orange',
    armBtn['text'] = 'Armar',
    armBtn['fg'] = 'black'

    takeOffBtn['bg'] = 'orange',
    takeOffBtn['text'] = 'Despegar',
    takeOffBtn['fg'] = 'black'

def land():
    global dron
    dron.Land(blocking = False,   callback = enTierra)
    landBtn['bg'] = 'green',
    landBtn['text'] = 'Aterrizando',
    landBtn['fg'] = 'white'

def RTL():
    global dron, RTLBtn
    dron.RTL(blocking = False,   callback = enTierra)
    RTLBtn['bg'] = 'green',
    RTLBtn['text'] = 'Retornando',
    RTLBtn['fg'] = 'white'

def llegada (btn):
    btn['bg'] = 'orange'
    btn['fg'] = 'black'

def move (direction, btn = None):
    global dron, area, mapa
    btn['bg'] = 'green'
    btn['fg'] = 'white'
    if not dron.move (direction, blocking = False,  callback = lambda: llegada(btn)):
        mapa.itemconfig (area, outline='red', width = 10 )
    else:
        mapa.itemconfig(area, outline='grey', width = 1 )

def startGo():
    global dron
    dron.startGo()


def stopGo():
    global dron
    dron.stopGo()

def startLocalTelem():
    global dron
    dron.send_local_telemetry_info(showLocalTelemetryInfo)


def stopLocalTelem():
    global dron
    dron.stop_sending_local_telemetry_info()

def fixHeading ():
    global dron
    dron.fixHeading()

def unfixHeading ():
    global dron
    dron.unfixHeading()

def changeHeading (heading):
    global dron
    global gradesSldr
    dron.changeHeading(int (heading))

def setStep (step):
    global dron
    dron.setStep(float (step))


def setNavSpeed (speed):
    global dron
    dron.setNavSpeed(float(speed))



def draw_arrow(canvas, x, y, length, angle_degrees):
    angle_radians = math.radians(angle_degrees + 180)
    x1 = x - length * math.sin(angle_radians)
    y1 = y + length * math.cos(angle_radians)
    return canvas.create_line(x, y, x1, y1, arrow=tk.LAST, fill="red", width=5)

def crear_ventana():
    global dron
    global dimXSldr, dimYSldr, dimZSldr, stepSldr, alturaSldr, takeOffAltSldr, navSpeedSldr
    global mapa, mapaFrame
    global connectBtn, armBtn, takeOffBtn, landBtn, RTLBtn
    global canvasSize
    global connectorEntry

    canvasSize = 800
    dron = Dron()

    ventana = tk.Tk()
    ventana.title("Control dron interior")
    ventana.geometry("1200x850")
    ventana.rowconfigure(0, weight=1)

    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)
    ventana.columnconfigure(2, weight=1)

    #############################################################################
    controlFrame = tk.LabelFrame(ventana, text="Controles")
    controlFrame.grid(row=0, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    controlFrame.rowconfigure(0, weight=1)
    controlFrame.rowconfigure(1, weight=1)
    controlFrame.rowconfigure(2, weight=1)
    controlFrame.rowconfigure(3, weight=1)
    controlFrame.rowconfigure(4, weight=1)
    controlFrame.rowconfigure(5, weight=1)
    controlFrame.rowconfigure(6, weight=1)
    controlFrame.rowconfigure(7, weight=1)
    controlFrame.rowconfigure(8, weight=1)
    controlFrame.rowconfigure(9, weight=1)
    controlFrame.rowconfigure(10, weight=1)
    controlFrame.rowconfigure(11, weight=1)
    controlFrame.rowconfigure(12, weight=1)
    controlFrame.rowconfigure(13, weight=1)
    controlFrame.rowconfigure(14, weight=1)


    controlFrame.columnconfigure(0, weight=1)
    controlFrame.columnconfigure(1, weight=1)


    dimXSldr = tk.Scale(controlFrame, label="dimension X (m)", resolution=1, from_=0, to=50, tickinterval=10,
                          orient=tk.HORIZONTAL)
    dimXSldr.grid(row=0, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    dimYSldr = tk.Scale(controlFrame, label="dimension Y (m)", resolution=1, from_=0, to=50, tickinterval=10,
                        orient=tk.HORIZONTAL)
    dimYSldr.grid(row=1, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    dimZSldr = tk.Scale(controlFrame, label="dimension Z (m)", resolution=1, from_=0, to=10, tickinterval=1,
                        orient=tk.HORIZONTAL)
    dimZSldr.grid(row=2, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    crearBtn = tk.Button(controlFrame, text="Crear espacio", bg="dark orange", command=crearEspacio)
    crearBtn.grid(row=3, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)


    connectBtn = tk.Button(controlFrame, text="Conectar", bg="dark orange", command = connect)
    connectBtn.grid(row=4, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    connectorEntry = tk.Entry(controlFrame)
    connectorEntry.insert(0,'sim')
    connectorEntry.grid(row=4, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    armBtn = tk.Button(controlFrame, text="Armar", bg="dark orange", command=arm)
    armBtn.grid(row=5, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    takeOffAltSldr = tk.Scale(controlFrame, label="Altura de despegue (m)", resolution=1, from_=0, to=10, tickinterval=1,
                        orient=tk.HORIZONTAL)
    #takeOffAltSldr.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    takeOffBtn = tk.Button(controlFrame, text="Despegar", bg="dark orange", command=takeoff)
    takeOffBtn.grid(row=7, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)


    landBtn = tk.Button(controlFrame, text="Aterrizar", bg="dark orange", command=land)
    landBtn.grid(row=8, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    RTLBtn = tk.Button(controlFrame, text="RTL", bg="dark orange", command=RTL)
    RTLBtn.grid(row=8, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    stepSldr = tk.Scale(controlFrame, label="Step (m)", resolution=0.5, from_=0, to=10, tickinterval=1,
                        orient=tk.HORIZONTAL, command=setStep)
    stepSldr.grid(row=9, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    navSpeedSldr = tk.Scale(controlFrame, label="Velocidad de navegación (m/s)", resolution=1, from_=0, to=10,
                            tickinterval=1,
                            orient=tk.HORIZONTAL, command=setNavSpeed)
    navSpeedSldr.grid(row=10, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    forwardBtn = tk.Button(controlFrame, text="Adelante", bg="dark orange", command=lambda: move("Forward", forwardBtn))
    forwardBtn.grid(row=11, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    backBtn = tk.Button(controlFrame, text="Atrás", bg="dark orange", command=lambda: move("Back", backBtn))
    backBtn.grid(row=11, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    leftBtn = tk.Button(controlFrame, text="Izquierda", bg="dark orange", command=lambda: move("Left", leftBtn))
    leftBtn.grid(row=12, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    rightBtn = tk.Button(controlFrame, text="Derecha", bg="dark orange", command=lambda: move("Right", rightBtn))
    rightBtn.grid(row=12, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    upBtn = tk.Button(controlFrame, text="Arriba", bg="dark orange", command=lambda: move("Up", upBtn))
    upBtn.grid(row=13, column=0, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    downBtn = tk.Button(controlFrame, text="Abajo", bg="dark orange", command=lambda: move("Down", downBtn))
    downBtn.grid(row=13, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    gradesSldr = tk.Scale(controlFrame, label="Cambiar el heading (grados)", resolution=5, from_=0, to=360,
                          tickinterval=90,
                          orient=tk.HORIZONTAL, command=changeHeading)
    gradesSldr.grid(row=14, column=0, columnspan=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    #############################################################################
    alturaFrame = tk.LabelFrame(ventana, text="Altura")
    alturaFrame.grid(row=0, column=1, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)
    alturaFrame.rowconfigure(0, weight=1)
    alturaFrame.columnconfigure(0, weight=1)

    alturaSldr = tk.Scale(alturaFrame, resolution=0.5, from_=50, to=0, tickinterval=1,
                          orient=tk.VERTICAL)

    #############################################################################
    mapaFrame = tk.LabelFrame(ventana, text="Mapa")
    mapaFrame.grid(row=0, column=2, padx=5, pady=3, sticky=tk.N + tk.S + tk.E + tk.W)

    mapa = tk.Canvas(mapaFrame, bg="white", height=canvasSize, width=canvasSize)
    #mapa.pack( fill=tk.BOTH)
    mapa.pack( )



    return ventana


if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()
