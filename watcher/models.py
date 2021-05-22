import hashlib
from typing import NamedTuple


class QueryResult(NamedTuple):
    sql: str
    result: tuple

    def get_result_hash(self) -> str:
        concat = "".join(str(item) for item in self.result)
        byte = concat.encode()
        return hashlib.sha1(byte).hexdigest()


class QueryResultChangedEvent(NamedTuple):
    name: str
    value: str
