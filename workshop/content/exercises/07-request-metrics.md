```editor:open-file
file: ~/exercises/hello-world-v6/wsgi.py
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/server-metrics.json http://localhost:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v6/wsgi.py --log-to-terminal
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.training.getwarped.org/d/server-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
