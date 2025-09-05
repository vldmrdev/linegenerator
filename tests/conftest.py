import pytest
from faker import Faker

from linegenerator import Generators, LinesGenerator


@pytest.fixture
def short_line_template():
    template = "Hello {name} from {city}!"
    expected_fields = ["name", "city"]
    return template, expected_fields


@pytest.fixture
def short_template_unknown_field():
    template = "This is unknown_field - {unknown_field}!"
    expected_field = "UNKNOWN_field_[unknown_field]"
    return template, expected_field


@pytest.fixture
def generators():
    generator = Faker()
    return Generators(generator)


# @pytest.fixture
# def lines_generator(generators, line_template):
#     return LinesGenerator(line_template, generators, line_count=3)


# mocked fixtures
# @pytest.fixture
# def mock_generator(mocker):
#     mock_generator = mocker.Mock()
#     mock_generator.name.return_value = "Test User"
#     mock_generator.email.return_value = "test@example.com"
#     mock_generator.phone.return_value = "+1234567890"
#     mock_generator.city.return_value = "Test City"
#     mock_generator.company.return_value = "Test Company"
#     return mock_generator
#
#
# @pytest.fixture
# def mock_generators(mock_generator):
#     return Generators(mock_generator)
#
#
# @pytest.fixture
# def mock_lines_generator(mock_generator, short_line_template):
#     generators = Generators(mock_generator)
#     return LinesGenerator(short_line_template[0], generators, line_count=3)
