import threading
import paho.mqtt.client as mqtt
import json
import logging
import time

BROKER_URL = 'localhost'
BROKER_PORT = 1883


def topic_dots_to_slashes(func):
    def decorator(instance, topic: str, *args, **kwargs):
        topic = topic.replace('.', '/')
        return func(instance, topic, *args, **kwargs)
    return decorator


def handle_exception(func):
    def decorator(instance, *args, **kwargs):
        try:
            return func(instance, *args, **kwargs)
        except Exception as exception:
            logging.error(f"IoService: {exception}\nComponent: {instance.name}", exc_info=True)
            instance.stop()
    return decorator


class IoService(threading.Thread):
    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)

        self._name = name
        self._callbacks = {}

        self._client = mqtt.Client(f"{name}-{int(time.time() * 1000)} ")
        self._client.on_message = self._on_message
        self._client.connect(BROKER_URL, BROKER_PORT)

        self.subscribe('shutdown', self.stop)

    def __del__(self):
        self.stop()

    def run(self):
        return self._client.loop_forever()

    def stop(self, message=""):
        self._client.disconnect()
        if message:
            logging.info(f"IoService: stop {self._name} '{message}'")

    @property
    def name(self):
        return self._name

    @topic_dots_to_slashes
    def publish(self, topic: str, **kwargs):
        payload_json = json.dumps(kwargs)
        self._client.publish(topic, payload_json)

    @topic_dots_to_slashes
    def subscribe(self, topic: str, callback: callable):
        self._callbacks[topic] = callback
        self._client.subscribe(topic)

    @handle_exception
    def _on_message(self, client, userdata, msg):
        callback = self._callbacks.get(msg.topic, None)
        if callback:
            payload = json.loads(msg.payload, encoding='ascii')
            callback(**payload)
