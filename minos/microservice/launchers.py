"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from __future__ import (
    annotations,
)

from pathlib import (
    Path,
)
from typing import (
    TYPE_CHECKING,
    NoReturn,
    Type,
    Union,
)

from aiomisc import (
    Service,
    entrypoint,
    receiver,
)
from aiomisc.entrypoint import (
    Entrypoint,
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
        with self.entrypoint as loop:
            loop.run_forever()

    @cached_property
    def entrypoint(self) -> Entrypoint:
        """TODO

        :return: TODO
        """

        # noinspection PyUnusedLocal
        @receiver(entrypoint.PRE_START)
        async def _fn(*args, **kwargs):
            await self.inject()  # noqa

        return entrypoint(*self.services)

    async def inject(self) -> NoReturn:
        """TODO

        :return: TODO
        """

        from minos import (
            common,
            networks,
            saga,
        )

        await self.injector.wire(modules=[common, networks, saga])

        from tests.order.services.rest import (
            RestService,
        )

        RestService.saga_manager = self.injector.container.saga_manager()

    @cached_property
    def injector(self) -> DependencyInjector:
        """Dependency injector instance.

        :return: A ``DependencyInjector`` instance.
        """
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
    def services(self) -> list[Service]:
        """List of services to be launched.

        :return: A list of ``Service`` instances.
        """
        kwargs = {"config": self.config, "interval": self.interval}
        return [cls(**kwargs) for cls in self._service_classes]

    @property
    def _service_classes(self) -> list[Type[Service]]:
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
            CommandConsumerService,
            CommandHandlerService,
            CommandReplyConsumerService,
            CommandReplyHandlerService,
            EventConsumerService,
            EventHandlerService,
            RestService,
            SnapshotService,
            ProducerService,
        ]
