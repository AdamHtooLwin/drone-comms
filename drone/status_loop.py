"""
This script retrieves the vehicle's status then encodes it as JSON and POSTs it to the web app
Loops on a x-interval.
"""

from dronekit import connect, VehicleMode
import time
import argparse
import json
import requests
import datetime

# Parsing args
parser = argparse.ArgumentParser()
parser.add_argument("connection", help="The connection string to be used, i.e. the Pixhawk")
args = parser.parse_args()

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (args.connection,))
vehicle = connect(args.connection, wait_ready=True)

print("")

while True:
    # Get some vehicle attributes (state)
    print ("Autopilot Firmware version: %s" % vehicle.version)
    print "Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp
    print ("Home Location: %s" % vehicle.home_location)
    print "Global Location: %s" % vehicle.location.global_frame
    print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print "Local Location: %s" % vehicle.location.local_frame    #NED
    print "Attitude: %s" % vehicle.attitude
    print "Velocity: %s" % vehicle.velocity
    print "GPS: %s" % vehicle.gps_0
    print "Groundspeed: %s" % vehicle.groundspeed
    print "Airspeed: %s" % vehicle.airspeed
    print "Gimbal status: %s" % vehicle.gimbal
    print "Battery: %s" % vehicle.battery
    print "EKF OK?: %s" % vehicle.ekf_ok
    print "Last Heartbeat: %s" % vehicle.last_heartbeat
    print "Rangefinder: %s" % vehicle.rangefinder
    print "Rangefinder distance: %s" % vehicle.rangefinder.distance
    print "Rangefinder voltage: %s" % vehicle.rangefinder.voltage
    print "Heading: %s" % vehicle.heading
    print "Is Armable?: %s" % vehicle.is_armable
    print "System status: %s" % vehicle.system_status.state
    print "Mode: %s" % vehicle.mode.name    # settable
    print "Armed: %s" % vehicle.armed    # settable

    nav_logs = {
    "gps_latitude": vehicle.location.global_relative_frame.lat,
    "gps_longitude": vehicle.location.global_relative_frame.lon,
    "altitude": vehicle.location.global_relative_frame.alt,
    "drone_id": 1,
    }

    print("")
    print("Posting with this navlog")
    print(nav_logs)
    print("")

    print("Posting navlogs")

    nav_post = requests.post("http://3.0.21.193/api/v1/nav_logs", data=nav_logs)

    print("")

    # Hold for 5 seconds
    print("Waiting for 5 seconds")
    time.sleep(5)
