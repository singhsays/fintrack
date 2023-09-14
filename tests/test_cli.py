import unittest
from pathlib import Path
from unittest.mock import ANY, call, patch

from click.testing import CliRunner

from fintrack import __version__, cli

config = {"version": __version__}


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.log_file = Path("test_log.log")

    def tearDown(self):
        self.log_file.unlink(missing_ok=True)

    @patch("fintrack.log")
    def test_version(self, log_mock):
        result = self.runner.invoke(cli, ["version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(__version__, result.output)
        log_mock.remove.assert_called_once()
        log_mock.add.assert_called_once_with(ANY, level="INFO")

    @patch("fintrack.log")
    def test_logfile(self, log_mock):
        result = self.runner.invoke(cli, ["--log_file", "test_log.log", "version"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn(__version__, result.output)
        log_mock.remove.assert_called_once()
        log_mock.add.assert_has_calls(
            [
                call(ANY, level="INFO"),
                call(
                    str(self.log_file.absolute()),
                    rotation="1 day",
                    retention="30 days",
                    level="INFO",
                ),
            ]
        )
