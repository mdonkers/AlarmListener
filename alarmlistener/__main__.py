__author__ = 'mieldonkers'

"""
    alarmlistener.__main__
    ~~~~~~~~~~~~~~

    Alias for server.run for the command line, for when this module is directly executed as "python -m alarmlistener"
"""

if __name__ == '__main__':
    from .server import run
    run()
