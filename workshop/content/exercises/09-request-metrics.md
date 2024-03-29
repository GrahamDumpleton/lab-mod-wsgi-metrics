```editor:open-file
file: ~/exercises/hello-world-v7/wsgi.py
```

```editor:open-file
file: ~/exercises/hello-world-v7/metrics.py
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v7/wsgi.py --log-to-terminal --working-directory hello-world-v7
clear: true
```

```terminal:execute
command: bombardier -d 300s -c 3 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://grafana-{{session_namespace}}.{{ingress_domain}}{{ingress_port_suffix}}/d/request-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v7/wsgi.py --log-to-terminal --working-directory hello-world-v7 --disable-reloading --queue-timeout=0
```

```terminal:execute
command: bombardier -d 300s -c 3 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://grafana-{{session_namespace}}.{{ingress_domain}}{{ingress_port_suffix}}/d/request-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```

```terminal:execute
command: mod_wsgi-express start-server hello-world-v7/wsgi.py --log-to-terminal --working-directory hello-world-v7 --processes=1 --threads=1 --embedded-mode
```

```terminal:execute
command: bombardier -d 300s -c 3 http://localhost:8000
session: 2
```

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://grafana-{{session_namespace}}.{{ingress_domain}}{{ingress_port_suffix}}/d/request-metrics?orgId=1&refresh=5s
```

```terminal:interrupt-all
```
