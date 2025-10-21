import sys
from server.server import Server
from client.client import Client
from shared.config import *

def run_mode(configs):
    if configs[0] == 'server':
        print(f"Starting server on IP {configs[2]} and port {configs[1]}...")
        server = Server(**configs[1:])
    elif configs[0] == 'client':
        print(f"Starting client connecting to IP {configs[2]} and port {configs[1]}...")
        client = Client(**configs[1:])
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