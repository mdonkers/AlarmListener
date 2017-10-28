Project for receiving Alarm system notifications.
[![Build Status](https://travis-ci.org/mdonkers/AlarmListener.png)](https://travis-ci.org/mdonkers/AlarmListener)

Receives notifications via SIA or Contact-ID protocol. Passes them on to Android devices using the Google GCM Cloud Connect Server (XMPP).

## Docker build and run
Building container:

    docker build -t alarm-listener .

Running container:

    docker pull miel/alarm-listener
    docker run -d -p 32001:32001 --name alarm-listener miel/alarm-listener

## Docker Repo
Automatic builds: [https://hub.docker.com/r/miel/alarm-listener/](https://hub.docker.com/r/miel/alarm-listener/)

