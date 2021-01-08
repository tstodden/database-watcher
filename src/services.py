import psycopg2
import yaml
import datetime

from .core import Watcher, QueryContent, WatcherValueChangedEvent
from .constants import *


class WatcherController:
    _dbConn: psycopg2.extensions.connection
    _watchers: [Watcher]

    def __init__(self, connection: psycopg2.extensions.connection):
        self._dbConn = connection
        self._watchers = self.initializeWatchers()

    def executeSqlStatement(self, statement: str) -> QueryContent:
        cursor = self.openCursor()
        cursor.execute(statement)
        result = cursor.fetchone()
        self.commitTransactionAndCloseCursor(cursor)
        return QueryContent(statement, result)

    def openCursor(self) -> psycopg2.extensions.cursor:
        cursor = self._dbConn.cursor()
        return cursor

    def commitTransactionAndCloseCursor(self, cursor: psycopg2.extensions.cursor):
        self._dbConn.commit()
        cursor.close()

    def initializeWatchers(self) -> [Watcher]:
        watchers = []
        config = self.getWatchersConfig()
        for watcherName in config:
            watchers.append(self.createWatcherFromConfig(
                watcherName, config[watcherName]))
        return watchers

    def createWatcherFromConfig(self, name: str, properties: dict) -> Watcher:
        queryContent = self.executeSqlStatement(properties["sql"])
        return Watcher(
            name=name,
            properties=properties,
            queryContent=queryContent)

    def getWatchersConfig(self) -> dict:
        with open(WATCHER_CONFIG_FILEPATH) as configFile:
            config = yaml.safe_load(configFile)
        return config

    def executeWatcherEvents(self):
        for event in self.checkWatchers():
            print(f"Watcher '{event.watcherName}' was triggered at {datetime.datetime.now()}")

    def checkWatchers(self) -> [WatcherValueChangedEvent]:
        watcherEvents = []
        for watch in self._watchers:
            watcherEvents.append(self.checkIndividualWatcher(watch))
        return filter(None, watcherEvents)

    def checkIndividualWatcher(self, watcher: Watcher) -> WatcherValueChangedEvent:
        queryContent = self.executeSqlStatement(watcher.sqlStatement)
        return watcher.checkWatchedValue(queryContent)


class ApplicationService:
    _dbConn: psycopg2.extensions.connection
    _watcherController: WatcherController

    def __init__(self):
        self._dbConn = self.openDBConnection()
        self._watcherController = self.initializeWatcherController()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.closeDBConnection()

    def openDBConnection(self) -> psycopg2.extensions.connection:
        connection = psycopg2.connect(
            host=HOST,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD
        )
        return connection

    def closeDBConnection(self):
        self._dbConn.close()

    def initializeWatcherController(self) -> WatcherController:
        controller = WatcherController(self._dbConn)
        return controller

    def triggerWatcherCheck(self):
        self._watcherController.executeWatcherEvents()
