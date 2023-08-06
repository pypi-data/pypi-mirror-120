from typing import NamedTuple, Optional

from ruteni.utils.dns import RecordList


class Record(NamedTuple):
    host: str
    priority: int
    ttl: int
    type: str = "MX"


class DNSMock:
    def __init__(self, domain_servers: dict[str, list[tuple[str, int, int]]]) -> None:
        self.domain_servers = domain_servers

    async def query_mx(self, domain: str) -> Optional[RecordList]:
        if domain not in self.domain_servers:
            return None
        return [Record(*fields) for fields in self.domain_servers[domain]]
