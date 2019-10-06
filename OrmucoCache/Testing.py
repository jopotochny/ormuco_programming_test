import socket
from OrmucoCache.Constants import ACTION_GET_DATA
import json
def open_socket(host, port, family, socket_type):
    s = None
    for res in socket.getaddrinfo(host, port, family, socket_type):
        af, socktype, proto, canonname, sa = res
        try:
            s = socket.socket(af, socktype, proto)
        except OSError as msg:
            s = None
            continue
        try:
            s.connect(sa)
        except OSError as msg:
            s.close()
            s = None
            continue
        break
    return s

s = open_socket("localhost", 9992, socket.AF_INET, socket.SOCK_STREAM)
if s is not None:
    d = {
        "action": ACTION_GET_DATA,
        "d": {
            "key": "apples",
        }
    }
    s.sendall(json.dumps(d).encode('utf-8'))