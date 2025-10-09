import typer
from faker import Faker

from linegenerator.generator import Generators, LinesGenerator
from linegenerator.presets import LogPreset

# from typing_extensions import Annotated


app = typer.Typer(
    name="linegenerator-cli",
    help="Synthetic data line generator",
    add_completion=True,
    pretty_exceptions_enable=True,
    pretty_exceptions_short=True,
    pretty_exceptions_show_locals=False,
)


@app.command(help="Generate data from ready presets")
def preset(
    preset: str = typer.Option("hello", "--preset-name", "-p", help="Preset templates"),
    count: int = typer.Option(1, "--count", "-n", help="Numbers of lines"),
    locale: str = typer.Option("en_US", "--locale", help="Output data language"),
) -> None:
    if not isinstance(preset, str):
        raise TypeError("preset must be string")
    template_preset = LogPreset
    if preset.upper() not in LogPreset.list_preset_names():
        typer.secho(f"Unknown preset: {preset}", fg=typer.colors.RED, err=True)
        typer.secho(
            f"Available presets: {template_preset.list_preset_names()}",
            fg=typer.colors.BRIGHT_BLACK,
            err=True,
        )
        raise typer.Exit(code=1)

    faker = Faker(locale=locale)
    data_generator = Generators(synthetic_generator=faker)
    lines_gen = LinesGenerator(template_preset[preset], data_generator, count)

    for line in lines_gen.generate_lines():  # TODO: change this logic to stdout or file options
        print(line)


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
