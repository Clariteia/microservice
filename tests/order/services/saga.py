"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    MinosModel,
)
from minos.saga import (
    Saga,
    SagaContext,
)


class Foo(MinosModel):
    """Utility minos model class for testing purposes"""

    foo: str


# noinspection PyUnusedLocal
def foo_fn(context: SagaContext) -> MinosModel:
    """Utility callback function for testing purposes.

    :param context: A context instance.
    :return: A minos model function.
    """
    return Foo("hello")


def finish_fn(order):
    return Foo("finish")


class SagaService(object):
    UPDATE_ORDER = (
        Saga("UpdateOrder")
        .step()
        .invoke_participant("AddOrder", foo_fn)
        .on_reply("order1", finish_fn)
        .step()
        .invoke_participant("DeleteOrder", foo_fn)
        .on_reply("order2", finish_fn)
        .commit()
    )
