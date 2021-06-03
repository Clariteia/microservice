import unittest
from unittest.mock import (
    patch,
)

from typer.testing import (
    CliRunner,
)

from minos.microservice import (
    cli_app,
)
from tests.utils import (
    BASE_PATH,
)

runner = CliRunner()


class TestCli(unittest.TestCase):
    def test_app(self):
        path = f"{BASE_PATH}/config.yml"
        with patch("minos.microservice.EntrypointLauncher.launch") as mock:
            mock.return_value = None
            result = runner.invoke(cli_app, ["start", path])
            self.assertEqual(result.exit_code, 0)
            self.assertIn("Microservice is up and running!", result.stdout)
            self.assertEqual(1, mock.call_count)

    def test_app_raises_config(self):
        path = f"{BASE_PATH}/non_existing_config.yml"
        result = runner.invoke(cli_app, ["start", path])
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Error loading config", result.stdout)


if __name__ == "__main__":
    unittest.main()
