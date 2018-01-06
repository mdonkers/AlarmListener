import logging
import sched
import time
from datetime import datetime, timedelta
from threading import Thread

HEARTBEAT_MARGIN_DIV = 200

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)


class EventController:
    def __init__(self, event_store, event_heartbeat_in_sec, mailer):
        self.event_store = event_store
        self.event_heartbeat = event_heartbeat_in_sec
        self.mailer = mailer
        self.last_alarm_timestamp = None

    def start(self):
        t = EventCheckScheduler(event_store=self.event_store,
                                event_heartbeat_in_sec=self.event_heartbeat,
                                alarm_notification_callback=self._send_alarm_notifications)
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

        # Assume they are delivered ordered as per the query from EventStore.find_last_events()
        delta_time = last_events[0] - last_events[1]
        log.debug('Delta time between last two events = {} seconds'.format(str(delta_time.total_seconds())))

        heartbeat_deviation = self.event_heartbeat - delta_time.total_seconds()
        heartbeat_margin = self.event_heartbeat // HEARTBEAT_MARGIN_DIV
        if heartbeat_deviation < -heartbeat_margin or heartbeat_deviation > heartbeat_margin:
            self._send_alarm_notifications(
                'Events received out of heartbeat range, must be something wrong!! Delta time = {} seconds'.format(
                    str(delta_time.total_seconds() // 1)),
                'Events received out of heartbeat range ({}), delta time = {} seconds'.format(
                    str(self.event_heartbeat),
                    str(delta_time.total_seconds() // 1))
            )

    def _send_alarm_notifications(self, log_msg, mail_msg):
        self.last_alarm_timestamp = datetime.utcnow()
        log.warning(log_msg)
        self.mailer.send_mail(mail_msg)

    def get_last_event_timestamp(self):
        events = self.event_store.find_last_events(max_events=1)
        return events[0] if len(events) > 0 else None

    def get_last_alarm_timestamp(self):
        return self.last_alarm_timestamp


class EventCheckScheduler(Thread):
    def __init__(self, event_store, event_heartbeat_in_sec, alarm_notification_callback):
        super().__init__()
        self.event_store = event_store
        self.event_heartbeat = event_heartbeat_in_sec
        self.alarm_notification_callback = alarm_notification_callback

    def run(self):
        log.debug('Starting job scheduler for regular checking alarm events')

        def alarm_event_verification_worker():
            log.info('Checking delay in alarm events stored')
            last_event = next(iter(self.event_store.find_last_events(max_events=1)))
            if _is_event_delta_falsify(last_event, self.event_heartbeat):
                self.alarm_notification_callback('Events received out of heartbeat range, must be something wrong!!',
                                                 'No event received within expected range; {}'.format(str(last_event)))

            # Re-schedule ourselves
            reschedule_time = datetime.now() + timedelta(seconds=self.event_heartbeat)
            scheduler.enterabs(reschedule_time.timestamp(), 1, alarm_event_verification_worker)
            return

        scheduler = sched.scheduler(time.time, time.sleep)
        first_time = datetime.now() + timedelta(seconds=(self.event_heartbeat * 1.5))
        scheduler.enterabs(first_time.timestamp(), 1, alarm_event_verification_worker)
        scheduler.run()
        return


def _is_event_delta_falsify(timestamp_event, event_heartbeat):
    if timestamp_event is None:
        return True  # There should have been an event.

    delta_time = datetime.utcnow() - timestamp_event
    if delta_time.total_seconds() > (event_heartbeat + (event_heartbeat // HEARTBEAT_MARGIN_DIV)):
        return True

    return False
