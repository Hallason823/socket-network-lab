import sys
from server.server import Server
from client.client import Client
from shared.config import *

def run_mode(configs):
    params = dict(zip(['port', 'ip', 'header', 'selected_format', 'who_command', 'disconnect_message'], configs[1:]))
    if configs[0] == 'server':
        print(f"Starting server on IP {params['ip']} and port {params['port']}...")
        server = Server(**params)
    elif configs[0] == 'client':
        print(f"Starting client connecting to IP {params['ip']} and port {params['port']}...")
        client = Client(**params)
        client.start()
    else:
        print("Invalid mode. Use --mode=server or --mode=client")
        sys.exit(1)

def main():
    params = sys.argv

    if '-h' in params or '--help' in params:
        print_help()
        sys.exit(0)

    configs = get_configs(params[1:])
    run_mode(configs)

if __name__ == "__main__":
    main()