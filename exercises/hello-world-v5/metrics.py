import socket
import threading
import queue
import time
import os

from threading import Thread
from queue import Queue

import wrapt

import mod_wsgi

from influxdb import InfluxDBClient

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

interval = 1.0

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

lock = threading.Lock()
data_points = []

@wrapt.synchronized(lock)
def record_metric(stop_time, duration):
    global data_points

    timestamp = int(1000000000*stop_time-epoch)

    data_points.append(
        f"wsgi.requests,hostname={hostname},process={process} application_time={duration} {timestamp}"
    )

def report_metrics():
    global data_points

    with wrapt.synchronized(lock):
        pending_data_points = data_points
        data_points = []

    if pending_data_points:
        client.write_points(pending_data_points, batch_size=10000, protocol='line')

def shutdown_handler(name, **kwargs):
    queue.put(None)

def collector():
    mod_wsgi.request_metrics()
    next_time = time.time() + interval
    
    while True:
        next_time += interval
        now = time.time()

        try:
            queue.get(timeout=next_time-now)
            report_metrics()
            return

        except Exception:
            pass

        report_metrics()

queue = Queue()
thread = Thread(target=collector)

def enable_reporting():
    mod_wsgi.subscribe_shutdown(shutdown_handler)
    thread.start()

class WSGIApplicationIterable(wrapt.ObjectProxy):

    def __init__(self, wrapped, start_time):
        super().__init__(wrapped)
        self._self_start_time = start_time

    def close(self):
        if hasattr(self.__wrapped__, 'close'):
            self.__wrapped__.close()

        stop_time = time.time()
        duration = stop_time - self._self_start_time

        record_metric(stop_time, duration)

@wrapt.decorator
def wsgi_application(wrapped, instance, args, kwargs):
    start_time = time.time()

    try:
        return WSGIApplicationIterable(wrapped(*args, **kwargs), start_time)

    except:
        stop_time = time.time()
        duration = stop_time - start_time

        record_metric(stop_time, duration)

        raise
