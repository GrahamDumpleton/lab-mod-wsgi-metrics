One of the great things about InfluxDB is it's ability to ingest individual events or metrics, as opposed to only working with aggregated metrics. Because you have access to distinct values for each event, HTTP requests in our case, it is possible to go back over the data and generate calculated metrics such as percentiles, which require access to all the original data to calculate.

In the examples we have been using so far, each time a HTTP request occurred we immediately reported a metric back to InfluxDB. This means that for every inbound HTTP request being handled by our application, we were creating an outbound request to InfluxDB. This has a significant cost and since our WSGI application was just a hello world application, the overhead of sending the data to InfluxDB was way more than that of our application. This approach has therefore been dramatically affecting the potential throughput of our application.

The recommended approach to avoid this when working with InfluxDB is to batch up data, and only periodically report it.

```editor:open-file
file: ~/exercises/hello-world-v4/metrics.py
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def record_metric\\(.*\\):"
  filesToInclude: hello-world-v4/metrics.py
  isRegex: true
```

```editor:execute-command
command: workbench.action.findInFiles
args:
- query: "def report_metrics\\(.*\\):"
  filesToInclude: hello-world-v4/metrics.py
  isRegex: true
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v4/wsgi.py --log-to-terminal --working-directory hello-world-v4
```

```terminal:execute
command: bombardier -d 120s -c 5 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v5/wsgi.py --log-to-terminal --working-directory hello-world-v5
```

```terminal:execute
command: bombardier -d 120s -c 5 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/raw-requests?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
