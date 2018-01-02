"""
This is the base-class for the AlarmListener Server
"""

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import time
import logging
import socketserver
import threading

from http.server import HTTPServer

from alarmlistener.monitor_request_handler import MonitorRequestHandler
from alarmlistener.config import LOG_LEVEL, HEARTBEAT_INTERVAL_SEC, BACKOFF_TIMEOUT_IN_SEC, SMTP_ADDRESS, SMTP_USERNAME, SMTP_PASSWORD, FROM_ADDRESS, TO_ADDRESS
from alarmlistener.mailer import Mailer
from alarmlistener.event_controller import EventController
from alarmlistener.alarm_notification_handler import AlarmNotificationHandler
from alarmlistener.event_store import EventStore

log = logging.getLogger(__name__)
ALARM_HOST, ALARM_PORT = '', 32001
MONITOR_HOST, MONITOR_PORT = '', 8080


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Own TCPServer class, also extending from ThreadingMixIn to support multi-threading and
    extending the __init__ method so we can set a reference to our Event Controller
    """

    def __init__(self, server_address, request_handler_class, event_controller):
        super().__init__(server_address, request_handler_class)
        self.event_controller = event_controller


class ThreadedMonitorServer(socketserver.ThreadingMixIn, HTTPServer):
    """
    Own Threaded HTTP Server to run as daemon thread
    """

    def __init__(self, server_address, request_handler_class, event_controller, mailer):
        super().__init__(server_address, request_handler_class)
        self.event_controller = event_controller
        self.mailer = mailer


def _init_log():
    # create console handler with with formatting and log level
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _console_handler = logging.StreamHandler()
    _console_handler.setLevel(LOG_LEVEL)
    _console_handler.setFormatter(_formatter)
    # add the handlers to the logger
    _root_logger = logging.getLogger()
    _root_logger.addHandler(_console_handler)
    _root_logger.setLevel(LOG_LEVEL)


def _run_threaded(server_class):
    # Start a thread with the server -- that thread will then start one more thread for each request
    server_thread = threading.Thread(target=server_class.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    log.info('Server loop running in thread: %s', server_thread.name)


def run():
    # Instantiate Controller and EventStore
    mailer = Mailer(BACKOFF_TIMEOUT_IN_SEC, SMTP_ADDRESS, SMTP_USERNAME, SMTP_PASSWORD, FROM_ADDRESS, TO_ADDRESS)
    event_store = EventStore()
    event_controller = EventController(event_store, event_heartbeat_in_sec=HEARTBEAT_INTERVAL_SEC, mailer=mailer)

    log.info('Starting Monitor site...')
    httpd = ThreadedMonitorServer((MONITOR_HOST, MONITOR_PORT), MonitorRequestHandler, event_controller, mailer)
    _run_threaded(httpd)

    log.info('Starting Alarm Server...')
    alarm_server = ThreadedTCPServer((ALARM_HOST, ALARM_PORT), AlarmNotificationHandler, event_controller)
    _run_threaded(alarm_server)

    event_controller.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info('Ctrl-c pressed, exiting ...')
        alarm_server.shutdown()
        httpd.shutdown()
        event_store.close()


# -----------------------------------------------------------------
# Main
# -----------------------------------------------------------------
_init_log()


if __name__ == '__main__':
    run()
