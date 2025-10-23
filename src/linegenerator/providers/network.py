import random
import socket
import struct

from linegenerator.core.provider import BaseProvider
from faker import Faker


# ipv4_local, ipv4_public
class NetworkProvider(BaseProvider):
    """Generates network-related fields (IPs, ports, etc.)."""

    def _random_ipv4_public(self):
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    def _random_port(self):
        return str(random.randint(1024, 65535))

    def get_generators(self):
        return {
            "ipv4_public": self._random_ipv4_public,
            "port": self._random_port,
        }
