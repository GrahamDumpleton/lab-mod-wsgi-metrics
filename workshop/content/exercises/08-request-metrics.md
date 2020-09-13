```editor:open-file
file: ~/exercises/hello-world-v7/wsgi.py
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
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/d/request-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
