"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    Command,
)
from tests.order import (
    Order,
)


class CommandService(object):
    async def get_order(self, topic: str, command: Command):
        return "get_order"

    async def add_order(self, topic: str, command: Command):
        return [Order(1, 1, "bar", 3)]

    async def delete_order(self, topic: str, command: Command):
        return [Order(1, 1, "bar", 3), Order(2, 1, "foobar", 6)]

    async def update_order(self, topic: str, command: Command):
        return "update_order"
