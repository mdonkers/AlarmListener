from _datetime import datetime

import logging

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)


class EventController():
    def __init__(self, event_store, event_heartbeat_in_sec):
        self.event_store = event_store
        self.event_heartbeat = event_heartbeat_in_sec

    def trigger_alarm_event(self):
        log.info('Controller received alarm event')
        self.event_store.store_event(datetime.utcnow())

        # get last 2 events and check whether they are too close or too far apart
        last_events = self.event_store.find_last_events()

        if len(last_events) < 2:
            log.info('Not enough events to determine if alarm event. # events returned = {}'.format(len(last_events)))
            return

        delta_time = last_events[0] - last_events[1]  # Assume they are delivered ordered as per the query from EventStore.find_last_events()
        log.debug('Delta time between last two events = {} seconds'.format(str(delta_time.total_seconds())))

        heartbeat_deviation = self.event_heartbeat - delta_time.total_seconds()
        heartbeat_margin = self.event_heartbeat // 50
        if heartbeat_deviation < -heartbeat_margin or heartbeat_deviation > heartbeat_margin:
            log.warn('Events received out of heartbeat range, must be something wrong!! Delta time = {}'.format(str(delta_time.total_seconds() // 1)))
