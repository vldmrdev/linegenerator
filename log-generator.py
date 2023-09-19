from jinja2 import Environment, FileSystemLoader
import faker

fake = faker.Faker('en_US')

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("nginx-log-template.txt")


def fake_log():
    content = template.render(
        uri=fake.domain_name(),
        ip_v4=fake.ipv4(),
        port='80',
        http_code='200'
    )
    return content


with open('output-log.txt', 'x') as f:
    for _ in range(3):
        f.writelines((fake_log()))
