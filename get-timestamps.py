#!/usr/bin/env python
import sys
from datetime import datetime, timedelta
from math import ceil

try:
    interval_in_minutes = int(sys.argv[1])
except (IndexError, ValueError):
    interval_in_minutes = 30

now = datetime.now()
old_minute_count = now.minute
new_minute_count = int(ceil(old_minute_count / 15.)) * 15

timestamp1 = now + timedelta(minutes=(new_minute_count - old_minute_count))
timestamp2 = timestamp1 + timedelta(minutes=interval_in_minutes)
timestamp_format = '%Y%m%d-%H%M'
print('%s - %s: %s minutes' % (
    timestamp1.strftime(timestamp_format),
    timestamp2.strftime(timestamp_format),
    interval_in_minutes))
