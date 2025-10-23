from faker import Faker


class GeneratorRegistry:
    def __init__(self) -> None:
        self._generators = {}

    def register(self, name: str, callable_gen):
        if name in self._generators:
            raise ValueError(f"Generator '{name}' already registered")
        self._generators[name] = callable_gen

    def get(self, name: str):
        return self._generators.get(name, lambda: "N/A")

    def register_from_provider(self, provider_instance, prefix: str = ""):
        """Automatically registers all public provider methods.
        For example: provider=TimeProvider(), prefix="timestamp"
        registers "time_iso_timestamp", "time_nginx_timestamp", etc.
        """
        import inspect

        for name, method in inspect.getmembers(provider_instance, predicate=inspect.ismethod):
            if not name.startswith("_"):
                full_name = f"{prefix}_{name}" if prefix else name
                self.register(full_name, method)


def create_default_registry(
    faker_locale: str = "en_US", faker_seed: int | None = None
) -> GeneratorRegistry:
    registry = GeneratorRegistry()

    # Создаём ОДИН экземпляр Faker
    fake = Faker(locale=faker_locale)
    if faker_seed is not None:
        fake.seed_instance(faker_seed)

    # Передаём его всем провайдерам
    registry.register_provider(NetworkProvider(fake))
    registry.register_provider(HttpProvider(fake))
    registry.register_provider(UserProvider(fake))  # и т.д.

    return registry
