```terminal:execute
command: pip install influxdb
```

```editor:insert-lines-before-line
file: ~/exercises/hello-world/wsgi.py
line: 1
text: |+
    import mod_wsgi

    from influxdb import InfluxDBClient
    from datetime import datetime

    client = InfluxDBClient('localhost', 8086, 'wsgi', 'wsgi', 'wsgi')

    def event_handler(name, **kwargs):
        if name == 'request_finished':
            client.write_points([
                {
                    "measurement": "application_time",
                    "time": datetime.now().isoformat(),
                    "fields": {
                        "value": kwargs["application_time"]
                    }
                }
            ])

    mod_wsgi.subscribe_events(event_handler)

...
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @hello-world/dashboard1.json http://localhost:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world/wsgi.py
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:open-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.training.getwarped.org/d/dashboard1/raw-requests?orgId=1&refresh=5s
```
