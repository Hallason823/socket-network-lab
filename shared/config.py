import random
import socket

PARAMETERS_NAME = ['--mode', '--server-port', '--server-ip', '--header', '--selected-format', '--who_message', '--disconnect_message'] 
DEFAULT_VALUES = ['server', random.randint(1024, 49151), socket.gethostbyname(socket.gethostname()), 64, 'utf-8', "!WHO", "!QUIT"]
TYPES = ['string', 'int', 'string', 'int'] + ['string']*3
HELP_TEXT = """
Usage: python main.py [OPTIONS]

Options:
  --mode=server|client          Choose to run as server or client (default: server)
  --server-port=PORT            Set the port number for the server/client (default: random between 1024-49151)
  --server-ip=IP                Set the IP address for the server/client (default: local machine IP)
  --header=NUM                  Number of bytes to represent message length (default: 64)
  --selected-format=FORMAT      Encoding format for messages (default: utf-8)
  --who_message=COMMAND         Command to list connected users (default: !WHO)
  --disconnect_message=COMMAND  Command to disconnect (default: !QUIT)
  -h, --help                    Show this help message and exit

Examples:
  python main.py --mode=server --server-port=5050
  python main.py --mode=client --server-ip=192.168.0.10 --server-port=5050
"""

def print_help():
    print(HELP_TEXT)

def print_error(error):
    if error == True:
        print_help()
        exit(1)

def set_parameter(args, param_name, default_value, s_type):
    param = None
    for arg in args:
         if arg.startswith(param_name + '='):
            if s_type == 'int':
                param = int(arg.split('=')[1])
            else:
                param = arg.split('=')[1]
    return param if param is not None else default_value

def get_configs(args):
    return [set_parameter(args, parameter_name, default_value, s_type) for parameter_name, default_value, s_type in zip(PARAMETERS_NAME, DEFAULT_VALUES, TYPES)]