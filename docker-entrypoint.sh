#!/bin/sh
set -e

# Make endernewton object detector
# make -C sfmt/endernewton

# Create directories and files
mkdir -p logs

# build sfmt-videocap
# cd video_cap2020
# python3 setup.py install

# build sfmt-streamsync
# cd stream_sync2020
# python3 setup.py install

cd /paddle

# Change permissions
# (comment out if you want to run the docker processes as root)
#chown -R sfmt:sfmt logs

# Step down to non-root user with gosu
# (comment out if you want to run the docker processes as root)
#exec gosu sfmt:sfmt "$@"

exec "$@"
