from __future__ import annotations

import json

from helloworld.core.mailing.services import AbstractSender
from helloworld.core.messaging import AbstractProducer
from helloworld.core.mailing.services.priority import Priority

class SMTPSender(AbstractSender):

    def init(self):
        return self

    async def send(self, to: str, subject: str, body: str, **kwargs) -> None:
        data = {
            "to": to,
            "subject": subject,
            "body": body
        }
        # await self.producer.send(priority, json.dumps(data).encode("utf-8"))
        print(data)