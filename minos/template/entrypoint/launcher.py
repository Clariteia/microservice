"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import asyncio
import sys

from aiomisc import (
    Service,
    entrypoint,
)
from cached_property import (
    cached_property,
)

from minos.common import (
    PostgreSqlMinosRepository,
)
from minos.networks import (
    CommandBroker,
    CommandConsumerService,
    CommandHandlerService,
    CommandReplyBroker,
    CommandReplyConsumerService,
    CommandReplyHandlerService,
    EventBroker,
    EventConsumerService,
    EventHandlerService,
    ProducerService,
    RestService,
    SnapshotService,
)
from minos.saga import (
    SagaManager,
)

from ..injectors import (
    MinosDependencyInjector,
)


class EntrypointLauncher(object):
    """TODO"""

    def __init__(self, config, interval: float = 0.1):
        self.config = config
        self.interval = interval

    def launch(self) -> None:
        """TODO

        :return: TODO
        """
        self._launch_injector()
        self._launch_services()

    def _launch_injector(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self._injector.wire(modules=[sys.modules[__name__]]))

        from minos.common import (
            Aggregate,
        )
        from minos.networks import (
            CommandHandler,
            CommandReplyHandler,
        )
        from minos.saga import (
            PublishExecutor,
        )

        CommandReplyHandler.saga_manager = self._injector.container.saga_manager()
        CommandHandler.broker = self._injector.container.command_reply_broker()
        PublishExecutor.broker = self._injector.container.command_broker()
        Aggregate._repository = self._injector.container.repository()

    @cached_property
    def _injector(self) -> MinosDependencyInjector:
        injector = MinosDependencyInjector(
            config=self.config,
            command_broker_cls=CommandBroker,
            command_reply_broker_cls=CommandReplyBroker,
            event_broker_cls=EventBroker,
            repository_cls=PostgreSqlMinosRepository,
            saga_manager_cls=SagaManager,
        )
        return injector

    def _launch_services(self):
        with entrypoint(*self._services) as loop:
            loop.run_forever()

    @cached_property
    def _services(self) -> list[Service]:
        return [
            CommandConsumerService(config=self.config, interval=self.interval),
            CommandHandlerService(config=self.config, interval=self.interval),
            CommandReplyConsumerService(config=self.config,),
            CommandReplyHandlerService(config=self.config, interval=self.interval),
            EventConsumerService(config=self.config,),
            EventHandlerService(config=self.config, interval=self.interval),
            RestService(config=self.config),
            SnapshotService(config=self.config, interval=self.interval),
            ProducerService(config=self.config, interval=self.interval),
        ]
