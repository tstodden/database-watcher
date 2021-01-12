import psycopg2
import yaml
import datetime
import logging

from .core import Watcher, QueryContent, WatcherValueChangedEvent
from .constants import *


class EventDispatcher:
    def dispatch(self, event):
        if type(event) == WatcherValueChangedEvent:
            logging.info(f"'{event.watcherName}' was triggered")
        else:
            raise NotImplementedError


class WatcherController:
    _database: psycopg2.extensions.connection
    _eventDispatcher = EventDispatcher()
    _watchers: [Watcher]

    def __init__(self, connection: psycopg2.extensions.connection):
        self._database = connection
        self._watchers = self._initializeWatchers()

    def executeSqlStatement(self, statement: str) -> QueryContent:
        cursor = self._openCursor()
        cursor.execute(statement)
        result = cursor.fetchone()
        self._commitTransactionAndCloseCursor(cursor)
        return QueryContent(statement, result)

    def executeWatcherEvents(self):
        for event in self._checkWatchers():
            self._eventDispatcher.dispatch(event)

    def _checkWatchers(self) -> [WatcherValueChangedEvent]:
        watcherEvents = []
        for watch in self._watchers:
            watcherEvents.append(self._checkIndividualWatcher(watch))
        return filter(None, watcherEvents)

    def _checkIndividualWatcher(self, watcher: Watcher) -> WatcherValueChangedEvent:
        queryContent = self.executeSqlStatement(watcher.sqlStatement)
        return watcher.checkWatchedValue(queryContent)

    def _openCursor(self) -> psycopg2.extensions.cursor:
        cursor = self._database.cursor()
        return cursor

    def _commitTransactionAndCloseCursor(self, cursor: psycopg2.extensions.cursor):
        self._database.commit()
        cursor.close()

    def _initializeWatchers(self) -> [Watcher]:
        watchers = []
        config = self._getWatchersConfig()
        for watcherName in config:
            watchers.append(self._createWatcherFromConfig(
                watcherName, config[watcherName]))
        return watchers

    def _getWatchersConfig(self) -> dict:
        with open(WATCHER_CONFIG_FILEPATH) as configFile:
            config = yaml.safe_load(configFile)
        return config

    def _createWatcherFromConfig(self, name: str, properties: dict) -> Watcher:
        queryContent = self.executeSqlStatement(properties["sql"])
        return Watcher(
            name=name,
            properties=properties,
            queryContent=queryContent)


class ApplicationService:
    _dbConn: psycopg2.extensions.connection
    _watcherController: WatcherController

    def __init__(self):
        self._dbConn = self._openDBConnection()
        self._watcherController = self._initializeWatcherController()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._closeDBConnection()

    def triggerWatcherCheck(self):
        self._watcherController.executeWatcherEvents()

    def _initializeWatcherController(self) -> WatcherController:
        controller = WatcherController(self._dbConn)
        return controller

    def _openDBConnection(self) -> psycopg2.extensions.connection:
        connection = psycopg2.connect(
            host=HOST,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD
        )
        return connection

    def _closeDBConnection(self):
        self._dbConn.close()
