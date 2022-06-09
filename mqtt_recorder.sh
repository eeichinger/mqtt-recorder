#!/bin/sh

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
CMD="$@"

echo "scriptdir:$SCRIPT_DIR"
echo "cmd:$CMD"

# force complete rebuild:
# docker build --pull --no-cache  --tag mqtt_recorder .
docker build --pull --tag mqtt_recorder .
docker run -it --rm --network="host" -v "$PWD":/usr/src/app mqtt_recorder python ./mqtt_recorder.py $CMD
