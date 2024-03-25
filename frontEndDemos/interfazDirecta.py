import tkinter as tk
from Dron import Dron
from tkinter import messagebox

def informar (mensaje):
    global dron
    print ('informar')
    messagebox.showinfo("showinfo", "Mensaje del dron:--->  "+mensaje)

def showTelemetryInfo (telemetry_info):
    global heading, altitude, groundSpeed, state
    global altShowLbl, headingShowLbl, speedShowLbl
<<<<<<< HEAD
    altShowLbl['text'] = round (telemetry_info['alt'],2)
    headingShowLbl['text'] =  round(telemetry_info['heading'],2)
    speedShowLbl['text'] = round (telemetry_info['groundSpeed'],2)


def connect ():
    global dron, speedSldr
    connection_string ='tcp:127.0.0.1:5763'
    baud = 115200
    dron.connect(connection_string,baud)
    speedSldr.set(1)
=======
    altShowLbl['text'] = telemetry_info['alt']
    headingShowLbl['text'] =  telemetry_info['heading']
    speedShowLbl['text'] = telemetry_info['groundSpeed']


def connect ():
    global dron
    connection_string ='tcp:127.0.0.1:5763'
    baud = 115200
    dron.connect(connection_string,baud)
>>>>>>> 20b3b69fafb27e1b439ca79c23128582cc426bc8

def arm ():
    global dron
    dron.arm()

def takeoff ():
    global dron
    dron.takeOff (10, blocking = False,  callback = informar, params= 'VOLANDO')
    #dron.takeOff (8)

def land ():
    global dron
    dron.Land(blocking = False,  callback = informar, params= 'EN TIERRA')

def RTL():
    global dron
    dron.RTL(blocking = False,   callback = informar, params= 'EN TIERRA')

def go (direction):
    global dron
    print ('vamos a: ', direction)
    dron.go (direction)

def startGo():
    global dron
    dron.startGo()


def stopGo():
    global dron
    dron.stopGo()

def startTelem():
    global dron
    dron.send_telemetry_info(showTelemetryInfo)


def stopTelem():
    global dron
    dron.stop_sending_telemetry_info()

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

def changeNavSpeed (speed):
    global dron
    global speedSldr
    dron.changeNavSpeed(float (speed))
