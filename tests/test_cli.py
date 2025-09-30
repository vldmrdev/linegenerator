import pytest
from typer.testing import CliRunner

from linegenerator.cli import app

runner = CliRunner()


class TestLinegeneratorCli:

    def test_linegenerator_cli_when_short_template(self):
        result = runner.invoke(
            app, ["--template", "Hello, {name}, welcome to {city}!", "--count", "1"]
        )
        assert result.exit_code == 0
        assert "Hello" in result.output
        assert "welcome to" in result.output
        assert "UNKNOWN_field_" not in result.output

    def test_linegenerator_cli_when_unknown_field(self):
        result = runner.invoke(
            app, ["--template", "Hello, {unknown_field}, welcome to {city}!", "--count", "1"]
        )
        assert result.exit_code == 0
        assert "UNKNOWN_field_" in result.output

    def test_linegenerator_cli_when_placeholders_with_space(self):
        result = runner.invoke(
            app, ["--template", "Hello, {name }, welcome to { city }!", "--count", "1"]
        )
        print(result.output)
        print(result.exception)
        assert result.exit_code == 0
        assert "{name }" not in result.output
        assert "{ city }" not in result.output
