import hashlib


class QueryContent:
    sqlStatement: str
    result: tuple

    def __init__(self, sqlStatement: str, result: tuple):
        self.sqlStatement = sqlStatement
        self.result = result


class WatcherValueChangedEvent:
    watchedValue: str

    def __init__(self, watchedValue: str):
        self.watchedValue = watchedValue

    def __eq__(self, other):
        return self.watchedValue == other.watchedValue


class Watcher:
    sqlStatement: str
    _watchedValue: str

    def __init__(self, queryContent: QueryContent):
        self.sqlStatement = queryContent.sqlStatement
        self._watchedValue = self._convertTupleToHash(queryContent.result)

    def checkWatchedValue(self, queryContent: QueryContent) -> WatcherValueChangedEvent:
        result = self._convertTupleToHash(queryContent.result)
        event = None
        if (self._watchedValue != result):
            event = WatcherValueChangedEvent(result)
            self._watchedValue = result
        return event

    def _convertTupleToHash(self, input: tuple) -> str:
        concat = "".join(str(item) for item in input)
        byte = concat.encode()
        hash_ = hashlib.sha1(byte).hexdigest()
        return hash_
