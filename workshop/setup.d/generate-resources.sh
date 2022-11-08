#!/bin/bash

INFLUXDB_HOST=influxdb-workshop
export INFLUXDB_HOST

envsubst < exercises/grafana/datasource.json.in > exercises/grafana/datasource.json
