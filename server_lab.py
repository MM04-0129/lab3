import socket
import threading
import time


class TupleSpace:
    def __init__(self):
        self.tuples = {}
        self.stats = {
            'tuple_count': 0,
            'average_tuple_size': 0,
            'average_key_size': 0,
            'average_value_size': 0,
            'total_clients': 0,
            'total_operations': 0,
            'total_READs': 0,
            'total_GETs': 0,
            'total_PUTs': 0,
            'total_errors': 0
        }
        self.lock = threading.Lock()
def read(self, key):
        with self.lock:
            if key in self.tuples:
                self.stats['total_READs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {self.tuples[key]}) read"
            else:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} does not exist"
def get(self, key):
        with self.lock:
            if key in self.tuples:
                value = self.tuples.pop(key)
                self.stats['tuple_count'] -= 1
                self.stats['total_GETs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {value}) removed"
            else:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} does not exist"
def put(self, key, value):
        with self.lock:
            if key in self.tuples:
                self.stats['total_errors'] += 1
                self.stats['total_operations'] += 1
                return f"ERR {key} already exists"
            else:
                self.tuples[key] = value
                self.stats['tuple_count'] += 1
                self.stats['total_PUTs'] += 1
                self.stats['total_operations'] += 1
                return f"OK ({key}, {value}) added"
