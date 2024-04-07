import argparse
import json
import time
from typing import Dict, Optional

from pymavlink import mavutil
'''from utilities.connect_to_sysid import connect_to_sysid
from utilities.get_autopilot_info import get_autopilot_info
'''

def upload_qgc_mission(the_connection):
    mission = {
        "takeOffAlt": 5,
        "waypoints":
            [
                {
                    'lat': 41.2763410,
                    'lon': 1.9888285,
                    'alt': 12
                },
                {
                    'lat': 41.2762977,
                    'lon': 1.9885401,
                    'alt': 14
                }
            ]

    }

    takOffAlt = mission['takeOffAlt']

    waypoints = mission['waypoints']

    # preparamos la misión para cargarla en el dron

    wploader = []
    seq = 0  # Waypoint sequence begins at 0
    # El primer wp debe ser la home position.
    # Averiguamos la home position
    the_connection.mav.command_long_send(
        the_connection.target_system,
        the_connection.target_component,
        mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,
        0, 0, 0, 0, 0, 0, 0, 0)

    msg = the_connection.recv_match(type='HOME_POSITION', blocking=True)
    msg = msg.to_dict()
    lat = msg['latitude']
    lon = msg['longitude']
    alt = msg['altitude']

    # añadimos este primer waypoint a la mision
    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        0, 0, seq, 0, 16, 0, 0, 0, 0, 0, 0,
        lat,
        lon,
        alt
    ))
    seq = 1

    # El siguiente elemento de la mision debe ser el comando de takeOff, en el que debemos indicar una posición
    # que será también la home position

    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        the_connection.target_system, the_connection.target_component, seq,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, True,
        0, 0, 0, 0,
        lat, alt, takOffAlt
    ))
    seq = 2

    # Ahora añadimos los waypoints de la ruta
    for wp in waypoints:
        wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
            the_connection.target_system, the_connection.target_component, seq,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, True,
            0, 0, 0, 0,
            int(wp["lat"] * 10 ** 7), int(wp["lon"] * 10 ** 7), int(wp["alt"])
        ))
        seq += 1  # Increase waypoint sequence for the next waypoint
    # añadimos para acabar un RTL
    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        the_connection.target_system, the_connection.target_component, seq,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_RETURN_TO_LAUNCH, 0, True,
        0, 0, 0, 0,
        0, 0, 0
    ))
    return upload_mission(the_connection, wploader)

def upload_qgc_mission2(the_connection):
    """
    Upload a mission to UAV.

    Args:
        mission_file (str): The path to the mission file.
        the_connection (mavutil.mavlink_connection): The MAVLink connection to use.

    Returns:
        bool: True if the mission is successfully uploaded, False otherwise.
        None: If the mission file couldn't be read.
    """
    '''autopilot_info = get_autopilot_info(the_connection, sysid)
    autopilot = autopilot_info["autopilot"]
    print(f"Autopilot: {autopilot}")'''
    mission_file = 'mission'
    mission = read_qgc_mission(mission_file)
    if not mission:
        print ('error')
        return None
    print ('ok')
    # Create MAVLink waypoint loader
    wploader = []

    seq = 0  # Waypoint sequence begins at 0

    the_connection.mav.command_long_send(
        the_connection.target_system,
        the_connection.target_component,
        mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,
        0, 0, 0, 0, 0, 0, 0, 0)

    msg = the_connection.recv_match(type='HOME_POSITION', blocking=True)
    msg = msg.to_dict()
    lat = msg['latitude']
    lon = msg['longitude']
    alt = msg['altitude']
      # print('POS ', lat, lon, alt)

    '''lat = float(msg['latitude'] / 10 ** 7)
    lon = float(msg['longitude'] / 10 ** 7)
    alt = float(msg['altitude'] / 1000)
    # print('POS ', lat, lon, alt)'''

    # Adding home position waypoint for Ardupilot
    add_home_position_waypoint(wploader, lat, lon, alt, seq)
    seq += 1  # Increase waypoint sequence

    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        the_connection.target_system, the_connection.target_component, seq,
        3, mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, True,
        0, 0, 0, 0, lat, alt, 19
    ))



    seq += 1  # Increase waypoint sequence
    # Add all waypoints from mission to MAVLink waypoint loader
    for wp in mission["mission"]["items"]:
        print(wp)
        add_waypoint(wploader, the_connection, wp, seq)
        seq += 1  # Increase waypoint sequence for the next waypoint

    return upload_mission(the_connection, wploader)


def read_qgc_mission(mission_file: str) -> Dict:
    """
    Read a mission file from QGroundControl.

    Args:
        mission_file (str): The path to the mission file.

    Returns:
        dict: A dictionary containing the mission details, or empty dict if file not found.
    """
    try:
        with open(mission_file, 'r') as file:
            mission = json.load(file)
    except FileNotFoundError:
        print(f"Mission file {mission_file} not found.")
        return {}

    return mission


def add_home_position_waypoint(wploader: list,lat, lon, alt, seq: int) -> None:
    """
    Adds home position waypoint to the wploader list.

    Args:
        wploader (list): The waypoint loader list.
        mission (dict): The mission details.
        seq (int): The waypoint sequence.
    """
    '''the_connection.mav.command_long_send(
        the_connection.target_system,
        the_connection.target_component,
        mavutil.mavlink.MAV_CMD_GET_HOME_POSITION,
        0, 0, 0, 0, 0, 0, 0, 0)

    msg = the_connection.recv_match(type='HOME_POSITION', blocking=True)
    msg = msg.to_dict()

    lat = float(msg['latitude'] / 10 ** 7)
    lon = float(msg['longitude'] / 10 ** 7)
    alt = float(msg['altitude'] / 1000)
    #print('POS ', lat, lon, alt)'''

    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
           0, 0, seq, 0, 16, 0, 0, 0, 0, 0, 0,
           lat,
           lon,
           alt
    ))

    ''' wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        0, 0, seq, 0, 16, 0, 0, 0, 0, 0, 0,
        int(mission["mission"]["plannedHomePosition"][0] * 10 ** 7),
        int(mission["mission"]["plannedHomePosition"][1] * 10 ** 7),
        int(mission["mission"]["plannedHomePosition"][2])
    ))'''


