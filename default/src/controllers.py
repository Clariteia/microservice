"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.common import (
    Request,
    Response,
)

from .dto import (
    FooDto,
    FoosQueryDto,
)
from .services import FooService


class FooController:
    """Ticket Controller class"""

    @staticmethod
    async def create_foo(request: Request) -> Response:
        """TODO

        :param request:TODO
        :return: TODO
        """
        content = await request.content()
        foo = await FooService().create_foo(**content[0])
        return Response(foo)

    @staticmethod
    async def get_foos(request: Request) -> Response:
        """TODO

        :param request: TODO
        :return: TODO
        """
        content = await request.content()
        if len(content) and isinstance(content[0], FoosQueryDto):
            content = content[0].ids
        foos = [FooDto.from_dict(foo.avro_data) for foo in await FooService().get_foos(content)]
        return Response(foos)
