import os

# database config
HOST = os.environ.get("HOST")
DATABASE = os.environ.get("DATABASE")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")

WATCHER_CONFIG_FILEPATH = "watchers.yml"
