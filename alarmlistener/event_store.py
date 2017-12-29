__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

import logging

from sqlalchemy import create_engine, MetaData, Column, Table, Integer, DateTime, select, desc


log = logging.getLogger(__name__)


class EventStore:
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
            log.debug('Event inserted correctly, generated primary key: {}'.format(result.inserted_primary_key))

    def find_last_events(self, max_events=2):
        """
        Return the last alarm events that were stored in the database, ordered from most recent to oldest.
        :param max_events: The maximum number of events to query for, default = 2
        :return: Ordered list of alarm events, from most recent to oldest
        """
        connection = self.engine.connect()

        select_statement = select([self.alarm_events]).order_by(desc("timestamp")).limit(max_events)
        result = connection.execute(select_statement)

        timestamp_results = tuple(row[self.alarm_events.c.timestamp] for row in result)
        log.debug('Got result from alarm_events, query limited to {max} records. Results: {rows}'
                  .format(max=max_events, rows=', '.join(str(tstamp) for tstamp in timestamp_results)))

        result.close()
        connection.close()
        return timestamp_results
