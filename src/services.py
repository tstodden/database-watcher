import psycopg2

from .core import Watcher, QueryContent

HOST = "localhost"
DATABASE = "tyler"
USER = "tester"
PASSWORD = "tester"


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
        watchers.append(Watcher(self.executeSqlStatement(
            "SELECT date_trunc('minute', now());")))
        return watchers

    # TODO: cleanup
    def checkWatchers(self):
        for watch in self._watchers:
            queryContent = self.executeSqlStatement(watch.sqlStatement)
            if watch.checkWatchedValue(queryContent):
                print(
                    f"An event was triggered with statement: {watch.sqlStatement} resulting in hash: {watch._watchedValue}")


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
        self._watcherController.checkWatchers()
