__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging

log = logging.getLogger(__name__)


class EventController():

    def trigger_alarm_event(self):
        log.info('Controller received alarm event')
