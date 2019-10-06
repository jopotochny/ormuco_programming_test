from OrmucoCache.LRUCacheHandler import LRUCacheHandler
from OrmucoCache.LRUCache import LRUCache
import socketserver
class LRUCacheManager:

    def __init__(self, host, port, cache):
        class LRUCacheHandlerWithCache(LRUCacheHandler):
            CACHE = cache

        with socketserver.TCPServer((host, port), LRUCacheHandlerWithCache) as server:
            server.serve_forever()