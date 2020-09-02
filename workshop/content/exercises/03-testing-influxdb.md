```terminal:execute
command: pip install influxdb
```

```editor:open-file
file: ~/exercises/hello-world-v2/wsgi.py
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @hello-world-v2/dashboard.json http://localhost:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v2/wsgi.py
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.training.getwarped.org/d/hello-world-v2/raw-requests?orgId=1&refresh=5s
```

```editor:open-file
file: ~/exercises/hello-world-v2/wsgi.py
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @hello-world-v3/dashboard.json http://localhost:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v3/wsgi.py
```

```terminal:execute
command: siege -t 300s -c 10 -d 0.1 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.training.getwarped.org/d/hello-world-v3/server-aggregated?orgId=1&refresh=5s
```
