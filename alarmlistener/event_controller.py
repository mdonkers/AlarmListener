from datetime import datetime, timedelta
from threading import Thread
import sched
import logging
import time


__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)


class EventController:
    def __init__(self, event_store, event_heartbeat_in_sec, mailer):
        self.event_store = event_store
        self.event_heartbeat = event_heartbeat_in_sec
        self.mailer = mailer

    def start(self):
        t = EventCheckScheduler(event_store=self.event_store, event_heartbeat_in_sec=self.event_heartbeat, mailer=self.mailer)
        t.daemon = True
        log.info('Event Controller loop running in thread: %s', t.name)
        t.start()
        return

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
        heartbeat_margin = self.event_heartbeat // 200
        if heartbeat_deviation < -heartbeat_margin or heartbeat_deviation > heartbeat_margin:
            log.warning('Events received out of heartbeat range, must be something wrong!! Delta time = {} seconds'.format(str(delta_time.total_seconds() // 1)))
            self.mailer.sendMail('Events received out of heartbeat range ({}), delta time = {} seconds'.format(str(self.event_heartbeat), str(delta_time.total_seconds() // 1)))

    def get_last_event_timestamp(self):
        events = self.event_store.find_last_events(max_events=1)
        return events[0] if len(events) > 0 else None


class EventCheckScheduler(Thread):
    def __init__(self, event_store, event_heartbeat_in_sec, mailer):
        super().__init__()
        self.event_store = event_store
        self.event_heartbeat = event_heartbeat_in_sec
        self.mailer = mailer

    def run(self):
        log.debug('Starting job scheduler for regular checking alarm events')
        mailer = self.mailer

        def alarm_event_verification_worker():
            log.info('Checking delay in alarm events stored')
            last_event = next(iter(self.event_store.find_last_events(max_events=1)))
            if _is_event_delta_falsify(last_event, self.event_heartbeat):
                log.warning('Events received out of heartbeat range, must be something wrong!!')
                mailer.sendMail('No event received within expected range; {}'.format(str(last_event)))

            # Re-schedule ourself
            reschedule_time = datetime.now() + timedelta(seconds=self.event_heartbeat)
            scheduler.enterabs(reschedule_time.timestamp(), 1, alarm_event_verification_worker)
            return

        scheduler = sched.scheduler(time.time, time.sleep)
        first_time = datetime.now() + timedelta(seconds=self.event_heartbeat)
        scheduler.enterabs(first_time.timestamp(), 1, alarm_event_verification_worker)
        scheduler.run()
        return


def _is_event_delta_falsify(timestamp_event, event_heartbeat):
    if timestamp_event is None:
        return True  # There should have been an event.

    delta_time = timestamp_event - datetime.utcnow()
    if delta_time.total_seconds() > (event_heartbeat + 5):
        return True

    return False
