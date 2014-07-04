"""
About this project
==================

Project for receiving Alarm system notifications.

Receives notifications via SIA or Contact-ID protocol. Passes them on to Android devices using the Google GCM Cloud Connect Server (XMPP).


Project Authors
===============

 * Miel Donkers (miel.donkers@gmail.com)

Current code lives on github: https://github.com/mdonkers/alarmlistener

"""

from alarmlistener import (
    # Modules

    # Files
    server, alarm_notification_handler
)

__all__ = [
    "server", "alarm_notification_handler"
]

__docformat__ = "epytext"
