
class Dron(object):
    def __init__(self):

        self.state = "desconectado"
        self.lat = None
        self.lon = None
        self.alt = None
        ''' os otros estados son:
            conectado
            armando
            despegando
            volando
            regresando
        '''

        self.going = False # se usa en dron_nav
        self.navSpeed = 5 # se usa en dron_nav
        self.direction = 'Stop' # se usa en dron_nav
        self.id = None
        self.sendTelemetryInfo = False #usado en dron_telemetry

    # aqui se importan los métodos de la clase Dron, que están organizados en ficheros.
    # Así podría orgenizarse la aportación de futuros alumnos que necesitasen incorporar nuevos servicios
    # para sus aplicaciones. Crearían un fichero con sus nuevos métodos y lo importarían aquí
    # Lo que no me gusta mucho es que si esa contribución nueva requiere de algún nuevo atributo de clase
    # ese atributo hay que declararlo aqui y no en el fichero con los métodos nuevos.
    # Ese es el caso del atributo going, que lo tengo que declarar aqui y preferiría poder declararlo en el fichero dron_goto

    from modules.dron_connect import connect, _connect
    from modules.dron_arm import arm, _arm
    from modules.dron_takeOff import takeOff, _takeOff
    from modules.dron_RTL_Land import  RTL, Land, _goDown
    from modules.dron_nav import _prepare_command, startGo, stopGo, go, _startGo, changeHeading, fixHeading, unfixHeading, changeNavSpeed
    from modules.dron_goto import goto, _goto, _distanceToDestinationInMeters
    from modules.dron_flightPlan import executeFlightPlan, _executeFlightPlan
    from modules.dron_parameters import getParams, _getParams, setParams, _setParams
    from modules.dron_setGeofence import setGEOFence, _setGEOFence
    from modules.dron_telemetry import send_telemetry_info, _send_telemetry_info, stop_sending_telemetry_info

