"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import UUID

from minos.common import (
    Service,
)
from minos.saga import SagaContext

from .aggregates import (
    Foo,
)
from .dto import BarsQueryDto


class FooService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_foo(bar) -> Foo:
        """TODO.

        :param bar: TODO
        :return: TODO
        """
        return await Foo.create(bar)

    def update_foo(self, ids: list[int]) -> UUID:
        """

        :return:
        """

        bars_query = BarsQueryDto(ids)
        return await self.saga_manager.run("UpdateFoo", context=SagaContext(bars_query=bars_query))

    @staticmethod
    async def get_foos(ids: list[int]) -> list[Foo]:
        """Get a list of tickets.

        :param ids: List of ticket identifiers.
        :return: A list of ``Ticket`` instances.
        """
        return await Foo.get(ids=ids)
