#!/bin/bash
echo ""
echo "Running Python AlarmListener Server"
echo ""

BASE_DIR=`dirname $0`

(cd ${BASE_DIR}/../ && python3 -m alarmlistener) # >/dev/null 2>&1)

exit 0
