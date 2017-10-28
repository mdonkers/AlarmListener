import unittest
from unittest.mock import MagicMock, patch

from alarmlistener.alarm_notification_handler import AlarmNotificationHandler
from alarmlistener.event_controller import EventController


class TestAlarmNotificationHandler(unittest.TestCase):

    def test_handle_method_triggers_alarm_event_on_controller(self):
        server_mock = MagicMock()
        server_mock.event_controller.mock_add_spec(EventController)

        # Instantiation of object already calls 'handle()' method
        AlarmNotificationHandler(MagicMock(), MagicMock(), server_mock)

        self.assertTrue(server_mock.event_controller.trigger_alarm_event.called)
        self.assertEqual(server_mock.event_controller.trigger_alarm_event.call_count, 1)

    @patch('alarmlistener.alarm_notification_handler.log')
    def test_exception_raised_on_socket_close_should_log_message(self, log_mock):
        server_mock = MagicMock()
        request_mock = MagicMock()
        request_mock.close.side_effect = OSError('some exception')

        # Instantiation of object already calls 'handle()' method
        AlarmNotificationHandler(request_mock, MagicMock(), server_mock)

        self.assertTrue(log_mock.debug.called)
        self.assertTrue(log_mock.warn.called)
        self.assertEqual(log_mock.warn.call_count, 1)
        self.assertFalse(server_mock.event_controller.trigger_alarm_event.called, msg="Trigger Alarm Event should not have been called")
