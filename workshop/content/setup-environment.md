Before we start we need to configure Grafana to use InfluxDB as a data source and load some dashboards. To do this run the following command by clicking on the action block below.

```terminal:execute
command: setup-grafana
```

The workshop uses these action blocks for various purposes. Anytime you see such a block with an icon on the right hand side, you can click on it and it will perform the listed action for you, you do not need to enter in the commands yourself.

To verify that Grafana is running okay, open the **Grafana** dashboard tab.

```dashboard:open-dashboard
name: Grafana
```

There is no need to login to Grafana as anonymous access is enabled for viewing Grafana dashboards.

Check that the dashboards have been loaded by selecting on **Dashboards->Manage** in Grafana.

```dashboard:reload-dashboard
name: Grafana
url: {{ingress_protocol}}://{{session_namespace}}-grafana.{{ingress_domain}}{{ingress_port_suffix}}/dashboards
```

We will also be using the embedded VS Code editor later on as well, open the **Editor** dashboard tab to warm it up.

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
