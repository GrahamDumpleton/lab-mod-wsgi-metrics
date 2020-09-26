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

client = InfluxDBClient(influxdb_hostname, 8086, "wsgi", "wsgi", "wsgi")

interval = 1.0

hostname = socket.gethostname()

old_timestamp = None
old_processes = {}


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
    global old_timestamp
    global old_processes

    new_processes = {}

    if old_timestamp:
        period = (timestamp - old_timestamp).total_seconds()
        print("PERIOD", period)

    # Get the list of processes.

    for pid in psutil.pids():
        try:
            if pid in old_processes:
                process = new_processes[pid] = old_processes[pid]

                cpu_percent = process.cpu_percent()
                rss_memory = process.memory_info().rss

                name = process_type(process)

                if name not in ["other"]:
                    yield (pid, name, cpu_percent, rss_memory)

            else:
                process = new_processes[pid] = psutil.Process(pid)
                process.cpu_percent()

        except psutil.NoSuchProcess:
            pass

    old_timestamp = timestamp
    old_processes = new_processes


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
                "fields": {"cpu": cpu, "memory": memory},
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

        time.sleep(next_time - now)

        # If we get to here it means the process is being shutdown
        # so we report any metrics that haven't been sent.

        report_metrics()


queue = Queue()
thread = Thread(target=collector, daemon=True)

thread.start()
thread.join()
