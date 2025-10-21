import random
import socket

PARAMETERS_NAME = ['--mode', '--server-port', '--server-ip', '--header', '--selected-format', '--who_message', '--disconnect_message'] 
DEFAULT_VALUES = ['server', random.randint(1024, 49151), socket.gethostbyname(socket.gethostname()), 64, 'utf-8', "!WHO", "!QUIT"]
TYPES = ['string', 'int', 'string', 'int'] + ['string']*3

def print_help():
    print('\nUsage: python main.py [OPTIONS]\n')

def print_error(error):
    if error == True:
        print_help()
        exit(1)

def set_parameter(args, param_name, default_value, type):
    param = None
    for arg in args:
         if arg.startswith(param_name + '='):
            if type_ == 'int':
                param = int(arg.split('=')[1])
            else:
                param = arg.split('=')[1]
    return param if param is not None else default_value

def get_configs(args):
    return [set_parameter(args, parameter_name, default_value, s_type) for parameter_name, default_value, s_type in zip(PARAMETERS_NAME, DEFAULT_VALUES, TYPES)]