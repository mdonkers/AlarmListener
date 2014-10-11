__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging

from sqlalchemy import create_engine, MetaData, Column, Table, Integer, DateTime


log = logging.getLogger(__name__)


class EventStore():
    """
    The EventStore manages database connections and provides methods to store alarm notification events and retrieve them.

    As this object references an SQLAlchemy Engine object, only one EventStore instance should be created per application.
    """

    def __init__(self):
        # Init de database connection
        self.engine = create_engine('sqlite:///alarm_events.db')
        # Table definition
        metadata = MetaData()
        self.alarm_events = Table('alarm_events', metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('timestamp', DateTime, nullable=False))
        # Init the database, creates corresponding tables when not available
        metadata.create_all(self.engine)

    def close(self):
        """
        Dispose of the connection-pool, releasing all connections
        """
        self.engine.dispose()

    def store_event(self, timestamp):
        with self.engine.begin() as connection:
            result = connection.execute(self.alarm_events.insert(), timestamp=timestamp)
            log.debug('Event insert result: {}'.format(result))

    def find_last_events(self, max_events=2):
        connection = self.engine.connect()

        result = connection.execute('SELECT * FROM alarm_events ORDER BY timestamp LIMIT ?', max_events)
        log.debug('Last events query result with max={}, result: {}'.format(max_events, result))

        result.close()
        connection.close()


# for row in result:
#     print "username:", row['username']
