"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

import unittest

from aiomisc import (
    Service,
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

    def setUp(self) -> None:
        super().setUp()
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

    @unittest.skip
    def test_launch(self):
        self.launcher.launch()


if __name__ == "__main__":
    unittest.main()
