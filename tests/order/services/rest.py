"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from aiohttp import (
    web,
)

from minos.saga import (
    SagaManager,
)


class RestService(object):
    saga_manager: SagaManager

    async def add_order(self, request, **kwargs):
        uuid = await self.saga_manager.run("UpdateOrder")
        return web.Response(text=f"Order added: {uuid!r}")

    async def get_order(self, request, **kwargs):
        return web.Response(text="Order get")
