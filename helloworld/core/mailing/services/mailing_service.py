from __future__ import annotations

from typing import Type, List, Tuple

from jinja2 import Environment, DictLoader

from helloworld.core.mailing.services.abstract_sender import AbstractSender
from .priority import Priority, PRIORITY_ORDER

class Template:
    name: str
    content: str
    lang: str

    def __init__(self, name: str, lang: str, content: str):
        self.name = name
        self.content = content
        self.lang = lang


async def render_template(template: Template, **kwargs):
    loader = DictLoader({template.name: template.content})
    env = Environment(loader=loader)

    jinja_template = env.get_template(template.name)

    return jinja_template.render(**kwargs)


class TemplateManager:
    templates: List[Template]
    _service: MailingService

    def __init__(self, service: MailingService) -> None:
        self.templates = []
        self._service = service

    def register(self, template: Template) -> MailingService:
        if self.find(template.name, template.lang) is not None:
            raise ValueError(f"A template with name '{template.name}' and lang '{template.lang}' already exists.")

        self.templates.append(template)
        return self._service

    def find(self, name: str, lang: str) -> Template | None:
        for template in self.templates:
            if template.name == name and template.lang == lang:
                return template

        return None


class SenderManager:
    senders: List[Tuple[AbstractSender, Priority]]
    _service: MailingService

    def __init__(self, service: MailingService) -> None:
        self.senders = []
        self._service = service

    def register(self, sender: Type[AbstractSender], priority: Priority = "medium", *args, **kwargs) -> MailingService:
        obj = sender()
        obj.init(*args, **kwargs)
        self.senders.append((obj, priority))

        return self._service

    def find_by_priority(self, desired_priority: Priority) -> AbstractSender | None:
        desired_index = PRIORITY_ORDER.index(desired_priority)
        sorted_senders = sorted(self.senders, key=lambda x: PRIORITY_ORDER.index(x[1]))

        for sender, sender_priority in sorted_senders:
            if sender_priority == desired_priority:
                return sender

        for priority in PRIORITY_ORDER[:desired_index + 1]:
            for sender, sender_priority in sorted_senders:
                if sender_priority == priority:
                    return sender

        return None


class MailingService:
    templates: TemplateManager
    senders: SenderManager

    def __init__(self) -> None:
        self.templates = TemplateManager(self)
        self.senders = SenderManager(self)

    def init(self) -> MailingService:
        return self

    async def send(self, template: str, lang: str, to: str, subject: str, priority: Priority = "medium", **kwargs):
        _template = self.templates.find(template, lang)
        if not _template:
            raise ValueError(f"Template '{template}', lang '{lang}' not registered.")

        body = await render_template(_template, **kwargs)

        sender = self.senders.find_by_priority(priority)
        await sender.send(to=to, subject=subject, body=body, **{"priority": priority})