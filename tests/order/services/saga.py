"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    CommandReply,
)


class SagaService(object):
    async def add_order(self, topic: str, command: CommandReply):
        return "add_order_saga"

    async def delete_order(self, topic: str, command: CommandReply):
        return "delete_order_saga"
