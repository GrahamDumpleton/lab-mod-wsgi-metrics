import atexit
import time

import mod_wsgi

from threading import Thread
from queue import Queue

from influxdb import InfluxDBClient
from datetime import datetime

client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

queue = Queue()

interval = 1.0

def collector():
    mod_wsgi.request_metrics()
    next_time = time.time() + interval
    while True:
        next_time += interval
        now = time.time()

        try:
            return queue.get(timeout=next_time-now)
        except Exception:
            pass

        metrics = mod_wsgi.request_metrics()

        stop_time = datetime.fromtimestamp(metrics["stop_time"]).isoformat()

        client.write_points([
            {
                "measurement": "wsgi.server",
                "time": stop_time,
                "fields": {
                    "request_rate": metrics["request_rate"],
                    "utilization": metrics["utilization"],
                    "server_time": metrics["server_time"],
                    "application_time": metrics["application_time"],
                    "cpu_user_time": metrics["cpu_user_time"],
                    "cpu_system_time": metrics["cpu_system_time"],
                    "threads_maximum": metrics["threads_maximum"],
                    "threads_initialized": metrics["threads_initialized"],
                    "active_threads": metrics["active_threads"],
                    "active_requests": metrics["active_requests"]
                }
            }
        ])

thread = Thread(target=collector)
thread.start()

def event_handler(name, **kwargs):
    if name == 'process_stopping':
        queue.put(None)

mod_wsgi.subscribe_events(event_handler)

def application(environ, start_response):
    status = '200 OK'
    output = b'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]
