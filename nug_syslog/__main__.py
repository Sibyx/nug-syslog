import argparse
import asyncio
import logging
import pathlib
from ipaddress import ip_address

from nug_syslog.server import SyslogServer

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--log-level', type=str, choices=logging._nameToLevel.keys(), default='INFO')
    parser.add_argument(
        '--bind', '-b', type=ip_address, default=ip_address('127.0.0.1'),
    )
    parser.add_argument('--port', '-p', type=int, default=514)
    parser.add_argument('--database', type=pathlib.Path)
    args = parser.parse_args()

    logging.getLogger().setLevel(args.log_level)
    if args.verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%S%z'
        ))
        logging.getLogger().addHandler(stream_handler)

    try:
        loop = asyncio.new_event_loop()
        loop.run_until_complete(SyslogServer.start(args))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
