"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""

import unittest

from minos.common.testing import (
    PostgresAsyncTestCase,
)
from minos.microservice import (
    EntrypointLauncher,
)
from tests.utils import (
    BASE_PATH,
)


class TestEntrypointLauncher(PostgresAsyncTestCase):
    CONFIG_FILE_PATH = BASE_PATH / "config.yml"

    def test_constructor(self):
        launcher = EntrypointLauncher(self.config)
        self.assertEqual(self.config, launcher.config)


if __name__ == "__main__":
    unittest.main()
