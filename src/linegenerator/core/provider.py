from abc import ABC
from typing import Callable, Dict


class BaseProvider(ABC):
    """Base class for generator providers.
    Provider -  is class which gets dict like {"generator_name": generator_func}.
    """

    def get_generators(self) -> Dict[str, Callable]:
        """return generators dict {"generator_name": generator_func}"""
        raise NotImplementedError
