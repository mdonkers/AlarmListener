from unittest import TestCase
from unittest.mock import MagicMock, patch
from alarmlistener.event_store import EventStore


class TestEventStore(TestCase):

    @patch('alarmlistener.event_store.create_engine')
    def test_close_of_event_store(self, create_engine_mock):
        sut_event_store = EventStore()

        sut_event_store.close()

        self.assertTrue(create_engine_mock().dispose.called)

    @patch('alarmlistener.event_store.create_engine')
    def test_store_event(self, create_engine_mock):
        sut_event_store = EventStore()

        sut_event_store.store_event(MagicMock())

        self.assertTrue(create_engine_mock().begin.called)
        self.assertTrue(create_engine_mock().begin().__enter__().execute.called)
        self.assertTrue(create_engine_mock().begin().__exit__.called)

    @patch('alarmlistener.event_store.create_engine')
    def test_find_last_events_returned_in_correct_order(self, create_engine_mock):
        test_results = MagicMock(), MagicMock()
        create_engine_mock().connect().execute().__iter__.return_value = test_results
        sut_event_store = EventStore()

        timestamp_results = sut_event_store.find_last_events()

        self.assertTrue(create_engine_mock().connect().execute.called)
        self.assertIs(type(timestamp_results), tuple)
        self.assertEqual(len(test_results), len(timestamp_results))
