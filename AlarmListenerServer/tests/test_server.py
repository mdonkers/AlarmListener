from unittest.case import TestCase
from unittest.mock import MagicMock, patch
from alarmlistener import server


class TestServer(TestCase):

    @patch('alarmlistener.server.logging')
    def test_init_log(self, logging_mock):
        server._init_log()

        self.assertTrue(logging_mock.getLogger().setLevel.called)
        self.assertTrue(logging_mock.getLogger().addHandler.called)

    # Take care for the order of multiple mock parameters, fed bottom-up as parameters
    @patch('alarmlistener.server.ThreadedTCPServer')
    @patch('alarmlistener.server.EventStore')
    @patch('alarmlistener.server.EventController')
    @patch('alarmlistener.server.threading')
    @patch('alarmlistener.server.time')
    def test_starting_server(self, time_mock, threading_mock, EventController_mock, EventStore_mock, ThreadedTCPServer_mock):
        time_mock.sleep.side_effect = KeyboardInterrupt('some exception when pressing ctrl-c')

        server.run()

        self.assertTrue(threading_mock.Thread().start.called)
        self.assertTrue(ThreadedTCPServer_mock().shutdown.called)
        self.assertTrue(EventStore_mock().close.called)
