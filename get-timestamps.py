#!/usr/bin/env python
import math
from argparse import ArgumentParser
from datetime import datetime, timedelta


def get_timestamps(interval_in_minutes=30, with_next=False):
    method = getattr(math, 'ceil' if with_next else 'floor')

    now = datetime.now()
    old_minute_count = now.minute
    new_minute_count = int(method(old_minute_count / 15.)) * 15

    timestamp1 = now + timedelta(minutes=(new_minute_count - old_minute_count))
    timestamp2 = timestamp1 + timedelta(minutes=interval_in_minutes)
    return timestamp1, timestamp2


if __name__ == '__main__':
    argument_parser = ArgumentParser()
    argument_parser.add_argument(
        '-i', '--interval_in_minutes', type=int, default=30)
    argument_parser.add_argument(
        '-n', '--next', action='store_true')
    args = argument_parser.parse_args()

    timestamp1, timestamp2 = get_timestamps(
        args.interval_in_minutes, args.next)
    timestamp_format = '%Y%m%d-%H%M'
    print('%s - %s: %s minutes' % (
        timestamp1.strftime(timestamp_format),
        timestamp2.strftime(timestamp_format),
        args.interval_in_minutes))
