import socket
import sys
import json
HOST = "localhost"
PORT = 9998
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM):
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
if s is None:
    print("we fucked up")
    sys.exit(1)
with s:
    data = {}
    data["key"] = "1234"
    data["value"] = "hello"
    s.sendall(json.dumps(data).encode("utf-8"))
    resp = s.recv(4096)
print(repr(resp))