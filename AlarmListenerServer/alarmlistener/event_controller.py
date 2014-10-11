from _datetime import datetime

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging

log = logging.getLogger(__name__)


class EventController():

    def __init__(self, event_store):
        self.event_store = event_store

    def trigger_alarm_event(self):
        log.info('Controller received alarm event')
        self.event_store.store_event(datetime.utcnow())

        # TODO get last 2 events and check whether they are too close or too far apart
        self.event_store.find_last_events(3)
