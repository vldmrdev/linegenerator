from jinja2 import Environment, FileSystemLoader
from faker import Faker
import click
from random import choice
import datetime

fake = Faker()


def fake_log(templates_path: str = 'templates/', template: str = 'example-template.txt'):
    environment = Environment(loader=FileSystemLoader(templates_path))
    template = environment.get_template(template)
    content = template.render(
        date=fake.date_time_between(start_date=datetime.datetime(2022, 4, 4, 16, 11, 35)),  # start_date
        uri=fake.domain_name(),
        ip_v4=fake.ipv4(),
        port=choice(['80', '443']),
        http_code=choice(['200', '500', '404', '302']),
        method=fake.http_method()
    )
    return content


@click.command()
@click.option('--lines', default=1, help='Lines count')
@click.option('--output', default='output.txt', help='Output file')
@click.option('--templates_path', default='templates/', help='Templates directory path')
@click.option('--template', default='web-server-template.txt', help='Template file name')
def main(lines: int = 1, output: str = 'output.txt', templates_path='templates/', template='nginx-log-template.txt'):
    with open(output, '+w') as f:
        for _ in range(lines):
            f.writelines((fake_log(templates_path, template)))


if __name__ == '__main__':
    main()
