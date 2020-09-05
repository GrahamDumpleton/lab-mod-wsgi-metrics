import socket
import threading
import os

import wrapt

import mod_wsgi

from influxdb import InfluxDBClient
from datetime import datetime

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

    data_points.append(
        {
            "measurement": "wsgi.requests",
            "time": stop_time.isoformat(),
            "tags": {
                "hostname": hostname,
                "process": process
            },
            "fields": {
                "application_time": duration
            }
        }
    )

def report_metrics():
    global data_points

    with wrapt.synchronized(lock):
        pending_data_points = data_points
        data_points = []

    if pending_data_points:
        client.write_points(pending_data_points)

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

thread = threading.Thread(target=collector)

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

        stop_time = datetime.now()
        duration = (stop_time - self._self_start_time).total_seconds()

        record_metric(stop_time, duration)

@wrapt.decorator
def wsgi_application(wrapped, instance, args, kwargs):
    start_time = datetime.now()

    try:
        return WSGIApplicationIterable(wrapped(*args, **kwargs), start_time)

    except:
        stop_time = datetime.now()
        duration = (stop_time - start_time).total_seconds()

        record_metric(stop_time, duration)

        raise
