import socketserver
import sys
import json
from OrmucoCache.LRUCache import LRUCache
from OrmucoCache.LRUCacheHandler import LRUCacheHandler
from OrmucoCache.LRUCacheManager import LRUCacheManager
from threading import Thread

def value_function(a):
    return a

def create_manager(host, port, max_size, caches_to_update):
    cache = LRUCache(value_function=value_function, max_size=max_size,
                     caches_to_update=caches_to_update)
    manager = LRUCacheManager(host, port, cache)
if __name__ == "__main__":
    HOST, PORTS = "localhost", [9990, 9991, 9992]
    update_list = [[(HOST, 9991), (HOST, 9992)], [(HOST, 9990)], [(HOST, 9990)]]
    # create_manager(HOST, PORTS[0], 4096, update_list[0])
    # create_manager(HOST, PORTS[1], 4096, update_list[1])
    create_manager(HOST, PORTS[2], 4096, update_list[2])



    # for i in range(len(PORTS)):
    #     thread = Thread(target=create_manager, args=(HOST, PORTS[i], 4096, update_list[i]))
    #     thread.start()
    #     thread.join()
    # print("thread finished...exiting")