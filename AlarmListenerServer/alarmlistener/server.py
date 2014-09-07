"""
This is the base-class for the AlarmListener Server
"""

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import time
import logging
import socketserver
import threading

from alarmlistener.alarm_notification_handler import AlarmNotificationHandler

log = logging.getLogger(__name__)
HOST, PORT = '', 32001


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def _init_log():
    # create console handler with with formatting and log level
    _formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    _console_handler = logging.StreamHandler()
    _console_handler.setLevel(logging.DEBUG)
    _console_handler.setFormatter(_formatter)
    # add the handlers to the logger
    _root_logger = logging.getLogger()
    _root_logger.addHandler(_console_handler)
    _root_logger.setLevel(logging.DEBUG)


def run():
    log.info('Starting Server...')

    # Create the server, binding to HOST on PORT
    server = ThreadedTCPServer((HOST, PORT), AlarmNotificationHandler)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    log.info('Server loop running in thread: %s', server_thread.name)

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        log.info('Ctrl-c pressed, exiting ...')
        server.shutdown()


#-----------------------------------------------------------------
# Main
#-----------------------------------------------------------------
_init_log()


if __name__ == '__main__':
    run()
