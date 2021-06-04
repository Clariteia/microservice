"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

from minos.saga import (
    Saga,
    SagaContext,
)


def prepare_get_bars(context: SagaContext):
    """TODO"""
    return context["bars_query"]


UPDATE_FOO = (
    Saga("UpdateFoo")
    .step()
    .invoke_participant("GetBars", prepare_get_bars)
    .on_reply("bars")
    .commit()
)
