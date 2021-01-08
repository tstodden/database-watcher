import time

from .services import ApplicationService, WatcherController
from .core import Watcher

with ApplicationService() as service:
    while(True):
        service.triggerWatcherCheck()
        time.sleep(1)
