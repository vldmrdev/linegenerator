import re
from typing import Callable, Generator

from faker import Faker


class Generators:
    def __init__(self, fake_gen: Faker) -> None:
        self.fake_gen: Faker = fake_gen
        self.__generators: dict[str, Callable[..., str]] = {}
        self._register_default_generators()

    def _register_default_generators(self) -> None:
        default_faker_methods = [
            "name",
            "first_name",
            "last_name",
            "email",
            "phone",
            "city",
            "company",
            "job",
            "date",
            "address",
        ]
        for method_name in default_faker_methods:
            if hasattr(self.fake_gen, method_name):

                def make_gen(method: str) -> Callable[..., str]:
                    return lambda: getattr(self.fake_gen, method)()

                self.__generators[method_name] = make_gen(method_name)

    def get_generator(self, name: str) -> Callable[..., str]:  # no
        if name not in self.__generators:
            raise ValueError("Invalid generator name")
        return self.__generators.get(name)  # type: ignore

    def has_generator(self, name: str) -> bool:
        return name in self.__generators

    # TODO: template method
    def get_all_generators(self) -> dict[str, Callable[..., str]]:
        return self.__generators

    # TODO: add custom generator option


class LinesGenerator:
    def __init__(self, line_template: str, data_generator: Generators, line_count: int = 1) -> None:
        self.line_template: str = line_template
        self.data_generator: Generators = data_generator
        self.line_count: int = line_count
        self._template_fields_list: list = self._extract_fields(self.line_template)

    def _extract_fields(self, template: str) -> list[str]:
        """
        return list of fields from template like this:
        "Hello {name}! Your city is {city}?" --> ['name', 'city']
        """
        return re.findall(r"\{\s*([^}]+?)\s*}", template)

    def one_line_generator(self) -> str:
        generated_data = {}
        for field in self._template_fields_list:
            if self.data_generator.has_generator(field):
                # TODO: add exception
                fake_data = self.data_generator.get_generator(field)()
                generated_data[field] = fake_data
            else:
                generated_data[field] = f"UNKNOWN_field_[{field}]"

        return self.line_template.format(**generated_data)

    def lines_generator(self) -> Generator[str, None, None]:
        for _ in range(self.line_count):
            yield self.one_line_generator()


# TODO: add export to file option
# TODO: add docstrings
