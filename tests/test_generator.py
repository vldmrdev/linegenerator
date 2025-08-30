import pytest
from faker import Faker

from linegenerator import Generators, LinesGenerator


@pytest.fixture
def synth_gen():
    return Faker()


@pytest.fixture
def generators(synth_gen):
    return Generators(synth_gen)


@pytest.fixture
def mock_faker_gen(mocker):
    mock_faker = mocker.Mock()
    mock_faker.name.return_value = "Test User"
    mock_faker.email.return_value = "test@example.com"
    mock_faker.phone.return_value = "+1234567890"
    mock_faker.city.return_value = "Test City"
    mock_faker.company.return_value = "Test Company"
    return mock_faker


@pytest.fixture
def mock_generators(mock_faker):
    return Generators(mock_faker)


class TestGenerators:
    """Test: Generators class methods"""

    def test_init_and_default_generators(self, generators):
        assert "name" in generators.get_all_generators()
        assert "email" in generators.get_all_generators()
        assert "unknown" not in generators.get_all_generators()

    def test_has_generator(self, generators):
        assert generators.has_generator("name") is True
        assert generators.has_generator("nonexistent") is False

    def test_get_generator_valid(self, generators):
        gen = generators.get_generator("name")
        result = gen()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_generator_invalid(self, generators):
        with pytest.raises(ValueError, match="Invalid generator name"):
            generators.get_generator("invalid_generator")

    def test_hack_generators_dict(self):
        """Test: delete generator by name from returned default generator's dict"""
        fake = Faker()
        generators = Generators(fake)

        original_count = len(generators.get_all_generators())
        original_has_name = generators.has_generator("name")

        returned_dict = generators.get_all_generators()
        if "name" in returned_dict:
            del returned_dict["name"]

        assert len(generators.get_all_generators()) == original_count
        assert generators.has_generator("name") == original_has_name
        assert "name" in generators.get_all_generators()


class TestLinesGenerator:
    """Test: LinesGenerator class methods"""

    @pytest.fixture
    def line_template(self):
        return "Hello {name} from {city}!"

    @pytest.fixture
    def lines_gen(self, synth_gen, line_template):
        generators = Generators(synth_gen)
        return LinesGenerator(line_template, generators, line_count=3)

    def test_extract_fields(self, lines_gen):
        expected = ["name", "city"]
        assert lines_gen._template_fields_list == expected

    def test_one_line_generator(self, synth_gen):
        generators = Generators(synth_gen)
        lg = LinesGenerator("Hi {name}!", generators)
        result = lg.one_line_generator()
        assert "{name}" not in result
        assert "Hi " in result

    def test_lines_generator(self, lines_gen):
        results = list(lines_gen.lines_generator())
        assert len(results) == 3
        for line in results:
            assert "{name}" not in line
            assert "{city}" not in line
            assert "Hello " in line
            assert " from " in line

    def test_unknown_field_in_template(self, synth_gen):
        generators = Generators(synth_gen)
        lg = LinesGenerator("Greetings {unknown_field}!", generators)
        result = lg.one_line_generator()
        assert "UNKNOWN_field_[unknown_field]" in result

    # mocked tests
    @pytest.fixture
    def lines_mock_gen(self, mock_faker_gen, line_template):
        generators = Generators(mock_faker_gen)
        return LinesGenerator(line_template, generators, line_count=3)

    def test_one_line_mock_generator(self, mock_faker_gen):
        generators = Generators(mock_faker_gen)
        lg = LinesGenerator("Hi {name}!", generators)
        result = lg.one_line_generator()
        assert "{name}" not in result
        assert "Hi Test User" in result

    def test_lines_mock_generator(self, lines_mock_gen):
        results = list(lines_mock_gen.lines_generator())
        assert len(results) == 3
        for line in results:
            assert "{name}" not in line
            assert "{city}" not in line
            assert "Hello Test User" in line
            assert " from Test City" in line
