```editor:open-file
file: ~/exercises/hello-world-v7/wsgi.py
```

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/request-metrics.json http://{{session_namespace}}-grafana:3000/api/dashboards/db
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v7/wsgi.py --log-to-terminal --working-directory hello-world-v7
```

```terminal:execute
command: siege -t 300s -c 10 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}/d/request-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
