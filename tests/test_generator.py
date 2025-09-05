import pytest
from faker import Faker

from linegenerator import Generators, LinesGenerator


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

    def test_extracted_fields_from_template_is_expected(self, short_line_template, generators):
        lg = LinesGenerator(short_line_template[0], generators, 1)
        expected = short_line_template[1]
        assert lg._template_fields_list == expected

    @pytest.mark.parametrize(
        "line_template, expected_fields",
        [
            ("Hello {name} from {city}!", ("{name}", "{city}")),
            (
                "Welcome to {company}, our phone number is {phone_number}!",
                ("{company}", "{phone_number}"),
            ),
        ],
    )
    def test_generate_lines_is_correct(self, line_template, expected_fields, generators):
        lg = LinesGenerator(line_template, generators, 3)
        results = list(lg.generate_lines())
        assert len(results) == 3
        for line in results:
            assert expected_fields[0] not in line
            assert expected_fields[1] not in line

    def test_lines_generator_when_no_fields(self, generators):
        template = "This template without fields"
        lg = LinesGenerator(template, generators, 1)
        results = list(lg.generate_lines())
        assert len(results) == 1
        assert template == results[0]

    def test_lines_generator_are_lines_different(self, short_line_template, generators):
        lg = LinesGenerator(short_line_template[0], generators, 2)
        results = list(lg.generate_lines())
        assert len(results) == 2
        assert results[0] != results[1]

    def test_unknown_field_in_template(self, short_template_unknown_field, generators):
        lg = LinesGenerator(short_template_unknown_field[0], generators, 1)
        result = list(lg.generate_lines())
        assert short_template_unknown_field[1] in result[0]
