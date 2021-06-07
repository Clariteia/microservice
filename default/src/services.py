"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from uuid import (
    UUID,
)

from minos.common import (
    Service,
)
from minos.saga import (
    SagaContext,
)

from .aggregates import (
    Foo,
)
from .dto import (
    BarsQueryDto,
)


class FooService(Service):
    """Ticket Service class"""

    @staticmethod
    async def create_foo(bar: str) -> Foo:
        """Creates a foo instance.

        :param bar: bar field to be set to the foo instance.
        :return: The created ``Foo`` instance.
        """
        return await Foo.create(bar)

    async def update_foo(self, ids: list[int]) -> UUID:
        """Updates foo instances over a saga.

        :return: The unique identifier of the saga.
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
