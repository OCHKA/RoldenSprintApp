import threading
import asyncio
import time

import aiocoap


class CoapPeriodSensor(threading.Thread):
    daemon = True

    __rpm = 0
    __stop_event = threading.Event()
    __protocol = None
    __event_loop = asyncio.new_event_loop()

    def run(self) -> None:
        while not self.__stop_event.is_set():
            self.__event_loop.run_until_complete(self.async_request())
            time.sleep(1)  # TODO: test under load, constantly polling

    async def async_request(self) -> None:
        protocol = await aiocoap.Context.create_client_context()
        request = aiocoap.Message(code=aiocoap.GET, uri='coap://192.168.1.149/period?0')

        try:
            response = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            if response.payload:  # TODO: implement proper error handling
                self.handle_response(response.payload)

    def handle_response(self, response):
        periods = response.split(b'\xFF')

        period_sum = 0
        count = 0
        for period in periods:
            if len(period) == 4:
                period_sum += int.from_bytes(period, 'big', signed=False)
                count += 1
            else:
                print(len(period))

        if count:
            self.__rpm = int(period_sum / count)

    def stop(self):
        self.__stop_event.set()

    @property
    def rpm(self) -> int:
        return self.__rpm
