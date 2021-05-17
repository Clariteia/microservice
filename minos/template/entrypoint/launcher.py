"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from aiomisc import (
    Service,
    entrypoint,
)
from cached_property import (
    cached_property,
)

from minos.common import (
    MinosConfig,
)
from minos.networks import (
    REST,
    MinosCommandPeriodicService,
    MinosCommandReplyPeriodicService,
    MinosCommandReplyServerService,
    MinosCommandServerService,
    MinosEventPeriodicService,
    MinosEventServerService,
    MinosQueueService,
    MinosSnapshotService,
)


class EntrypointLauncher(object):
    """TODO"""

    def __init__(self, config: MinosConfig, interval: float = 0.1):
        self.config = config
        self.interval = interval

    def launch(self) -> None:
        """TODO

        :return: TODO
        """
        with entrypoint(*self._services) as loop:
            loop.run_forever()

    @cached_property
    def _services(self) -> list[Service]:
        return [
            self._command_handler,
            self._command_queue_handler,
            self._command_reply_handler,
            self._command_reply_queue_handler,
            self._event_handler,
            self._event_queue_handler,
            self._queue_broker,
            self._rest_handler,
            self._snapshot,
        ]

    @cached_property
    def _command_handler(self) -> MinosCommandServerService:
        return MinosCommandServerService(self.config)

    @cached_property
    def _command_queue_handler(self) -> MinosCommandPeriodicService:
        return MinosCommandPeriodicService(self.config, interval=self.interval)

    @cached_property
    def _command_reply_handler(self) -> MinosCommandReplyServerService:
        return MinosCommandReplyServerService(self.config)

    @cached_property
    def _command_reply_queue_handler(self) -> MinosCommandReplyPeriodicService:
        return MinosCommandReplyPeriodicService(self.config, interval=self.interval)

    @cached_property
    def _event_handler(self) -> MinosEventServerService:
        return MinosEventServerService(self.config)

    @cached_property
    def _event_queue_handler(self) -> MinosEventPeriodicService:
        return MinosEventPeriodicService(self.config, interval=self.interval)

    @cached_property
    def _rest_handler(self):
        return REST(self.config)

    @cached_property
    def _snapshot(self):
        return MinosSnapshotService(self.config, interval=self.interval)

    @cached_property
    def _queue_broker(self) -> MinosQueueService:
        return MinosQueueService(self.config, interval=self.interval)
