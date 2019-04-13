import sys
import glob
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("--path", help="The complete path of the generated Thrift files. Default is /home/ubuntu/drone-comms/base/gen-py.")
# args = parser.parse_args()

# if args.path:
#     path = args.path
# else:
#     path = '/home/adam/drone/drone-comms/drone/gen-py'

# sys.path.append(path)

sys.path.append('/home/adam/drone/drone-comms/drone/thrift/gen-py')

from drone import Drone

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


def main():
    # Make socket
    transport = TSocket.TSocket('localhost', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = Drone.Client(protocol)

    # Connect!
    transport.open()

    client.fly_to(14.076550, 100.614012, 50)
    print('FLYING AWAY')

    # Close!
    transport.close()


if __name__ == '__main__':
    try:
        main()
    except Thrift.TException as tx:
        print("%s" % tx.message)
        # print(f'{tx.message}')
