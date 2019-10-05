import socketserver
import json
from OrmucoCache.Constants import ACTION_GET_DATA, ACTION_UPDATE_CACHE
from OrmucoCache.LRUCache import LRUCache
class LRUCacheMasterHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = json.loads(self.request.recv(4096).strip())
        action = self.data["action"]
        if action == ACTION_GET_DATA:
            d = cache(self.data["d"]["key"])
            print(d)
            self.request.sendall(d.encode('utf-8'))
        elif action == ACTION_UPDATE_CACHE:
            cache.update_cache(self.data["d"])
            self.request.sendall("0".encode('utf-8'))
if __name__ == "__main__":
    HOST, PORT = "localhost", 9998
    cache = LRUCache(max_size=4096)
    with socketserver.TCPServer((HOST, PORT), LRUCacheMasterHandler) as server:
        server.serve_forever()
