import configparser
import logging
import os
from logging import INFO

__author__ = 'Miel Donkers <miel.donkers@gmail.com>'

log = logging.getLogger(__name__)

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

SMTP_ADDRESS = config.get('MAIL', 'smtp_address', fallback=os.getenv('MAIL_SMTP_ADDRESS'))
SMTP_USERNAME = config.get('MAIL', 'smtp_username', fallback=os.getenv('MAIL_SMTP_USERNAME'))
SMTP_PASSWORD = config.get('MAIL', 'smtp_password', fallback=os.getenv('MAIL_SMTP_PASSWORD'))
FROM_ADDRESS = config.get('MAIL', 'from_address', fallback=os.getenv('MAIL_FROM_ADDRESS'))
TO_ADDRESS = config.get('MAIL', 'to_address', fallback=os.getenv('MAIL_TO_ADDRESS'))

BACKOFF_TIMEOUT_IN_SEC = config.get('MAIL', 'backoff_timeout_in_sec', fallback=os.getenv('MAIL_BACKOFF_TIMEOUT_IN_SEC'))
HEARTBEAT_INTERVAL_SEC = config.get('ALARM', 'heartbeat_interval_sec', fallback=os.getenv('ALARM_HEARTBEAT_INTERVAL_SEC'))
LOG_LEVEL = config.get('ALARM', 'log_level', fallback=os.getenv('ALARM_LOG_LEVEL'))


#
# Raise error for mandatory parameters
#
if any(param is None for param in [SMTP_ADDRESS, SMTP_USERNAME, SMTP_PASSWORD, FROM_ADDRESS, TO_ADDRESS]):
    log.error('One or more mandatory parameters are unset, please check the configuration and try again')
    raise ValueError('One or more mandatory parameters are unset, please check the configuration and try again')

#
# Set defaults for all variables or convert them to the correct format
#
if BACKOFF_TIMEOUT_IN_SEC is None or HEARTBEAT_INTERVAL_SEC is None:
    log.warning('Some config values are EMPTY, check if correctly set!')

if BACKOFF_TIMEOUT_IN_SEC is None:
    BACKOFF_TIMEOUT_IN_SEC = 3600
else:
    BACKOFF_TIMEOUT_IN_SEC = int(BACKOFF_TIMEOUT_IN_SEC)

if HEARTBEAT_INTERVAL_SEC is None:
    HEARTBEAT_INTERVAL_SEC = 600
else:
    HEARTBEAT_INTERVAL_SEC = int(HEARTBEAT_INTERVAL_SEC)

if LOG_LEVEL is None:
    LOG_LEVEL = INFO
else:
    LOG_LEVEL = LOG_LEVEL.upper()
