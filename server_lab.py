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

