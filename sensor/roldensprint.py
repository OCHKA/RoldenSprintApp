import os
import time
import aiocoap
import logging
import asyncio
import threading
from typing import Optional

from message.io_service import IoService

os.environ['AIOCOAP_CLIENT_TRANSPORT'] = 'simple6'  # Android doesn't work with udp6


class RoldenSprintSensor(threading.Thread):
    """
    Client for COAP-based RoldenSprintSensor device
    """

    def __init__(self, topic: str, url_base: str, index: int, max_poll_rate: int = 30, **kwargs):
        super().__init__(name=__name__, **kwargs)

        self._logger = logging.getLogger(__name__)
        self._io = IoService(__name__)
        self._topic = topic

        self._coap: Optional[aiocoap.Context] = None
        self._url = f'{url_base}?{index}'

        self._loop = asyncio.new_event_loop()

        self._max_poll_rate = max_poll_rate
        self._stop_requested = False

    def __del__(self):
        self.stop()

    def run(self):
        self._stop_requested = False

        self._io.start()

        while not self._stop_requested:
            start_time = time.time()

            # forward sensor data
            rotations = self._loop.run_until_complete(self.poll())
            if rotations:
                self._io.publish(self._topic, rotations)

            # wait for next run
            max_poll_time = 1 / self._max_poll_rate
            used_time = time.time() - start_time
            unused_time = max_poll_time - used_time

            if unused_time > 0:
                time.sleep(unused_time)

    def stop(self):
        self._stop_requested = True
        self._io.stop()
        self._loop.stop()

    async def poll(self) -> Optional[int]:
        if not self._coap:
            self._coap = await aiocoap.Context.create_client_context()

        request = aiocoap.Message(code=aiocoap.GET, uri=self._url)
        response = await self._coap.request(request).response

        payload = response.payload
        if payload and len(payload) == 4:
            return int.from_bytes(payload, 'little', signed=False)
        else:
            logging.warning("invalid response with len: ", len(payload))
