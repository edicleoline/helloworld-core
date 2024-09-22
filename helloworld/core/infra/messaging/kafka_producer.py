from __future__ import annotations

from aiokafka import AIOKafkaProducer

from helloworld.core.messaging import AbstractProducer

class KafkaProducer(AbstractProducer[AIOKafkaProducer, bytes]):
    producer: AIOKafkaProducer | None
    bootstrap_servers: str | None

    def init(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None

        return self

    async def start(self) -> AIOKafkaProducer:
        if not self.producer:
            self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
            await self.producer.start()
        return self.producer

    async def send(self, topic: str, message: bytes):
        if not self.producer:
            raise RuntimeError("Producer not initialized. Call 'start' first.")

        await self.producer.send_and_wait(topic, message)

    async def stop(self):
        if self.producer:
            await self.producer.stop()