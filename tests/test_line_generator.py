import pytest
from linegenerator.linegenerator import line_generator


def test_line_generator_basic():
    template = "{name} <{email}>"
    result = line_generator(template)

    assert "{name}" not in result
    assert "{email}" not in result
    assert "@" in result
    assert len(result.split()) >= 2  # Имя и email
