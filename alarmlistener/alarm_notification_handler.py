"""
Handles receiving of the alarm notification messages on the TCP/IP socket
"""
__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging
import socketserver

log = logging.getLogger(__name__)


class AlarmNotificationHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):

        try:
            log.debug('Socket open... Connection received from {}.'.format(self.client_address[0]))
            # Close connection because we expect no data
            self.request.close()
            log.debug('Socket connection closed...')

            # Pass event on to Event Controller
            self.server.event_controller.trigger_alarm_event()

        except OSError as error:
            log.warning('Got error while reading from socket {}'.format(error.args[0]), exc_info=error)
