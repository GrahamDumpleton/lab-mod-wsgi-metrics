During the workshop we will be using InfluxDB to capture metrics from mod_wsgi and Grafana to graph the results.

Before we start we need to configure Grafana to use InfluxDB as a data source. To do this run the following command by clicking on the action block below.

```terminal:execute
command: |
    curl -H "Content-Type: application/json" --user admin:admin --data @grafana/datasource.json http://localhost:3000/api/datasources
```

The workshop uses these action blocks for various purposes. Anytime you see such a block with an icon on the right hand side, you can click on it and it will perform the listed action for you.

To verify that the data source has been correctly configured, open the **Grafana** dashboard tab.

```dashboard:open-dashboard
name: Grafana
```

Login to Grafana. The username is `admin`, and the password is also `admin`.

> NOTE: Do not set a new password as later on we will be running scripts which connect to Grafana and they rely on the default credentials being used. So when prompted to provide a new password, click on **Skip**.

Now click on **Configuration->Data Sources** in the Grafana view, or click below.

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.training.getwarped.org/datasources
```

You should have a single data source called **WSGI**, which is associated with InfluxDB.

We will also be using the embedded editor later on as well, open the **Editor** dashboard tab to start it up.

```dashboard:open-dashboard
name: Editor
```

Finally, return back to the **Terminal** dashboard tab:

```dashboard:open-dashboard
name: Terminal
```

Clear the terminals so we are ready to go.

```terminal:clear-all
```
