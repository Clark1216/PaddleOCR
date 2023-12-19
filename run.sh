#!/bin/bash

# disable x server access control for graphical output
xhost +

# disable CPU clockdown
echo 100 | tee /sys/devices/system/cpu/intel_pstate/min_perf_pct

# startup containers
export VERSION="$(cat version.txt)"
export COMPOSE_PROJECT_NAME="$(cat project_name.txt)"
docker-compose up -d
