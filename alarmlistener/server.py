"""
This is the base-class for the AlarmListener Server
"""

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import time
import logging
import socketserver
import threading

from alarmlistener.config import LOG_LEVEL, HEARTBEAT_INTERVAL_MIN
from alarmlistener.event_controller import EventController
from alarmlistener.alarm_notification_handler import AlarmNotificationHandler
from alarmlistener.event_store import EventStore

log = logging.getLogger(__name__)
HOST, PORT = '', 32001


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Own TCPServer class, also extending from ThreadingMixIn to support multi-threading and
    extending the __init__ method so we can set a reference to our Event Controller
    """

    def __init__(self, server_address, RequestHandlerClass, event_controller):
        super().__init__(server_address, RequestHandlerClass)
        self.event_controller = event_controller


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


def run():
    # Instantiate Controller and EventStore
    event_store = EventStore()
    event_controller = EventController(event_store, event_heartbeat_in_sec=HEARTBEAT_INTERVAL_MIN * 60)

    log.info('Starting Server...')

    # Create the server, binding to HOST on PORT
    server = ThreadedTCPServer((HOST, PORT), AlarmNotificationHandler, event_controller)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    log.info('Server loop running in thread: %s', server_thread.name)
    event_controller.start()

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info('Ctrl-c pressed, exiting ...')
        server.shutdown()
        event_store.close()


# -----------------------------------------------------------------
# Main
# -----------------------------------------------------------------
_init_log()


if __name__ == '__main__':
    run()
