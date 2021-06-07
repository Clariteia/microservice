"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from minos.common import (
    MinosModel,
)


class FooDto(MinosModel):
    """Foo DTO instance."""

    id: int
    bar: str


class FoosQueryDto(MinosModel):
    """Foo's Query Dto instance."""

    ids: list[int]


class BarsQueryDto(MinosModel):
    """Bar's query instance."""

    ids: list[int]
