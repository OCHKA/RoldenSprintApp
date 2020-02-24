import os
import time
import aiocoap
import logging
import asyncio
import pickle
from typing import Optional
import pynng

os.environ['AIOCOAP_CLIENT_TRANSPORT'] = 'simple6'  # Android doesn't work with udp6


class RoldenSprint:
    """
    Client for COAP-based RoldenSprintSensor device
    """

    def __init__(self, url_base: str, index: int, max_poll_rate: int = 30):
        self._coap: Optional[aiocoap.Context] = None
        self._logger = logging.getLogger(__name__)
        self._url = f'{url_base}?{index}'
        self._topic = f'sensor/{index}'.encode('ascii')
        self._interface = pynng.Pub0(listen='inproc://roldensprint')
        self._loop = asyncio.new_event_loop()
        self._max_poll_rate = max_poll_rate

    def run(self):
        while True:
            start_time = time.time()
            rotations = self._loop.run_until_complete(self.poll())
            if not rotations:
                continue

            try:
                self._interface.send(self._topic + pickle.dumps(rotations))
            except pynng.exceptions.Closed:  # socket was closed, time to stop
                return

            max_poll_time = 1 / self._max_poll_rate
            used_time = time.time() - start_time
            unused_time = max_poll_time - used_time
            if unused_time > 0:
                time.sleep(unused_time)

    def stop(self):
        # TODO: _protocol too
        self._interface.close()

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