def crear_ventana():
    global dron
    global  altShowLbl, headingShowLbl,  speedSldr, gradesSldr, speedShowLbl
    global takeOffBtn

    dron = Dron()

    ventana = tk.Tk()
    ventana.title("Ventana con botones y entradas")
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)
    ventana.rowconfigure(3, weight=1)
    ventana.rowconfigure(4, weight=1)
    ventana.rowconfigure(5, weight=1)
    ventana.rowconfigure(6, weight=1)
    ventana.rowconfigure(7, weight=1)
    ventana.rowconfigure(8, weight=1)
    ventana.rowconfigure(9, weight=1)
    ventana.rowconfigure(10, weight=1)


    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)


    connectBtn = tk.Button(ventana, text="Conectar", bg="dark orange", command = connect)
    connectBtn.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    armBtn = tk.Button(ventana, text="Armar", bg="dark orange", command=arm)
    armBtn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    takeOffBtn = tk.Button(ventana, text="Despegar", bg="dark orange", command=takeoff)
    takeOffBtn.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    fixBtn = tk.Button(ventana, text="fijar heading", bg="dark orange", command=fixHeading)
    fixBtn.grid(row=3, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    unfixBtn = tk.Button(ventana, text="desfijar heading", bg="dark orange", command=unfixHeading)
    unfixBtn.grid(row=3, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Quality and Period sliders
    gradesSldr = tk.Scale(ventana, label="Grados:", resolution=5, from_=0, to=360, tickinterval=45,
                              orient=tk.HORIZONTAL, command = changeHeading)
    #gradesSldr.set(45)
    gradesSldr.grid(row=4, column=0, columnspan=2,padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    landBtn = tk.Button(ventana, text="aterrizar", bg="dark orange", command=land)
    landBtn.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    RTLBtn = tk.Button(ventana, text="RTL", bg="dark orange", command=RTL)
    RTLBtn.grid(row=5, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    StartBtn = tk.Button(ventana, text="Empezar a navegar", bg="dark orange", command=startGo)
    StartBtn.grid(row=6, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    StopBtn = tk.Button(ventana, text="Parar de navegar", bg="dark orange", command=stopGo)
    StopBtn.grid(row=6, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    navFrame = tk.LabelFrame (ventana, text = "Navegación")
    navFrame.grid(row=7, column=0, columnspan = 2, padx=50, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    navFrame.rowconfigure(0, weight=1)
    navFrame.rowconfigure(1, weight=1)
    navFrame.rowconfigure(2, weight=1)


    navFrame.columnconfigure(0, weight=1)
    navFrame.columnconfigure(1, weight=1)
    navFrame.columnconfigure(2, weight=1)


    NWBtn = tk.Button(navFrame, text="NW", bg="dark orange",
                        command= lambda: go("NorthWest"))
    NWBtn.grid(row=0, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NoBtn = tk.Button(navFrame, text="No", bg="dark orange",
                        command= lambda: go("North"))
    NoBtn.grid(row=0, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NEBtn = tk.Button(navFrame, text="NE", bg="dark orange",
                        command= lambda: go("NorthEast"))
    NEBtn.grid(row=0, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)



    WeBtn = tk.Button(navFrame, text="We", bg="dark orange",
                        command=lambda: go("West"))
    WeBtn.grid(row=1, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    StopBtn = tk.Button(navFrame, text="St", bg="dark orange",
                        command=lambda: go("Stop"))
    StopBtn.grid(row=1, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    EaBtn = tk.Button(navFrame, text="Ea", bg="dark orange",
                        command=lambda: go("East"))
    EaBtn.grid(row=1, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)


    SWBtn = tk.Button(navFrame, text="SW", bg="dark orange",
                        command=lambda: go("SouthWest"))
    SWBtn.grid(row=2, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SoBtn = tk.Button(navFrame, text="So", bg="dark orange",
                        command=lambda: go("South"))
    SoBtn.grid(row=2, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SEBtn = tk.Button(navFrame, text="SE", bg="dark orange",
                        command=lambda: go("SouthEast"))
    SEBtn.grid(row=2, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)



    speedSldr = tk.Scale(ventana, label="Velocidad (m/s):", resolution=1, from_=0, to=20, tickinterval=5,
                          orient=tk.HORIZONTAL, command = changeNavSpeed)
    #speedSldr.set(1)
    speedSldr.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    StartTelemBtn = tk.Button(ventana, text="Empezar a enviar telemetría", bg="dark orange", command=startTelem)
    StartTelemBtn.grid(row=9, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    StopTelemBtn = tk.Button(ventana, text="Parar de enviar telemetría", bg="dark orange", command=stopTelem)
    StopTelemBtn.grid(row=9, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    telemetryFrame = tk.LabelFrame(ventana, text="Telemetría")
    telemetryFrame.grid(row=10, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    telemetryFrame.rowconfigure(0, weight=1)
    telemetryFrame.rowconfigure(1, weight=1)

    telemetryFrame.columnconfigure(0, weight=1)
    telemetryFrame.columnconfigure(1, weight=1)
    telemetryFrame.columnconfigure(2, weight=1)


    altLbl = tk.Label(telemetryFrame, text='Altitud')
    altLbl.grid(row=0, column=0,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    headingLbl = tk.Label(telemetryFrame, text='Heading')
    headingLbl.grid(row=0, column=1,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    speedLbl = tk.Label(telemetryFrame, text='Speed')
<<<<<<< HEAD
    speedLbl.grid(row=0, column=2,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
=======
    speedLbl.grid(row=0, column=3,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
>>>>>>> 20b3b69fafb27e1b439ca79c23128582cc426bc8


    altShowLbl = tk.Label(telemetryFrame, text='')
    altShowLbl.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    headingShowLbl = tk.Label(telemetryFrame, text='',)
    headingShowLbl.grid(row=1, column=1,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    speedShowLbl = tk.Label(telemetryFrame, text='', )
    speedShowLbl.grid(row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    return ventana


if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()
