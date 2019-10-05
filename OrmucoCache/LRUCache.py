from OrmucoCache.CacheNode import CacheNode
from datetime import datetime, timedelta
class LRUCache:
    def __init__(self, value_function, max_size=512, expiration_time=604800):
        '''

        :param value_function: A function that will get the value of a key, for use in the case of a cache miss. This
        would do something like go to the database, etc.
        :param max_size: the maximum number of nodes the cache should hold
        :param expiration_time: the time in seconds that a node should remain in the cache for
        '''
        self.mapping = {}
        self.value_function = value_function
        self.max_size = max_size
        self.expiration_time = expiration_time
        self.root = CacheNode(None, None, None, None, None)
        self.root.prev_node = self.root.next_node = self.root

    def __call__(self, *key):
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
            last_node = self.root.prev_node
            last_node.next_node = self.root.prev_node = node
            node.prev_node = last_node
            node.next_node = self.root
            self.remove_expired_nodes()
            return node.value, 0
        else:
            value = self.value_function(*key)
            if len(self.mapping) >= self.max_size:
                oldest_node = self.root.prev_node
                second_oldest_node = oldest_node.prev_node
                second_oldest_node.next_node = self.root
                del self.mapping[oldest_node.key]
            last_node = self.root.next_node
            last_node.prev_node = self.root.next_node = self.mapping[key] = CacheNode(self.root, last_node, key, value, datetime.now() + timedelta(self.expiration_time))
            self.remove_expired_nodes()
            return value, 1
    def update_cache(self, new_mapping):
        self.mapping = new_mapping
    def remove_expired_nodes(self):
        '''
        removes all expired nodes from the circular doubly linked list

        because the oldest node is always root_node.prev_node (we insert nodes from the front of the list), we can check
        from there to potentially save computation. if we come across a node that is not expired we know that the others wont
        be expired either
        '''
        now = datetime.now()
        current_node = self.root.prev_node
        while current_node.expire_time is not None: # if it is none then we have circled back to root
            if current_node.expire_time >= now:
                next_node = current_node.next_node
                prev_node = current_node.prev_node
                next_node.prev_node = prev_node
                prev_node.next_node = next_node
                del self.mapping[current_node.key]
                current_node = prev_node
            else:
                break
if __name__ == '__main__':
    p = LRUCache()
    for c in 'abcdecaeaa':
        print(c, p(c))