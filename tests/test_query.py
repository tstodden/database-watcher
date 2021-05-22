from watcher.models import QueryResult
from watcher.query import Query

TEST_RESULT_1 = QueryResult("SELECT test_1;", ("Hello", "World"))

TEST_RESULT_2 = QueryResult("SELECT test_2;", ("Goodbye", "World"))
TEST_HASH_2 = "aa54794c1f89160723f29cc6e677852f1d5e0597"


class TestQuery():
    def test_no_change_in_value(self):
        sut = Query(None, TEST_RESULT_1)

        got = sut.check(TEST_RESULT_1)

        want = False
        assert got == want

    def test_change_in_value(self):
        sut = Query(None, TEST_RESULT_1)

        got = sut.check(TEST_RESULT_2)

        want = True
        assert got == want


class TestQueryResult():
    def test_query_result_hash(self):
        sut = TEST_RESULT_2

        got = sut.get_result_hash()

        want = TEST_HASH_2
        assert got == want
