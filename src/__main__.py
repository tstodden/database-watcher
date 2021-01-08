import time, signal

from .services import ApplicationService, WatcherController
from .core import Watcher

def signal_handler(signal_received, frame):
    exit(0)

with ApplicationService() as service:
    # catch ctrl+c signal to exit
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        service.triggerWatcherCheck()
        time.sleep(5)
