import unittest
from typer.testing import CliRunner
from minos.microservice.cli import app
from tests.utils import BASE_PATH

runner = CliRunner()


class TestCli(unittest.TestCase):
    def test_app(self):
        path = f"{BASE_PATH}/config.yml"
        result = runner.invoke(app, ["start", path])
        self.assertEqual(result.exit_code, 0)
        self.assertTrue("Microservice is up and running!" in result.stdout)

    def test_app_ko(self):
        path = f"{BASE_PATH}/non_existing_config.yml"
        result = runner.invoke(app, ["start", path])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue("Error starting microservice" in result.stdout)
