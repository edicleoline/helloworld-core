from __future__ import annotations

import json

from helloworld.core.mailing.services import AbstractSender
from helloworld.core.messaging import AbstractProducer
from helloworld.core.mailing.services.priority import Priority

class KafkaSender(AbstractSender):
    producer: AbstractProducer | None

    def init(self, producer: AbstractProducer):
        self.producer = producer
        return self

    async def send(self, to: str, subject: str, body: str, priority: Priority = "medium") -> None:
        data = {
            "to": to,
            "subject": subject,
            "body": body
        }
        await self.producer.send(priority, json.dumps(data).encode("utf-8"))
        pass