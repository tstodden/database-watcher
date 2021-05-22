class Config:
    def __init__(self, config: dict):
        self._config = config

    @property
    def name(self) -> str:
        return self.get_required_property("name")

    @property
    def sql(self) -> str:
        return self.get_required_property("sql")

    def get_required_property(self, prop: str):
        prop = self._config.get(prop)
        if not prop:
            raise KeyError(f"Missing '{prop}' in watchers.yml")
        return prop

    def get_optional_property(self, prop: str):
        return self._config.get(prop)
