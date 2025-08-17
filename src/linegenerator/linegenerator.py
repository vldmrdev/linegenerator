from faker import Faker
import re

fake_data = Faker()


def line_generator(line_template: str) -> str:
    def replace(match):
        field = match.group(1)
        # Базовые поля
        if field == "name":
            return fake_data.name()
        if field == "email":
            return fake_data.email()
        if field == "ip":
            return fake_data.ipv4()
        if field == "phone":
            return fake_data.phone_number()
        if field == "address":
            return fake_data.address().replace("\n", ", ")
        if field == "company":
            return fake_data.company()
        if field == "job":
            return fake_data.job()
        if field == "browser":
            return fake_data.chrome() if fake_data.pybool() else fake_data.firefox()
        if field == "os":
            return fake_data.linux_platform_token()
        if field == "date":
            return fake_data.date()

        return match.group(0)  # Оставляем {unknown} без изменений

    return re.sub(r"\{(\w+)\}", replace, line_template)
