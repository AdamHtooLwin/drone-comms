import sys
import glob
import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--drone_id", help="The ID of the drone, default is 2 i.e. the real drone; put 1 for simulator")
parser.add_argument("--ait", help="Set to 1 to make destination ait main gate")
parser.add_argument("--port", help="The port to which the thrift socket must connect. Default is 9090.")
parser.add_argument("--path", help="The complete path of the generated Thrift files. Default is /home/ubuntu/drone-comms/base/gen-py.")
parser.add_argument("--user", help="The user profile name. This will be used in the path to the generated Thrift files. Default is ubuntu.")
args = parser.parse_args()


# TODO
if args.ait:
    dest_latitude = 14.076550
    dest_longitude = 100.614012
#

drone_id = 2
if args.drone_id:
    drone_id = args.drone_id

drone_endpoint = "https://teamdronex.com/api/v1/drone/%s" % drone_id

if args.path:
    path = args.path
else:
    path = '/home/ubuntu/drone-comms/drone/thrift/gen-py'

if args.user:
    user = args.user
    path = '/home/{}/drone-comms/drone/thrift/gen-py'.format(user)

else:
    user = "ubuntu"

sys.path.append(path)

port = 9090
if args.port:
    port = args.port

# sys.path.append('/home/adam/drone/drone-comms/drone/thrift/gen-py')

from drone import Drone

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', port)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Drone.Client(protocol)

    # Connect!
    transport.open()
    
    print("Checking status...")
    client.check_status()

    # Close!
    transport.close()

if __name__ == '__main__':
    try:
        main()

        success_drone_status_data = {
            "status": "Available"
        }

        success_drone_patch = requests.patch(drone_endpoint, data=success_drone_status_data) 
    except Thrift.TException as tx:
        print("ERROR!\n")
        print("%s" % tx.message)

        error_drone_status_data = {
            "status": "Unable to connect"
        }

        error_drone_patch = requests.patch(drone_endpoint, data=error_drone_status_data)  
        # print(f'{tx.message}')