def add_waypoint(wploader: list, master: mavutil.mavlink_connection, wp: Dict, seq: int) -> None:
    """
    Adds a waypoint to the wploader list.

    Args:
        wploader (list): The waypoint loader list.
        master (mavutil.mavlink_connection): The MAVLink connection to use.
        wp (dict): The waypoint details.
        seq (int): The waypoint sequence.
    """
    wploader.append(mavutil.mavlink.MAVLink_mission_item_int_message(
        master.target_system, master.target_component, seq, wp["frame"], wp["command"], 0, int(wp["autoContinue"]),
        float(wp["params"][0]), float(wp["params"][1]), float(wp["params"][2]),
        float(wp["params"][3]), int(wp["params"][4] * 10 ** 7), int(wp["params"][5] * 10 ** 7),
        int(wp["params"][6])
    ))


def upload_mission(master: mavutil.mavlink_connection, wploader: list) -> bool:
    """
    Upload the mission to the UAV.

    Args:
        master (mavutil.mavlink_connection): The MAVLink connection to use.
        wploader (list): The waypoint loader list.

    Returns:
        bool: True if the mission is successfully uploaded, False otherwise.
    """
    # Clear any existing mission from vehicle
    print('Clearing mission')
    master.mav.mission_clear_all_send(master.target_system, master.target_component)

    if not verify_ack(master, 'Error clearing mission'):
        return False

    # Send waypoint count to the UAV
    master.waypoint_count_send(len(wploader))

    # Upload waypoints to the UAV
    return send_waypoints(master, wploader)


def verify_ack(master: mavutil.mavlink_connection, error_msg: str) -> bool:
    """
    Verifies the ack response.

    Args:
        master (mavutil.mavlink_connection): The MAVLink connection to use.
        error_msg (str): The error message to log if ack verification fails.

    Returns:
        bool: True if ack verification successful, False otherwise.
    """
    ack = master.recv_match(type='MISSION_ACK', blocking=True, timeout=3)
    print(ack)
    if ack.type != 0:
        print(f'{error_msg}: {ack.type}')
        return False
    return True


def send_waypoints(master: mavutil.mavlink_connection, wploader: list) -> bool:
    """
    Send the waypoints to the UAV.

    Args:
        master (mavutil.mavlink_connection): The MAVLink connection to use.
        wploader (list): The waypoint loader list.

    Returns:
        bool: True if waypoints are successfully sent, False otherwise.
    """
    for i in range(len(wploader)):
        msg = master.recv_match(type=['MISSION_REQUEST_INT', 'MISSION_REQUEST'], blocking=True, timeout=3)
        if not msg:
            print('No waypoint request received')
            return False
        print(f'Sending waypoint {msg.seq}/{len(wploader) - 1}')
        master.mav.send(wploader[msg.seq])

        if msg.seq == len(wploader) - 1:
            break

    return verify_ack(master, 'Error uploading mission')


def ack (the_connection, keyword):
    print ('***** -> ' + str (the_connection.recv_match(type = keyword, blocking = True)))

if __name__ == '__main__':
    # Parser for command-line arguments
    parser = argparse.ArgumentParser(description='Upload a mission created by QGroundControl to a vehicle.')

    # Add mission_file argument
    parser.add_argument('--mission_file', type=str, default='wps/CMAC_square.plan',
                        help='Path to the mission file.')

    # Add address argument
    parser.add_argument('--address', type=str, default='udpin:localhost:14551',
                        help='The address and port to connect to.')

    # Parse the arguments
    args = parser.parse_args()
    connection_string = 'tcp:127.0.0.1:5763'
    baud = 115200
    the_connection = mavutil.mavlink_connection(connection_string, baud)
    the_connection.wait_heartbeat()

    print(f"Heartbeat from system (system {the_connection.target_system} component {the_connection.target_component})")




    # Upload the mission to the UAV
    upload_qgc_mission(the_connection)
    print ('listo')

    mode = 'GUIDED'
    # Get mode ID
    mode_id = the_connection.mode_mapping()[mode]
    the_connection.mav.set_mode_send(
        the_connection.target_system,
        mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
        mode_id)
    arm_msg = the_connection.recv_match(type='COMMAND_ACK', blocking=True, timeout=3)
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    the_connection.motors_armed_wait()
    '''aTargetAltitude =15
    the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                       mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, aTargetAltitude)
    ack (the_connection, 'COMMAND_ACK')'''
    '''time.sleep (15)
    while True:
        msg = the_connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        # print('meg ', msg)
        if msg:
            msg = msg.to_dict()
            alt = float(msg['relative_alt'] / 1000)
            print (alt)
            if alt >= aTargetAltitude * 0.90:
                print("Reached target altitude")
                break
        time.sleep(2)'''
    the_connection.mav.command_long_send(
        the_connection.target_system,
        the_connection.target_component,
        mavutil.mavlink.MAV_CMD_MISSION_START,
        0, 0, 0, 0, 0, 0, 0, 0)