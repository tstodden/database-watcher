from typing import List

import yaml
from psycopg2.pool import ThreadedConnectionPool

from .config import Config
from .constants import DATABASE, HOST, PASSWORD, USER, WATCHER_CONFIG_FILEPATH
from .models import QueryResult, QueryResultChangedEvent
from .query import Query


class QueryController:
    def __init__(self):
        self._dbpool: ThreadedConnectionPool = self._initialize_dbpool()
        self._queries: List[Query] = self._initialize_queries()

    def check_queries(self) -> List[QueryResultChangedEvent]:
        events = list()
        for query in self._queries:
            result = self._execute_sql(query.sql)
            if query.check(result):
                events.append(
                    QueryResultChangedEvent(query.name, query.value)
                )
        return events

    def _initialize_queries(self) -> List[Query]:
        all_queries = list()
        for query_config in self._get_configs():
            config = Config(query_config)
            all_queries.append(self._create_query(config))
        return all_queries

    def _initialize_dbpool(self) -> ThreadedConnectionPool:
        return ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            host=HOST,
            dbname=DATABASE,
            user=USER,
            password=PASSWORD
        )

    def _get_configs(self) -> List[dict]:
        with open(WATCHER_CONFIG_FILEPATH) as f:
            config = yaml.safe_load(f)
        return config

    def _create_query(self, config: Config) -> Query:
        result = self._execute_sql(config.sql)
        return Query(
            config=config,
            result=result
        )

    def _execute_sql(self, sql: str) -> QueryResult:
        try:
            conn = self._dbpool.getconn()
            curs = conn.cursor()
            curs.execute(sql)
            result = curs.fetchone()
            conn.commit()
        except:
            conn.rollback()
        curs.close()
        self._dbpool.putconn(conn)
        return QueryResult(sql, result)
