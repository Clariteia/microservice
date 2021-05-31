"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

import sys
from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
    NoReturn,
    Union,
)

from aiomisc import (
    Service,
    entrypoint,
    receiver,
)
from cached_property import (
    cached_property,
)

from .injectors import (
    DependencyInjector,
)

if TYPE_CHECKING:
    from minos.common import (
        MinosConfig,
    )


class EntrypointLauncher(object):
    """EntryPoint Launcher class."""

    def __init__(self, config: Union[MinosConfig, Path, str], interval: float = 0.1):
        if isinstance(config, (str, Path)):
            from minos.common import (
                MinosConfig,
            )

            config = MinosConfig(config)

        self.config = config
        self.interval = interval

    def launch(self) -> NoReturn:
        """Launch a new execution and keeps running forever..

        :return: This method does not return anything.
        """

        @receiver(entrypoint.PRE_START)
        async def _fn(*args, **kwargs):
            await self._launch_injector()

        with entrypoint(*self._services) as loop:
            loop.run_forever()

    async def _launch_injector(self):
        await self._injector.wire(modules=[sys.modules[__name__]])

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

        from tests.order.services.rest import (
            RestService,
        )

        RestService.saga_manager = self._injector.container.saga_manager()

    @cached_property
    def _injector(self) -> DependencyInjector:
        from minos.common import (
            PostgreSqlMinosRepository,
        )
        from minos.networks import (
            CommandBroker,
            CommandReplyBroker,
            EventBroker,
        )
        from minos.saga import (
            SagaManager,
        )

        injector = DependencyInjector(
            config=self.config,
            command_broker_cls=CommandBroker,
            command_reply_broker_cls=CommandReplyBroker,
            event_broker_cls=EventBroker,
            repository_cls=PostgreSqlMinosRepository,
            saga_manager_cls=SagaManager,
        )
        return injector

    @cached_property
    def _services(self) -> list[Service]:
        from minos.networks import (
            CommandConsumerService,
            CommandHandlerService,
            CommandReplyConsumerService,
            CommandReplyHandlerService,
            EventConsumerService,
            EventHandlerService,
            ProducerService,
            RestService,
            SnapshotService,
        )

        return [
            CommandConsumerService(config=self.config, interval=self.interval),
            CommandHandlerService(config=self.config, interval=self.interval),
            CommandReplyConsumerService(config=self.config),
            CommandReplyHandlerService(config=self.config, interval=self.interval),
            EventConsumerService(config=self.config),
            EventHandlerService(config=self.config, interval=self.interval),
            RestService(config=self.config),
            SnapshotService(config=self.config, interval=self.interval),
            ProducerService(config=self.config, interval=self.interval),
        ]
