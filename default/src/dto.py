"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    MinosModel,
)


class FooDto(MinosModel):
    """TODO"""
    id: int
    bar: str


class FoosQueryDto(MinosModel):
    """TODO"""
    ids: list[int]


class BarsQueryDto(MinosModel):
    """TODO"""
    ids: list[int]
