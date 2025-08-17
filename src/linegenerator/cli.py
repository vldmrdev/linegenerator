import typer
from faker import Faker
from linegenerator import line_generator

app = typer.Typer(
    name="linegenerator-cli",
    help="Synthetic data line generator"
)

@app.command()
def main(template: str = "{name}"):
    fake = Faker()
    result = template.format(name=fake.name(), email=fake.email(), ip=fake.ipv4())
    print(result)

if __name__ == "__main__":
    app()