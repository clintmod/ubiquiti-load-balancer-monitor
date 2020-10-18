#! /usr/bin/env bash

set -e

./scripts/uptime_via_telnet.sh $1 2>&1 > /dev/null

cat workdir/uptime.txt | head -2 | tail -1 | awk '{print $1}'
