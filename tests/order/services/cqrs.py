"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Event,
)


class CqrsService(object):
    async def ticket_added(self, topic: str, event: Event):
        return "request_added"

    async def ticket_deleted(self, topic: str, event: Event):
        return "ticket_deleted"
