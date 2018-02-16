import logging
import textwrap
from datetime import datetime

import requests

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)

MSG_BIRD_BASE_URI = 'https://rest.messagebird.com'
MSG_BIRD_API_BALANCE = '/balance'
MSG_BIRD_API_MESSAGE = '/messages'


class SmsSender:

    def __init__(self, sms_backoff_timeout_in_sec, sms_api_key, sms_from_number, sms_to_number):
        self.backoff_timeout_in_sec = sms_backoff_timeout_in_sec
        self.sms_api_key = sms_api_key
        self.sms_from_number = sms_from_number
        self.sms_to_number = sms_to_number

        self.last_sms_timestamp = datetime.min

    def get_last_sms_timestamp(self):
        return self.last_sms_timestamp

    def get_remaining_credit(self):
        headers = {'Authorization': 'AccessKey ' + self.sms_api_key, 'accept': 'application/json'}
        resp = requests.get(MSG_BIRD_BASE_URI + MSG_BIRD_API_BALANCE, headers=headers)
        log.debug('Balance response: ' + str(resp.json()))
        return str(resp.json()['amount']) + ' ' + resp.json()['type']

    def send_sms(self, message, ignore_last_sms_timestamp=False):
        if not ignore_last_sms_timestamp and (
                datetime.utcnow() - self.last_sms_timestamp).total_seconds() < self.backoff_timeout_in_sec:
            log.warning('Not sending SMS, recently already sent an SMS')
            return

        log.info('Trying to send SMS with text: {}'.format(str(message)))

        try:
            trimmed_message = textwrap.shorten(str(message), 100)
            headers = {'Authorization': 'AccessKey ' + self.sms_api_key, 'accept': 'application/json'}
            payload = {'type': 'sms',
                       'originator': self.sms_from_number,
                       'body': 'Alarm notification! Unexpected event: {}'.format(trimmed_message),
                       'recipients': [self.sms_to_number]}
            resp = requests.post(MSG_BIRD_BASE_URI + MSG_BIRD_API_MESSAGE, headers=headers, data=payload)
            log.info('SMS response: ' + str(resp.json()))

            if not ignore_last_sms_timestamp:
                self.last_sms_timestamp = datetime.utcnow()
        except requests.exceptions.RequestException:
            log.exception('Failed to send SMS!')
