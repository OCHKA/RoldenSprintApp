import asyncio
import aiocoap


class CoapSensor:
    _protocol = None

    def __init__(self, url: str):
        self._url = url

    async def poll(self):
        if not self._protocol:
            self._protocol = await aiocoap.Context.create_client_context()

        request = aiocoap.Message(code=aiocoap.GET, uri=self._url)
        response = await self._protocol.request(request).response

        payload = response.payload
        if payload and len(payload) == 4:
            return int.from_bytes(payload, 'little', signed=False)
        else:
            print("coap: invalid response with len: ", len(payload))
