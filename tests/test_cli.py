from typer.testing import CliRunner

from linegenerator.cli import app

runner = CliRunner()


class TestLinegeneratorCli:
    UNKNOWN_FIELD_MASK = "UNKNOWN_field_"

    def test_linegenerator_cli_when_short_template(self):
        result = runner.invoke(
            app, ["custom", "--template", "Hello, {name}, welcome to {city}!", "--count", "1"]
        )
        assert result.exit_code == 0
        assert "Hello" in result.output
        assert "welcome to" in result.output
        assert self.UNKNOWN_FIELD_MASK not in result.output

    def test_linegenerator_cli_when_unknown_field(self):
        result = runner.invoke(
            app,
            ["custom", "--template", "Hello, {unknown_field}, welcome to {city}!", "--count", "1"],
        )
        assert result.exit_code == 0
        assert self.UNKNOWN_FIELD_MASK in result.output

    def test_linegenerator_cli_when_placeholders_with_space(self):
        result = runner.invoke(
            app, ["custom", "--template", "Hello, {name }, welcome to { city }!", "--count", "1"]
        )
        assert result.exit_code == 0
        assert "{name }" not in result.output
        assert "{ city }" not in result.output

    def test_linegenerator_cli_when_locale_not_default(self):
        result = runner.invoke(
            app,
            [
                "custom",
                "--template",
                "Hello, {name}, welcome to {city}!",
                "--locale",
                "ru_RU",
                "--count",
                "1",
            ],
        )
        assert result.exit_code == 0
        assert "Hello" in result.output
        assert "welcome to" in result.output
        assert self.UNKNOWN_FIELD_MASK not in result.output

    # Negative tests
    def test_linegenerator_cli_when_locale_is_invalid(self):
        result = runner.invoke(
            app,
            [
                "custom",
                "--template",
                "Hello, {name}, welcome to {city}!",
                "--locale",
                "xy_XY",
                "--count",
                "1",
            ],
        )
        assert result.exit_code != 0

    def test_linegenerator_cli_when_option_is_invalid(self):
        result = runner.invoke(
            app, ["custom", "--blablabla", "Hello, {name}, welcome to {city}!", "--count", "1"]
        )
        assert result.exit_code != 0
