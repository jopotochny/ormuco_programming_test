import socketserver
import json
import socket
from OrmucoCache.Constants import ACTION_GET_DATA, ACTION_UPDATE_CACHE
class LRUCacheHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = json.loads(self.request.recv(4096).strip())
        action = self.data["action"]
        if action == ACTION_GET_DATA:
            value, expire_time, is_miss = self.CACHE(self.data["d"]["key"])
            self.request.sendall(value.encode('utf-8')) # we send first because no reason to delay the process requesting data
            if is_miss == 1:
                # then we missed, want to update other caches. If this is a master cache, there will be more than
                # one address in this list. If not, there will be one element which is the (HOST, PORT) of this cache's
                # master cache
                addresses = self.CACHE.get_caches_to_update()
                if len(addresses) == 1: # then this is not a master cache, want to update master cache
                    HOST = addresses[0][0]
                    PORT = addresses[0][1]
                    s = self.open_socket(HOST, PORT, socket.AF_INET, socket.SOCK_STREAM)
                    if s is not None:
                        with s:
                            data = {
                                "action": ACTION_UPDATE_CACHE,
                                "d": {
                                    "node": {
                                        "key": self.data["d"]["key"],
                                        "value": value,
                                        "expire_time": expire_time
                                    }
                                }
                            }
                            s.sendall(json.dumps(data).encode('utf-8'))
                            # TODO you can put whatever error handling you wish here by checking whether the socket
                            # responds with "0" or not, "0" being the OK signal
        elif action == ACTION_UPDATE_CACHE:
            new_node = self.data["d"]["node"]
            self.CACHE.insert_node(new_node["key"], new_node["value"], new_node["expire_time"])
            self.request.sendall("0".encode('utf-8'))
            addresses = self.CACHE.get_caches_to_update()
            if len(addresses) > 1: # then this is a master cache, needs to update its children to match it
                for address in addresses:
                    s = self.open_socket(address[0], address[1], socket.AF_INET, socket.SOCK_STREAM)
                    if s is not None:
                        with s:
                            data = {
                                "action": ACTION_UPDATE_CACHE,
                                "d": {
                                    "node": new_node
                                }
                            }
                            s.sendall(json.dumps(data).encode('utf-8'))
                            # TODO similarly to above, can do error handling here
        print(self.CACHE.mapping)
    def open_socket(self, host, port, family, socket_type):
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

