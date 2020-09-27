import socket
import threading
import queue
import time
import atexit
import traceback
import os

from threading import Thread
from queue import Queue

import wrapt

import mod_wsgi

from influxdb import InfluxDBClient
from datetime import timedelta

session_namespace = os.environ["SESSION_NAMESPACE"]
influxdb_hostname = f"{session_namespace}-influxdb"

client = InfluxDBClient(influxdb_hostname, 8086, 'wsgi', 'wsgi', 'wsgi')

interval = 1.0

hostname = socket.gethostname()
pid = os.getpid()

process = f"{hostname}:{pid}"

lock = threading.Lock()
data_points = []

@wrapt.synchronized(lock)
def record_metric(stop_time, duration):
    """Records a single metric, adding it to a list to later be sent
    to InfluxDB in a batch.

    """

    global data_points

    timestamp = int(stop_time.total_seconds() * 1000000000)

    # Metric is added as a formatted string record to the list of data
    # points with the list of strings later being passed to the InfluxDB
    # client to report.

    data_points.append(
        f"raw-requests,hostname={hostname},process={process} application_time={duration} {timestamp}"
    )

def report_metrics():
    """Report the current batch of metrics to InfluxDB.

    """

    global data_points

    # Set aside the current batch of metrics and initialize the list
    # used to collect metrics to empty again.

    with wrapt.synchronized(lock):
        pending_data_points = data_points
        data_points = []

    # Report the complete batch of metrics to InfluxDB in one go.

    if pending_data_points:
        try:
            client.write_points(pending_data_points, batch_size=10000, protocol='line')
        except Exception:
            traceback.print_exc()

def collector():
    next_time = time.time() + interval
    
    while True:
        next_time += interval
        now = time.time()

        try:
            # Waiting for next schedule time to report metrics.

            queue.get(timeout=max(0, next_time-now))

            # If we get to here it means the process is being shutdown
            # so we report any metrics that haven't been sent.

            report_metrics()

            return

        except Exception:
            # Timeout occurred on waiting on queue, which means the next
            # reporting time has arrived.

            pass

        # Report the current batch of metrics.

        report_metrics()

queue = Queue()
thread = Thread(target=collector, daemon=True)

def shutdown_handler(*args, **kwargs):
    queue.put(None)
    thread.join(timeout=3.0)

def enable_reporting():
    """Subscribe to shutdown of the application so we can report the last
    batch of metrics and notify the collector thread to shutdown.

    """

    if hasattr(mod_wsgi, "subscribe_shutdown"):
        mod_wsgi.subscribe_shutdown(shutdown_handler)
    else:
        atexit.register(shutdown_handler)

    # Start collector thread for periodically reporting accumlated metrics.

    thread.start()

def event_handler(name, **kwargs):
    """Record a metric for each request when finished. These will be batched
    up and periodically sent to InfluxDB.

    """

    if name == 'request_finished':
        stop_time = timedelta(seconds=kwargs["application_finish"])
        duration = kwargs["application_time"]

        record_metric(stop_time, duration)

mod_wsgi.subscribe_events(event_handler)
