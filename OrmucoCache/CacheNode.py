from datetime import datetime
class CacheNode:
    def __init__(self, prev_node, next_node, key, value, expire_time):
        self.prev_node = prev_node
        self.next_node = next_node
        self.key = key
        self.value = value
        self.expire_time = expire_time

    def is_expired(self):
        if self.expire_time is None:
            # then this node is the root
            return False
        return self.expire_time <= datetime.now()