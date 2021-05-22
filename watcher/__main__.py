import logging
import signal
import time

from .app import ApplicationService


def signal_handler(signal_received, frame):
    exit(0)


signal.signal(signal.SIGINT, signal_handler)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

service = ApplicationService()

while True:
    service.trigger_query_check()
    time.sleep(5)
