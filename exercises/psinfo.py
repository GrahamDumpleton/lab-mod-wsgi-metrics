import psutil
import socket
import time
import traceback
import os

from threading import Thread
from queue import Queue

from influxdb import InfluxDBClient
from datetime import datetime

session_namespace = os.environ["SESSION_NAMESPACE"]
influxdb_hostname = f"{session_namespace}-influxdb"

client = InfluxDBClient(influxdb_hostname, 8086, 'wsgi', 'wsgi', 'wsgi')

interval = 1.0

hostname = socket.gethostname()

old_timestamp = None
old_cpu_percent = {}

def process_type(process):
    if not process.cmdline():
        return "other"

    if process.cmdline()[0].startswith("httpd"):
        return "httpd"
    elif process.cmdline()[0].startswith("(wsgi:"):
        return "wsgi"
    elif process.name() in ["bombardier"]:
        return process.name()
    else:
        return "other"

def process_metrics(timestamp):
    global old_cpu_percent

    new_cpu_percent = {}

    period = (timestamp - old_timestamp).total_seconds()

    # Get the list of processes.

    processes = {pid: psutil.Process(pid) for pid in psutil.pids()}

    for pid, process in processes.items():
        try:
            new_cpu_percent[pid] = process.cpu_percent()

            if old_timestamp:
                if pid in old_cpu_percent:
                    cpu_percent = new_cpu_percent[pid] - old_cpu_times[pid]
                    cpu_percent = cpu_percent / period
                    rss_memory = process.memory_info().rss
                    yield (pid, process_type(process), cpu_percent, rss_memory)

        except psutil.NoSuchProcess:
            pass

    old_timestamp = timestamp
    old_cpu_percent = new_cpu_percent

def report_metrics():
    stop_time = datetime.now()

    data_points = []

    for pid, name, cpu, memory in process_metrics(stop_time):
        data_points.append(
            {
                "measurement": "process-info",
                "time": stop_time.isoformat(),
                "tags": {
                    "hostname": hostname,
                    "process_type": name,
                    "pid": pid,
                },
                "fields": {
                    "cpu": cpu,
                    "memory": memory
                }
            }
        )

    try:
        client.write_points(data_points)
        print(data_points)

    except Exception:
        traceback.print_exc()

def collector():
    next_time = time.time() + interval
    
    while True:
        next_time += interval
        now = time.time()

        # Waiting for next schedule time to report metrics.

        time.sleep(next_time-now)

        # If we get to here it means the process is being shutdown
        # so we report any metrics that haven't been sent.

        report_metrics()

queue = Queue()
thread = Thread(target=collector, daemon=True)

thread.start()
thread.join()
