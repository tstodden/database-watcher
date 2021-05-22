from .controller import QueryController
from .dispatcher import EventDispatcher


class ApplicationService:
    def __init__(self):
        self._query_controller = QueryController()
        self._event_dispatcher = EventDispatcher()

    def trigger_query_check(self):
        events = self._query_controller.check_queries()
        for e in events:
            self._event_dispatcher.dispatch(e)
