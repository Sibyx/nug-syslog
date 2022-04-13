import asyncio
import logging
import re
import sqlite3
import uuid
from argparse import Namespace
from asyncio import DatagramProtocol

from nug_syslog import version


class SyslogServer(DatagramProtocol):
    def __init__(self, config: Namespace):
        self._db = sqlite3.connect(config.database)
        self._re = re.compile(r"<(?P<level>[0-9]{2})>(?P<message>.*)\x00")

    def datagram_received(self, data, addr):
        message = data.decode()
        logging.debug(f'Received {message} from {addr}')

        data = self._re.match(message)
        level = int(data.group(1)) % 8
        message = data.group(2)

        cursor = self._db.cursor()
        cursor.execute(
            "insert into logs (id, host, level, message, created_at, updated_at) "
            "values (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (str(uuid.uuid4()), addr[0], level, message)
        )
        cursor.close()
        self._db.commit()

    @classmethod
    async def start(cls, config: Namespace):
        logging.info(f"Starting nug-syslog v{version.__version__}")
        loop = asyncio.get_running_loop()

        transport, protocol = await loop.create_datagram_endpoint(
            lambda: cls(config),
            local_addr=(str(config.bind), config.port)
        )

        logging.info(f"Started nug-syslog v{version.__version__} on {config.bind}:{config.port}")

