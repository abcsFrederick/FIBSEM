#!/bin/bash

echo -e "* * * * * /tmp/snapshot.sh $module > /var/log/cron.log 2>&1\n#end" > /tmp/cronJob

crontab /tmp/cronJob && tail -f /var/log/cron.log