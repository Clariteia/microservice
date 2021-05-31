"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

import unittest
from unittest.mock import (
    MagicMock,
    call,
)

from aiomisc import (
    Service,
)
from aiomisc.entrypoint import (
    Entrypoint,
)

from minos.common import (
    MinosConfig,
)
from minos.common.testing import (
    PostgresAsyncTestCase,
)
from minos.microservice import (
    DependencyInjector,
    EntrypointLauncher,
)
from tests.utils import (
    BASE_PATH,
)


class TestEntrypointLauncher(PostgresAsyncTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    async def asyncSetUp(self):
        await super().asyncSetUp()
        self.launcher = EntrypointLauncher(self.config)

    def test_config(self):
        self.assertEqual(self.config, self.launcher.config)

    def test_interval(self):
        self.assertEqual(0.1, self.launcher.interval)

    def test_injector(self):
        self.assertIsInstance(self.launcher.injector, DependencyInjector)

    def test_services(self):
        self.assertIsInstance(self.launcher.services, list)
        self.assertEqual(9, len(self.launcher.services))
        for service in self.launcher.services:
            self.assertIsInstance(service, Service)

    async def test_entrypoint(self):
        async def _fn(*args, **kwargs):
            pass

        mock = MagicMock(side_effect=_fn)
        self.launcher.wire = mock
        self.launcher.__dict__["services"] = list()
        self.launcher.unwire = mock
        self.assertIsInstance(self.launcher.entrypoint, Entrypoint)

    async def test_wire(self):
        async def _fn(*args, **kwargs):
            pass

        mock = MagicMock(side_effect=_fn)
        self.launcher.injector.wire = mock
        await self.launcher.wire()

        self.assertEqual(1, mock.call_count)
        from minos import (
            common,
            networks,
            saga,
        )

        self.assertEqual(call(modules=[common, networks, saga]), mock.call_args)

    async def test_unwire(self):
        async def _fn(*args, **kwargs):
            pass

        mock = MagicMock(side_effect=_fn)
        self.launcher.injector.unwire = mock
        await self.launcher.unwire()

        self.assertEqual(1, mock.call_count)
        self.assertEqual(call(), mock.call_args)

    @unittest.skip
    def test_launch(self):
        self.launcher.launch()


class TestEntrypointLauncherFromPath(unittest.TestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def test_config(self) -> None:
        launcher = EntrypointLauncher(self.CONFIG_FILE_PATH)
        self.assertIsInstance(launcher.config, MinosConfig)


if __name__ == "__main__":
    unittest.main()
