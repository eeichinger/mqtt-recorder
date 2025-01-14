#!/usr/bin/env -S python3 -u

"""MQTT recorder"""

import argparse
import asyncio
import base64
import json
import logging
import os
import signal
import sys
import time
import dateutil.parser

from hbmqtt.client import QOS_0, QOS_1, MQTTClient

TOPICS = [("#", QOS_1)]

logger = logging.getLogger('mqtt_recorder')

async def mqtt_record(server: str, clientid: str, output: str = None) -> None:
    """Record MQTT messages"""
    mqtt = MQTTClient(clientid)
    await mqtt.connect(server)
    await mqtt.subscribe(TOPICS)
    if output is not None:
        output_file = open(output, 'wt')
    else:
        output_file = sys.stdout
    while True:
        message = await mqtt.deliver_message()
        tst=time.strftime("%Y-%m-%dT%H:%M:%S.%s%z", time.localtime())
        record = {
            'tst': tst,
            'qos': message.qos,
            'retain': 1 if message.retain else 0,
            'topic': message.topic,
            'payloadlen': len(message.data),
            'payload': json.loads(message.data)
        }
        recjson=json.dumps(record)
        print(recjson, file=output_file, flush=True)


async def mqtt_replay(server: str, clientid: str, input: str = None, delay: int = 0, realtime: bool = False, scale: float = 1, loop: int = 1) -> None:
    """Replay MQTT messages"""
    mqtt = MQTTClient(clientid)
    await mqtt.connect(server)
    await mqtt.subscribe(TOPICS)

    if (loop < 0):
        loop = sys.maxsize

    for it in range(0, loop):
        logger.info("loop count: %s of %s", it, loop)

        if input is not None:
            input_file = open(input, 'rt')
        else:
            input_file = sys.stdin
        if delay > 0:
            static_delay_s = delay / 1000
        else:
            static_delay_s = 0
        last_timestamp = None
        for line in input_file:
            if line.startswith('#'):
                logger.info("ignore: %s", line)
                continue

            record = json.loads(line)
            if 'msg_b64' in record:
                msg = base64.urlsafe_b64decode(record['msg_b64'].encode())
            elif 'msg' in record:
                msg = record['msg'].encode()
            elif 'payload' in record:
                msg = json.dumps(record['payload']).encode()
            else:
                logger.warning("Missing message attribute: %s", record)
                next
            delay_s = static_delay_s
            tststr=dateutil.parser.isoparse(record['tst'].replace('Z+', '+'))
            tst=tststr.timestamp()
            if realtime or scale != 1:
                delay_s += (tst - last_timestamp if last_timestamp else 0) * scale
                last_timestamp = tst
            if delay_s > 0:
                logger.info("Sleeping %.3f seconds", delay_s)
                await asyncio.sleep(delay_s)
            logger.info("publish: %s", record)
            await mqtt.publish(record['topic'], msg,
                               retain=record.get('retain'),
                               qos=record.get('qos', QOS_0))
        # wait for last message to be published
        input_file.close()

    await asyncio.sleep(2)

async def shutdown(sig, loop):
    loop.stop()
    os._exit(-1)


def main():
    """ Main function"""
    parser = argparse.ArgumentParser(description='MQTT recorder')

    parser.add_argument('--server',
                        dest='server',
                        metavar='server',
                        help='MQTT broker',
                        default='mqtt://127.0.0.1:1883/')
    parser.add_argument('--clientid',
                        dest='clientid',
                        metavar='clientid',
                        help='MQTT Client-ID',
                        default=None)
    parser.add_argument('--mode',
                        dest='mode',
                        metavar='mode',
                        choices=['record', 'replay'],
                        help='Mode of operation (record/replay)',
                        default='record')
    parser.add_argument('--input',
                        dest='input',
                        metavar='filename',
                        help='Input file')
    parser.add_argument('--output',
                        dest='output',
                        metavar='filename',
                        help='Output file')
    parser.add_argument('--realtime',
                        dest='realtime',
                        action='store_true',
                        help="Enable realtime replay")
    parser.add_argument('--speed',
                        dest='speed',
                        type=float,
                        default=1,
                        metavar='factor',
                        help='Realtime speed factor for replay (10=10x)')
    parser.add_argument('--delay',
                        dest='delay',
                        type=int,
                        default=0,
                        metavar='milliseconds',
                        help='Delay between replayed events')
    parser.add_argument('--loop',
                        dest='loop',
                        metavar='loop',
                        type=int,
                        default=1,
                        help='repeat replay script. Set -1 for infinite')
    parser.add_argument('--debug',
                        dest='debug',
                        action='store_true',
                        help="Enable debugging")

    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.mode == 'replay':
        process = mqtt_replay(server=args.server, clientid=args.clientid, input=args.input,
                              delay=args.delay, realtime=args.realtime,
                              scale=1 / args.speed, loop=args.loop)
    else:
        process = mqtt_record(server=args.server, clientid=args.clientid, output=args.output)

    loop = asyncio.get_event_loop()
    for s in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(s, lambda: asyncio.ensure_future(shutdown(s, loop)))

    loop.run_until_complete(process)


if __name__ == "__main__":
    main()
