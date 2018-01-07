__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging
import urllib
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

from jinja2 import Environment, PackageLoader, select_autoescape

log = logging.getLogger(__name__)

env = Environment(
    loader=PackageLoader('alarmlistener', 'static'),
    autoescape=select_autoescape(['html', 'xml'])
)


class MonitorRequestHandler(BaseHTTPRequestHandler):
    """Re-used some code from SimpleHTTPRequestHandler to serve (template) files when found in the static
    folder. Set the correct headers etc.

    """

    def _get_translated_path(self):
        """Strip query parameters and parse the path to translate encoded characters"""

        path = urllib.parse.urlsplit(self.path).path
        try:
            path = urllib.parse.unquote(path, errors='surrogatepass')
        except UnicodeDecodeError:
            path = urllib.parse.unquote(path)
        return path

    def _send_get_headers(self, content_bytes=None):
        self.send_response(HTTPStatus.OK)
        if content_bytes is not None:
            self.send_header("Content-Length", str(len(content_bytes)))
            self.send_header("Last-Modified", self.date_time_string(None))  # None resolves to current timestamp

        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.end_headers()

    def do_HEAD(self):
        self._send_get_headers()

    def do_GET(self):
        # path = self._get_translated_path()
        # log.info('Path is {}, translated path is {}'.format(self.path, path))

        template = env.get_template('index.html')
        template_bytes = bytes(template.render({
            'last_event_timestamp': self.server.event_controller.get_last_event_timestamp(),
            'last_alarm_timestamp': self.server.event_controller.get_last_alarm_timestamp(),
            'last_email_timestamp': self.server.mailer.get_last_mail_timestamp()
        }), 'utf-8')
        self._send_get_headers(template_bytes)
        self.wfile.write(template_bytes)

    def do_PUT(self):
        log.debug('PUT request for path: {}'.format(self._get_translated_path()))
        try:
            if '/test-mail' == self._get_translated_path():
                self.server.mailer.send_mail('Test message from Alarm Listener', ignore_last_mail_timestamp=True)
                self.send_response(HTTPStatus.OK, 'Success sending test mail')
                self.end_headers()
            else:
                log.warning('Ignoring unexpected PUT request for path {}'.format(self._get_translated_path()))
                self.send_error(HTTPStatus.BAD_REQUEST, 'Request not supported')
        except Exception as e:
            log.exception('Caught exception when sending test mail')
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, 'Sending test mail failed; {}'.format(e))
