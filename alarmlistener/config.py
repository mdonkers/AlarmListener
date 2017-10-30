import configparser
import logging
import os
from logging import INFO

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

HEARTBEAT_INTERVAL_MIN = config.get('ALARM', 'heartbeat_interval_min', fallback=os.getenv('ALARM_HEARTBEAT_INTERVAL_MIN'))
LOG_LEVEL = config.get('ALARM', 'log_level', fallback=os.getenv('ALARM_LOG_LEVEL'))

if HEARTBEAT_INTERVAL_MIN is None:
    log.warning(
        'Some config values are EMPTY, check if correctly set! HEARTBEAT_INTERVAL_MIN={}'.format(HEARTBEAT_INTERVAL_MIN))


#
# Set defaults for all variables or convert them to the correct format
#
if HEARTBEAT_INTERVAL_MIN is None:
    HEARTBEAT_INTERVAL_MIN = 10
else:
    HEARTBEAT_INTERVAL_MIN = int(HEARTBEAT_INTERVAL_MIN)

if LOG_LEVEL is None:
    LOG_LEVEL = INFO
else:
    LOG_LEVEL = LOG_LEVEL.upper()
