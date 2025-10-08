import re
from typing import Callable, Generator

from faker import Faker


class Generators:
    """A registry of callable generators that produce synthetic data using Faker or custom generator.

    This class wraps a Faker instance and provides a dictionary-like interface
    to access predefined or custom data generators by name. It supports default
    Faker methods (like 'name', 'email') and allows future extension with custom generators.

    Attributes:
        synthetic_generator (Faker): The underlying Faker instance used to generate data.
        __generators (dict[str, Callable[..., str]]): A private mapping of generator names to callables.
    """

    def __init__(self, synthetic_generator: Faker) -> None:
        self.synthetic_generator: Faker = synthetic_generator
        self.__generators: dict[str, Callable[..., str]] = {
            "name": self.synthetic_generator.name,
            "email": self.synthetic_generator.email,
            "phone_number": self.synthetic_generator.phone_number,
            "city": self.synthetic_generator.city,
            "company": self.synthetic_generator.company,
            "job": self.synthetic_generator.job,
            "date": self.synthetic_generator.date,
            "address": self.synthetic_generator.address,
        }

    @property
    def synthetic_generator(self) -> Faker:
        return self._synthetic_generator

    @synthetic_generator.setter
    def synthetic_generator(self, value: Faker) -> None:
        if not isinstance(value, Faker):
            raise TypeError("synth_generator must be a Faker instance.")
        self._synthetic_generator = value

    def get_generator(self, name: str) -> Callable[..., str]:
        """Returns a callable generator by its name.

        Args:
            name (str): The name of the generator (e.g., 'email', 'city').
        Returns:
            Callable[..., str]: A function that returns a generated string.
        Raises:
            ValueError: If no generator exists with the given name.
        """

        if name not in self.__generators:
            raise ValueError(f"Invalid generator name: '{name}'")
        return self.__generators.get(name)  # type: ignore

    def has_generator(self, name: str) -> bool:
        """Checks whether a generator with the given name exists.

        Args:
            name (str): The name of the generator to check.
        Returns:
            bool: True if the generator exists, False otherwise.
        """
        return name in self.__generators

    def get_all_generators(self) -> dict[str, Callable[..., str]]:
        return self.__generators.copy()

    # TODO: add custom generator option


class LinesGenerator:
    """Generates formatted text lines using a template and fake data.

    This class takes a template string with placeholders (e.g., {name}, {city}),
    replaces them with synthetic data from a Generators instance, and produces one or more lines.
    Important note: NO space in placeholders, only {name}, { name } or {name }, etc. are wrong.

    Attributes:
        line_template (str): The template string with placeholders.
        data_generator (Generators): Instance providing fake data generators.
        line_count (int): Number of lines to generate.
        _template_fields_list (list[str]): List of field names extracted from the line_template.
    """

    def __init__(self, line_template: str, data_generator: Generators, line_count: int = 1) -> None:
        self.line_template: str = line_template
        self.data_generator: Generators = data_generator
        self.line_count: int = line_count
        self._template_fields_list: list = self._extract_fields(self.line_template)

    def __setattr__(self, key: str, value: object) -> None:
        """Class attributes validator"""
        if key == "line_template" and not isinstance(value, str):
            raise TypeError("line_template must be a string.")
        elif key == "data_generator" and not isinstance(value, Generators):
            raise TypeError("data_generator must be an instance of Generators.")
        elif key == "line_count" and (not isinstance(value, int) or value <= 0):
            raise ValueError("line_count must be a positive integer.")
        super().__setattr__(key, value)

    def _extract_fields(self, template: str) -> list[str]:
        """Extracts placeholder field names from a template string.

        Supports placeholders in the only {field} format, without spaces.

        Args:
            template (str): The template string containing placeholders.
        Returns:
            list[str]: A list of field names extracted from the template.
        Example:
            >>> self._extract_fields("Hello {name}! You live in {city}?")
            ['name', 'city']
        """

        return re.findall(r"\{([^}]*)\}", template)

    def generate_lines(self) -> Generator[str, None, None]:
        """Generates multiple formatted lines lazily (one at a time).

        Yields:
            str: A generated line with synthetic data, one per iteration.
        Note:
            This is a generator function. Use in a loop or convert to list if needed.
        """
        fields_generators = {}
        generated_data = {}
        for field in self._template_fields_list:
            if self.data_generator.has_generator(field):
                fields_generators[field] = self.data_generator.get_generator(field)
            else:
                generated_data[field] = f"UNKNOWN_field_[{field}]"
        for _ in range(self.line_count):
            for field, generator in fields_generators.items():
                generated_data[field] = generator()
            yield self.line_template.format(**generated_data)


# TODO: add locales option
# TODO: add export to file option
