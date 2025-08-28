import pytest
from typer.testing import CliRunner

from src.linegenerator.cli import app

runner = CliRunner()

def test_linegenerator_cli_basic():
    result = runner.invoke(app,[
        "--template",
        "Hello, {name}, welcome to {city}!",
        "--count",
        "1"
    ]
                           )
    assert result.exit_code == 0
    assert "Hello" in result.output
    assert "welcome to" in result.output
    assert "UNKNOWN_field_" not in result.output


