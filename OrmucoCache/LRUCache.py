from OrmucoCache.CacheNode import CacheNode
from datetime import datetime, timedelta
class LRUCache:
    def __init__(self, value_function, caches_to_update, max_size=512, expiration_time=604800):
        '''

        :param value_function: A function that will get the value of a key, for use in the case of a cache miss. This
        would do something like go to the database, etc.
        :param max_size: the maximum number of nodes the cache should hold
        :param expiration_time: the time in seconds that a node should remain in the cache for
        :param caches_to_update: a tuple of the form (HOST, PORT) for connecting to this cache's master cache. If None,
        then this cache is a master cache
        '''
        self.mapping = {}
        self.value_function = value_function
        self.max_size = max_size
        self.expiration_time = expiration_time
        self.root = CacheNode(None, None, None, None, None)
        self.root.prev_node = self.root.next_node = self.root
        self.caches_to_update = caches_to_update

    def __call__(self, key):
        '''

        :param key: the key of the item we want to get the value of from the cache
        :return: the value associated with the key, and either 0 if it was a cache hit or 1 if it was a miss
        '''
        node = self.mapping.get(key)
        if node is not None:
            prev_node = node.prev_node
            next_node = prev_node.next_node
            prev_node.next_node = next_node
            next_node.prev_node = prev_node
            most_recently_accessed_node = self.root.next_node
            most_recently_accessed_node.prev_node = self.root.next_node = node
            node.prev_node = self.root
            node.next_node = most_recently_accessed_node
            self.remove_expired_nodes()
            return node.value, node.expire_time, 0
        else:
            value = self.value_function(key)
            if len(self.mapping) >= self.max_size:
                self.remove_LRU_node()
            last_node = self.root.next_node
            last_node.prev_node = self.root.next_node = self.mapping[key] = CacheNode(self.root, last_node, key, value, (datetime.now() + timedelta(self.expiration_time)).timestamp())
            self.remove_expired_nodes()
            return value, self.root.next_node.expire_time, 1
    def insert_node(self, key, value, expire_time):
        root_next = self.root.next_node
        new_node = CacheNode(self.root, root_next, key, value, expire_time)
        root_next.prev_node = new_node
        self.root.next_node = new_node
        if len(self.mapping) >= self.max_size:
            self.remove_LRU_node()
        self.mapping[key] = new_node
    def remove_LRU_node(self):
        oldest_node = self.root.prev_node
        second_oldest_node = oldest_node.prev_node
        second_oldest_node.next_node = self.root
        del self.mapping[oldest_node.key]
    def remove_expired_nodes(self):
        '''
        removes all expired nodes from the circular doubly linked list
        '''
        now = datetime.now().timestamp()
        current_node = self.root.prev_node
        while current_node.expire_time is not None: # if it is none then we have circled back to root
            if current_node.expire_time <= now:
                next_node = current_node.next_node
                prev_node = current_node.prev_node
                next_node.prev_node = prev_node
                prev_node.next_node = next_node
                del self.mapping[current_node.key]
                current_node = prev_node
            else:
                current_node = current_node.prev_node
    def get_caches_to_update(self):
        return self.caches_to_update
if __name__ == '__main__':
    p = LRUCache()
    for c in 'abcdecaeaa':
        print(c, p(c))