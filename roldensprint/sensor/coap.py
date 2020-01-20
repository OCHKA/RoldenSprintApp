import threading
import asyncio
import time

import aiocoap


class CoapSensor(threading.Thread):
    daemon = True

    __rpm = 0
    __stop_event = threading.Event()
    __protocol = None
    __event_loop = asyncio.new_event_loop()

    def __init__(self, base_url):
        super(CoapSensor, self).__init__()
        self._base_url = base_url

    def run(self) -> None:
        self.__event_loop.run_until_complete(self.init())

        while not self.__stop_event.is_set():
            self.__event_loop.run_until_complete(self.poll())
            time.sleep(1 / 10)  # TODO: test under load, constantly polling

    async def init(self):
        self.__protocol = await aiocoap.Context.create_client_context()

    async def poll(self) -> None:
        request = aiocoap.Message(code=aiocoap.GET, uri=f'coap://{self._base_url}?0')

        try:
            response = await self.__protocol.request(request).response
        except Exception as e:
            print('coap:', e)
        else:
            if response.payload:  # TODO: implement proper error handling
                self.handle_response(response.payload)

    def handle_response(self, response):
        if len(response) != 4:
            print("invalid length:", len(response))

        avg_period = int.from_bytes(response, 'little', signed=False)
        if avg_period:
            self.__rpm = int(1e6 / avg_period * 60)

    def stop(self):
        self.__stop_event.set()

    @property
    def rpm(self) -> int:
        return self.__rpm
