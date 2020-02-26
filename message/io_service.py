import threading
import paho.mqtt.client as mqtt

BROKER_URL = 'localhost'
BROKER_PORT = 1883


def topic_dots_to_slashes(func):
    def decorator(instance, topic: str, *args, **kwargs):
        topic = topic.replace('.', '/')
        return func(instance, topic, *args, **kwargs)
    return decorator


class IoService(threading.Thread):
    def __init__(self, name: str,  **kwargs):
        super().__init__(name=f'{name}.io_service', **kwargs)

        self._callbacks = {}

        self._client = mqtt.Client()
        self._client.on_message = self._on_message
        self._client.connect(BROKER_URL, BROKER_PORT)

    def __del__(self):
        self.stop()

    def run(self) -> None:
        self._client.loop_forever()

    def stop(self):
        self._client.disconnect()

    @topic_dots_to_slashes
    def publish(self, topic: str, payload):
        self._client.publish(topic, payload)

    @topic_dots_to_slashes
    def subscribe(self, topic: str, callback: callable):
        self._callbacks[topic] = callback
        self._client.subscribe(topic)

    def _on_message(self, client, userdata, msg):
        callback = self._callbacks.get(msg.topic, None)
        if callback:
            callback(msg.payload)
