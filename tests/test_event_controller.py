from _datetime import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch
from alarmlistener.event_controller import EventController
from alarmlistener.event_store import EventStore
from alarmlistener.mailer import Mailer


class TestEventController(TestCase):

    def setUp(self):
        self.mailer = MagicMock(spec=Mailer)

    @patch('alarmlistener.event_controller.datetime')
    def test_storing_new_event_with_current_utc_timestamp(self, datetime_mock):
        mocked_utc_time = datetime(2000, 1, 1)
        datetime_mock.utcnow.return_value = mocked_utc_time
        event_store_mock = MagicMock(spec=EventStore)
        sut_event_controller = EventController(event_store_mock, 600, self.mailer)

        sut_event_controller.trigger_alarm_event()

        event_store_mock.store_event.assert_called_once_with(mocked_utc_time)

    @patch('alarmlistener.event_controller.log')
    def test_do_nothing_if_less_than_two_events_returned(self, log_mock):
        event_store_mock = MagicMock(spec=EventStore)
        event_store_mock.find_last_events.return_value = datetime(2000, 1, 1),
        sut_event_controller = EventController(event_store_mock, 600, self.mailer)

        sut_event_controller.trigger_alarm_event()

        last_call_args = log_mock.info.call_args  # Returns arguments of last call
        self.assertIn('Not enough events', last_call_args[0][0])  # last_call_args = tuple containing tuple

    @patch('alarmlistener.event_controller.log')
    def test_log_warning_if_events_too_far_apart(self, log_mock):
        event_store_mock = MagicMock(spec=EventStore)
        event_store_mock.find_last_events.return_value = datetime(2000, 1, 1, 12, 6, 34), datetime(2000, 1, 1, 12, 5, 32)
        sut_event_controller = EventController(event_store_mock, 600, self.mailer)

        sut_event_controller.trigger_alarm_event()

        self.assertTrue(log_mock.warning.called)
        last_call_args = log_mock.warning.call_args  # Returns arguments of last call
        self.assertIn('out of heartbeat range', last_call_args[0][0])  # last_call_args = tuple containing tuple

    @patch('alarmlistener.event_controller.log')
    def test_log_warning_if_events_too_close_together(self, log_mock):
        event_store_mock = MagicMock(spec=EventStore)
        event_store_mock.find_last_events.return_value = datetime(2000, 1, 1, 12, 6, 30), datetime(2000, 1, 1, 12, 5, 32)
        sut_event_controller = EventController(event_store_mock, 600, self.mailer)

        sut_event_controller.trigger_alarm_event()

        self.assertTrue(log_mock.warning.called)
        last_call_args = log_mock.warning.call_args  # Returns arguments of last call
        self.assertIn('out of heartbeat range', last_call_args[0][0])  # last_call_args = tuple containing tuple

    @patch('alarmlistener.event_controller.log')
    def test_do_nothing_if_delta_timestamps_within_expected_range(self, log_mock):
        event_store_mock = MagicMock(spec=EventStore)
        event_store_mock.find_last_events.return_value = datetime(2000, 1, 1, 12, 15, 33), datetime(2000, 1, 1, 12, 5, 31)
        sut_event_controller = EventController(event_store_mock, 600, self.mailer)

        sut_event_controller.trigger_alarm_event()

        self.assertFalse(log_mock.warning.called)
