# MQTT Recorder

This project is a fork from https://github.com/kirei/mqtt-recorder. There is a similar tool here https://github.com/rpdswtk/mqtt_recorder

Advantage of this project:

- uses a file format compatible with mosquitto_sub/mosquitto_pub cli tools
- adds the option to control replay speed (via --realtime, --speed or --delay options)

Downside:
- as of now uses an outdated lib `hbmqtt` which doesn't work with python>3.7 and doesn't support TLS connections 


Simple tool to record/replay MQTT data compatible with format produced by mosquitto_sub

```
$>mosquitto_sub -v -h 127.0.0.1 -p 1883 -i mqtt-cli-4663d4e5 -c -t '#' -F %J

{"tst":"2022-01-24T14:57:18.902850Z+0100","topic":"f/i/stock","qos":0,"retain":0,"payloadlen":765,"payload":{"ts":"2022-01-24T13:57:15.631Z","stockItems":[{"workpiece":{"id":"0","state":"","type":""},"location":"A1"},{"workpiece":{"id":"04c34892186581","state":"RAW","type":"WHITE"},"location":"A2"},{"workpiece":{"id":"04c34892186582","state":"RAW","type":"WHITE"},"location":"A3"},{"workpiece":{"id":"046a5ba2186581","state":"RAW","type":"RED"},"location":"B1"},{"workpiece":{"id":"04c34892186584","state":"RAW","type":"RED"},"location":"B2"},{"workpiece":{"id":"04c34892186585","state":"RAW","type":"RED"},"location":"B3"},{"workpiece":{"id":"040467a2186581","state":"RAW","type":"BLUE"},"location":"C1"},{"workpiece":{"id":"047e6da2186580","state":"RAW","type":"BLUE"},"location":"C2"},{"workpiece":{"id":"04c34892186588","state":"RAW","type":"BLUE"},"location":"C3"}]}}
```


## NOTE

Currently this tool requires python 3.7. It will *not* work with later versions!

## Usage

**NOTE:** Make sure you have create your local python environment, see "Manage Python Environment" below

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

# Manage Python Environment

## Install python 3.7
Make sure you have v3.7 installed. You can use pyenv to manage python versions, see https://github.com/pyenv/pyenv.

TL;DR on MacOS:
```shell
# install pyenv
brew install pyenv

# install desired python version
pyenv install 3.7.12

#add to ~/.bash_profile:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
```

## Create virtual environment and install dependencies

```shell
python3 -m venv .venv
source .venv/bin/activate

# upgrade pip
pip install --upgrade pip
# install deps
pip install -r requirements.txt
```
