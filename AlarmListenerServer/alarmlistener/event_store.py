__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

from sqlalchemy import create_engine
import logging

log = logging.getLogger(__name__)


class EventStore():

    def __init__(self):
        self.engine = create_engine('sqlite:///alarm_events.db')

    def store_event(self):
        self.engine.connect()
