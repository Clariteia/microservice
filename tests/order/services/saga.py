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


class Bar(MinosModel):
    """Utility minos model class for testing purposes"""

    bar: str


class FooBar(MinosModel):
    """Utility minos model class for testing purposes"""

    bar: str


# noinspection PyUnusedLocal
def foo_fn(context: SagaContext) -> MinosModel:
    """Utility callback function for testing purposes.

    :param context: A context instance.
    :return: A minos model function.
    """
    return Foo("hello")


# noinspection PyUnusedLocal
def finish_fn_1(order):
    """Utility callback function for testing purposes."""
    return Foo("finish")


# noinspection PyUnusedLocal
def finish_fn_2(order):
    """Utility callback function for testing purposes."""
    return Bar("finish")


# noinspection PyUnusedLocal
def finish_fn_3(order):
    """Utility callback function for testing purposes."""
    return FooBar("finish")


# noinspection PyUnusedLocal
def finish_fn_raises(order):
    """Utility callback function for testing purposes."""
    raise ValueError()


class SagaService(object):
    UPDATE_ORDER = (
        Saga("UpdateOrder")
        .step()
        .invoke_participant("AddOrder", foo_fn)
        .with_compensation("DeleteOrder", foo_fn)
        .on_reply("order1", finish_fn_1)
        .step()
        .invoke_participant("AddOrder", foo_fn)
        .with_compensation("DeleteOrder", foo_fn)
        .on_reply("order2", finish_fn_2)
        .step()
        .invoke_participant("AddOrder", foo_fn)
        .with_compensation("DeleteOrder", foo_fn)
        .on_reply("order3", finish_fn_raises)
        .step()
        .invoke_participant("AddOrder", foo_fn)
        .with_compensation("DeleteOrder", foo_fn)
        .on_reply("order4", finish_fn_3)
        .commit()
    )
