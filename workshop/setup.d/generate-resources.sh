#!/bin/bash

INFLUXDB_HOST=$SESSION_NAMESPACE-influxdb
export INFLUXDB_HOST

envsubst < exercises/grafana/datasource.json.in > exercises/grafana/datasource.json
