# Socket Network Lab

A computer networking lab project using TCP sockets. Includes basic implementations of client, server, and shared code.

## Project Structure

```plaintext
socket-network-lab/
├── client/           # Client code
│   └── client.py
├── server/           # Server code
│   └── server.py
└── shared/           # Shared modules and utilities
    └── config.py
```

## Features

- TCP server and client implementations
- Support for broadcast and direct messaging
- User nickname registration and management
- Commands to list connected users and disconnect
- Configurable via command-line parameters

## Requirements

- Python 3.x
- No external dependencies (uses built-in `socket` and `threading` modules)

## Usage

Run the server:

```bash
python main.py --mode=server --server-port=<server-port>
```

Run the client:
```bash
python main.py --mode=client --server-ip=<server-ip> --server-port=<server-port>
```

For help:

```bash
python main.py -h
```

or

```bash
python main.py --help
```

# Configuration Parameters

| Parameter             | Description                         | Default                       |
|-----------------------|-------------------------------------|-------------------------------|
| `--mode`              | Run as server or client             | `server`                      |
| `--server-port`       | Port number                         | Random between 1024 and 49151 |
| `--server-ip`         | IP address                          | Local machine IP              |
| `--header`            | Message length header size (bytes)  | 64                            |
| `--selected-format`   | Encoding format                     | `utf-8`                       |
| `--who_message`       | Command to list users               | `!WHO`                        |
| `--disconnect_message`| Command to disconnect               | `!QUIT`                       |

# How it works

- The server waits for client connections, manages connected users, and routes messages.
- The client connects to the server, sends/receives messages, and supports commands like listing users and quitting.
- Communication is done with message headers defining message lengths.

# Authors

- Arthur Azevedo
- David Mendes
- Deivson Ricardo
- Hallason Matias
- Wilson Pereira
