__author__ = 'mieldonkers'

import logging

log = logging.getLogger(__name__)


def run():
    log.info("hello world")
    print
    print("usage    : ./compare.py <file 1> <file 2> .. <file n>")
    print
    print("example  : ./compare.py ContentProxy.properties.tstcell12 properties.out")
    print


#-----------------------------------------------------------------
# Main
#-----------------------------------------------------------------

if __name__ == '__main__':
    run()
