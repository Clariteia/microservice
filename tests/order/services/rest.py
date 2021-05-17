"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from aiohttp import (
    web, )


class RestService(object):
    async def add_order(self, request):
        return web.Response(text="Order added")

    async def get_order(self, request):
        return web.Response(text="Order get")
