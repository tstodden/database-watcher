import unittest

from src.core import Watcher, QueryContent, WatcherValueChangedEvent

TEST_DATA1 = QueryContent("SELECT test_1;", ("Hello", "World"))
TEST_DATA2 = QueryContent("SELECT test_2;", ("Goodbye", "World"))

TEST_HASH2 = "aa54794c1f89160723f29cc6e677852f1d5e0597"

TEST_EVENT2 = WatcherValueChangedEvent(
    watcherName="test", watchedValue=TEST_HASH2)


class TestWatcher(unittest.TestCase):
    def test_no_change_in_watched_value(self):
        sut = Watcher("test", {"sql": ""}, TEST_DATA1)

        result = sut.checkWatchedValue(TEST_DATA1)

        self.assertIsNone(result)

    def test_change_in_watched_value(self):
        sut = Watcher("test", {"sql": ""}, TEST_DATA1)

        result = sut.checkWatchedValue(TEST_DATA2)

        self.assertEqual(TEST_EVENT2, result)
