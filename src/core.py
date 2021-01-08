import hashlib


class QueryContent:
    sqlStatement: str
    result: tuple

    def __init__(self, sqlStatement: str, result: tuple):
        self.sqlStatement = sqlStatement
        self.result = result


class WatcherValueChangedEvent:
    watcherName: str
    watchedValue: str

    def __init__(self, watcherName: str, watchedValue: str):
        self.watcherName = watcherName
        self.watchedValue = watchedValue

    def __eq__(self, other):
        return self.watcherName == self.watcherName and \
            self.watchedValue == other.watchedValue


class Watcher:
    name: str
    sqlStatement: str
    _properties: dict
    _watchedValue: str

    def __init__(self, name: str, properties: dict, queryContent: QueryContent):
        self.name = name
        self.sqlStatement = properties["sql"]
        self._properties = properties
        self._watchedValue = self._convertTupleToHash(queryContent.result)

    def checkWatchedValue(self, queryContent: QueryContent) -> WatcherValueChangedEvent:
        result = self._convertTupleToHash(queryContent.result)
        event = None
        if (self._watchedValue != result):
            event = WatcherValueChangedEvent(self.name, result)
            self._watchedValue = result
        return event

    def _convertTupleToHash(self, input: tuple) -> str:
        concat = "".join(str(item) for item in input)
        byte = concat.encode()
        hash_ = hashlib.sha1(byte).hexdigest()
        return hash_
