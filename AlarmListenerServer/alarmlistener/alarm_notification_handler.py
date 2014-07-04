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
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        # log.debug("{} wrote:".format(self.client_address[0]))
        # log.debug(self.data)
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())

        data = str(self.request.recv(1024), 'ascii')
        log.debug("{}: {}".format(self.client_address[0], data))
        # response = bytes("{}: {}".format(data), 'ascii')
        # self.request.sendall(response)
