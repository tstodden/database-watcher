import logging

from .models import QueryResultChangedEvent


class EventDispatcher:
    def dispatch(self, event: QueryResultChangedEvent):
        logging.info(f"'{event.name}' was triggered")
