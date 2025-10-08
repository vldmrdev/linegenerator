import typer
from faker import Faker

from linegenerator.generator import Generators, LinesGenerator

# from typing_extensions import Annotated


app = typer.Typer(
    name="linegenerator-cli",
    help="Synthetic data line generator",
    add_completion=True,
)


@app.command(help="Generate data from ready presets")
def preset(
    preset: str = typer.Option("hello", "--preset-name", "-p", help="Preset templates")
) -> str:  # TODO: mypy fix, change it
    return "preset"


@app.command(help="Generate data from custom template")
def custom(
    template: str = typer.Option("Hello, {name}!", "--template", "-t", help="Line template"),
    count: int = typer.Option(1, "--count", "-n", help="Numbers of lines"),
    locale: str = typer.Option("en_US", "--locale", help="Output data language"),
    help_generators: bool = typer.Option(
        False, "--help-generators", help="Show list default generators"
    ),
) -> None:
    faker = Faker(locale=locale)
    data_generator = Generators(synthetic_generator=faker)
    lines_gen = LinesGenerator(template, data_generator, count)

    if help_generators:
        typer.secho("Available generators:", bold=True, fg=typer.colors.BLUE)
        # TODO: add generators description
        for field in sorted(data_generator.get_all_generators()):
            typer.echo(f"  {{{field}}}")
        raise typer.Exit()

    for line in lines_gen.generate_lines():  # TODO: change this logic to stdout or file options
        print(line)


# TODO: add try\except for error running app()
if __name__ == "__main__":
    app()
