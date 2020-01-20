import threading
import asyncio
import time
import sys

import aiocoap


class CoapSensor(threading.Thread):
    daemon = True

    __stop_event = threading.Event()
    __event_loop = asyncio.new_event_loop()
    __protocol = None
    __nodes = []

    def __init__(self, poll_freq: int, urls: [str]):
        super(CoapSensor, self).__init__()

        self.__poll_freq = poll_freq

        for url in urls:
            self.__nodes.append({'url': url, 'rpm': 0})

    def run(self) -> None:
        self.__event_loop.run_until_complete(self.init())

        while not self.__stop_event.is_set():
            responses = self.__event_loop.run_until_complete(self.poll())

            for idx, response in enumerate(responses):
                if not response.payload:
                    print("coap: invalid query")
                    continue
                self.__nodes[idx]['rpm'] = self.parse_rpm_from_response(response.payload)

            time.sleep(1 / self.__poll_freq)  # TODO: test under load, constantly polling

    async def init(self):
        self.__protocol = await aiocoap.Context.create_client_context()

    async def poll(self) -> []:
        polls = []

        for node in self.__nodes:
            polls.append(self.poll_node(node['url']))

            try:
                return await asyncio.gather(*polls)
            except Exception as e:
                print(e, file=sys.stderr)
                return []

    async def poll_node(self, url):
        request = aiocoap.Message(code=aiocoap.GET, uri=url)
        return await self.__protocol.request(request).response

    @staticmethod
    def parse_rpm_from_response(payload):
        if len(payload) != 4:
            print("coap: invalid length: ", len(payload))

        avg_period = int.from_bytes(payload, 'little', signed=False)
        return int(1e6 / avg_period * 60)

    def stop(self):
        self.__stop_event.set()

    @property
    def rpm(self) -> list:
        values = []
        for node in self.__nodes:
            values.append(node['rpm'])
        return values

    @property
    def poll_freq(self) -> int:
        return self.__poll_freq
