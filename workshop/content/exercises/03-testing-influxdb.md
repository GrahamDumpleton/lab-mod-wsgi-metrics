```terminal:execute
command: pip install influxdb
```

```editor:insert-lines-before-line
file: ~/exercises/hello-world/wsgi.py
line: 1
text: |
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
command: mod_wsgi-express start-server hello-world/wsgi.py
```

```terminal:execute
command: siege -t 60s -c 10 http://localhost:8000
```
