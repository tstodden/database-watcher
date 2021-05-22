from .config import Config
from .models import QueryResult


class Query:
    def __init__(self, config: Config, result: QueryResult):
        self._config = config
        self._value = result.get_result_hash()

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def sql(self) -> str:
        return self._config.sql

    @property
    def value(self) -> str:
        return self._value

    def check(self, result: QueryResult) -> bool:
        is_changed = False
        new_value = result.get_result_hash()
        if (self._value != new_value):
            is_changed = True
            self._value = new_value
        return is_changed
