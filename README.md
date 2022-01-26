# MQTT Recorder

Simple tool to record/replay MQTT data.

## Usage

```
usage: mqtt_recorder.py [-h] [--server server] [--mode mode]
                        [--input filename] [--output filename] [--realtime]
                        [--speed factor] [--delay milliseconds] [--debug]

MQTT recorder

optional arguments:
  -h, --help            show this help message and exit
  --server server       MQTT broker
  --mode mode           Mode of operation (record/replay)
  --input filename      Input file
  --output filename     Output file
  --realtime            Enable realtime replay
  --speed factor        Realtime speed factor for replay (10=10x)
  --delay milliseconds  Delay between replayed events
  --debug               Enable debugging


Examples:

# recording
./mqtt_recorder.py --server 192.168.0.1 --mode record | tee record.json

# replay in realtime
./mqtt_recorder.py --server 192.168.0.1 --mode replay --input record.json

```

# Create & activate virtual env
```
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip
pip install --upgrade pip
# install deps
pip install -r requirements.txt
```
