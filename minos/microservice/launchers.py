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

from minos.common import (
    MinosConfig,
    MinosSetup,
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

from .injectors import (
    DependencyInjector,
)


class EntrypointLauncher(MinosSetup):
    """EntryPoint Launcher class."""

    def __init__(self, config: Union[MinosConfig, Path, str], interval: float = 0.1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(config, (str, Path)):

            config = MinosConfig(config)

        self.config = config
        self.interval = interval

    @classmethod
    def _from_config(cls, *args, config: MinosConfig, **kwargs) -> EntrypointLauncher:
        return cls(*args, config=config, **kwargs)

    def launch(self) -> NoReturn:
        """Launch a new execution and keeps running forever..

        :return: This method does not return anything.
        """
        with self.entrypoint as loop:  # pragma: no cover
            loop.run_forever()

    @cached_property
    def entrypoint(self) -> Entrypoint:
        """Entrypoint instance.

        :return: An ``Entrypoint`` instance.
        """

        # noinspection PyUnusedLocal
        @receiver(entrypoint.PRE_START)
        async def _start(*args, **kwargs):
            await self.setup()

        # noinspection PyUnusedLocal
        @receiver(entrypoint.POST_STOP)
        async def _stop(*args, **kwargs):
            await self.destroy()

        return entrypoint(*self.services)

    async def _setup(self) -> NoReturn:
        """Wire the dependencies and setup it.

        :return: This method does not return anything.
        """

        from minos import (
            common,
            microservice,
            networks,
            saga,
        )

        await self.injector.wire(modules=[common, networks, saga, microservice])

    async def _destroy(self) -> NoReturn:
        """Unwire the injected dependencies and destroys it.

        :return: This method does not return anything.
        """
        await self.injector.unwire()

    @cached_property
    def injector(self) -> DependencyInjector:
        """Dependency injector instance.

        :return: A ``DependencyInjector`` instance.
        """
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
