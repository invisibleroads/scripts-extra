#!/bin/env python
import socket
from sys import argv


def is_port_in_use(port):
    # https://stackoverflow.com/a/52872579
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', int(port))) == 0


minimum_port, maximum_port = argv[1:]
minimum_port = int(minimum_port)
maximum_port = int(maximum_port)
for port in range(minimum_port, maximum_port + 1):
    is_in_use = is_port_in_use(port)
    if is_in_use:
        print(f'{port} is being used')
