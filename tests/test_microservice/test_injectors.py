"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import sys
import unittest
from unittest.mock import (
    MagicMock,
    call,
)

from minos.common import (
    MinosConfig,
    PostgreSqlMinosRepository,
)
from minos.microservice import (
    DependencyInjector,
)
from minos.networks import (
    CommandBroker,
    CommandReplyBroker,
    EventBroker,
)
from minos.saga import (
    SagaManager,
)
from tests.utils import (
    BASE_PATH,
)


class TestMinosDependencyInjector(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.config_file_path = BASE_PATH / "config.yml"
        self.config = MinosConfig(path=str(self.config_file_path))

    def test_container(self):
        injector = DependencyInjector(self.config)
        self.assertEqual(self.config, injector.container.config())

    def test_container_repository(self):
        injector = DependencyInjector(self.config, repository_cls=PostgreSqlMinosRepository)
        self.assertIsInstance(injector.container.repository(), PostgreSqlMinosRepository)

    def test_container_event_broker(self):
        injector = DependencyInjector(self.config, event_broker_cls=EventBroker)
        self.assertIsInstance(injector.container.event_broker(), EventBroker)

    def test_container_command_broker(self):
        injector = DependencyInjector(self.config, command_broker_cls=CommandBroker)
        self.assertIsInstance(injector.container.command_broker(), CommandBroker)

    def test_container_command_reply_broker(self):
        injector = DependencyInjector(self.config, command_reply_broker_cls=CommandReplyBroker)
        self.assertIsInstance(injector.container.command_reply_broker(), CommandReplyBroker)

    def test_container_saga_manager(self):
        injector = DependencyInjector(self.config, saga_manager_cls=SagaManager)
        self.assertIsInstance(injector.container.saga_manager(), SagaManager)

    async def test_wire_unwire(self):
        injector = DependencyInjector(
            self.config,
            repository_cls=PostgreSqlMinosRepository,
            event_broker_cls=EventBroker,
            command_broker_cls=CommandBroker,
            command_reply_broker_cls=CommandReplyBroker,
            saga_manager_cls=SagaManager,
        )

        mock = MagicMock()
        injector.container.wire = mock
        await injector.wire(modules=[sys.modules[__name__]])
        self.assertEqual(1, mock.call_count)
        self.assertEqual(call(modules=[sys.modules[__name__]]), mock.call_args)

        mock = MagicMock()
        injector.container.unwire = mock
        await injector.unwire()
        self.assertEqual(1, mock.call_count)


if __name__ == "__main__":
    unittest.main()
