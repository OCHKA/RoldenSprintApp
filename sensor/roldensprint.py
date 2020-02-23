import os
import aiocoap
import logging
import asyncio
import pickle
from typing import Optional
import pynng
from pynng import Push0, Message

os.environ['AIOCOAP_CLIENT_TRANSPORT'] = 'simple6'  # Android doesn't work with udp6


class RoldenSprint:
    """
    Client for COAP-based RoldenSprintSensor device
    """

    def __init__(self, url_base: str, index: int):
        self._protocol: Optional[aiocoap.Context] = None
        self._logger = logging.getLogger(__name__)
        self._url = f'{url_base}?{index}'
        self._socket = Push0(listen=f'inproc://sensor/{index}')
        self._loop = asyncio.new_event_loop()

    def run(self):
        while True:
            rotations = self._loop.run_until_complete(self.poll())
            if not rotations:
                continue

            msg = pynng.Message(pickle.dumps(rotations))
            try:
                self._socket.send_msg(msg)
            except pynng.exceptions.Closed:  # socket was closed, time to stop
                return

    def stop(self):
        self._socket.close()

    async def poll(self) -> Optional[int]:
        if not self._protocol:
            self._protocol = await aiocoap.Context.create_client_context()

        request = aiocoap.Message(code=aiocoap.GET, uri=self._url)
        response = await self._protocol.request(request).response

        payload = response.payload
        if payload and len(payload) == 4:
            return int.from_bytes(payload, 'little', signed=False)
        else:
            logging.warning("invalid response with len: ", len(payload))
