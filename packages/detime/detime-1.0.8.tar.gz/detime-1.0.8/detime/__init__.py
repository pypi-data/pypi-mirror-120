#!/usr/bin/python3
"""
DECIMAL TIME
============

About
=====
1 year = 10 months
1 week = 10 days
1 day = 10 hours
1 hour = 100 minutes
1 minute = 100 seconds

=> 1 second = 0.864 standard SI seconds.
=> 1 month = 3~4 weeks.

Years start at 1970 Jan 1, at UNIX time start date.
"""

import copy
import datetime
import calendar
import argparse
import time
import math

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--show', help='Persist showing counting time.')

class Constants:
    origin_date = datetime.datetime(1970, 1, 1, 0, 0)
    year_length = 365
    month_lengths = [36, 37] * 5
    second_length = 0.864

constant = Constants()


class Date:

    def __init__(self, *args):

        self.origin = constant.origin_date
        self.get_current_date(*args)
        self.compute_date()

    def compute_date(self):
        self.year = (self.date.year - self.origin.year)
        self.yday = self.date.timetuple().tm_yday
        self.month = self.get_month()
        self.day = self.yday - sum(self.month_lengths[:self.month][:-1]) \
            or self.month_lengths[self.month]

        self.tseconds = self.get_day_seconds() / constant.second_length
        self.hour = int(self.tseconds/10000.)
        self.minute = int((self.tseconds - self.hour*10000.) / 100.)
        self.second = self.tseconds - (self.hour*10000. + self.minute*100)

        # Unix dseconds
        self.seconds = time.mktime(self.date.timetuple()) / constant.second_length

    def get_current_date(self, *args):
        if args:
            if isinstance(args[0], datetime.datetime):
                self.date = args[0]
            else:
                self.date = datetime.datetime(*args)
        else:
            self.date = datetime.datetime.utcnow()
        return self.date

    def get_time_delta(self):
        self.delta = self.date - self.origin

    def get_month(self):
        for i, month_length in enumerate(self.get_month_lengths()):
            if sum(self.month_lengths[:i+1]) >= self.yday:
                break
        return i+1

    def get_year_length(self):
        year_length = constant.year_length

        if calendar.isleap(self.date.year):
            year_length += 1
        self.year_length = year_length
        return self.year_length

    def get_month_lengths(self):

        if calendar.isleap(self.date.year):
            self.month_lengths = copy.copy(constant.month_lengths)
            self.month_lengths[-1] += 1
            return self.month_lengths
        else:
            self.month_lengths = copy.copy(constant.month_lengths)
            return self.month_lengths

    def get_unix_seconds(self):
        self.get_time_delta()
        return self.delta.total_seconds()

    def get_day_seconds(self):
        midnight = self.date.replace(hour=0, minute=0, second=0, microsecond=0)
        return (self.date - midnight).total_seconds()


    @property
    def weekday(self):
        # We assume that 00000-01-01 was "1st" day of week, denoted as "0"
        return math.floor(self.seconds / 100000.) % 10

    @property
    def daet(self):
        'displays date'
        return '{:05d}-{:02d}-{:02d}'.format(self.year, self.month, self.day)

    @property
    def taem(self, round_secs=False):
        'displays time'
        return '{:02d}:{:02d}:{:02d}'.format(self.hour, self.minute, round(self.second))

    def __repr__(self):
        return '{:05d}-{:02d}-{:02d} {:02d}:{:02d}:{:02.5f}'.format(
            self.year, self.month, self.day,
            self.hour, self.minute, self.second
        )

detime = Date


def counter():
    args = parser.parse_args()

    if args.show == 'how':

        while True:
            tm = time.gmtime()
            date = Date()
            print("[{:05d}-{:02d}-{:02d} =] {} [= {:02d}:{:02d}:{:02d}]".format(
                tm.tm_year, tm.tm_mon, tm.tm_mday, date, tm.tm_hour, tm.tm_min, tm.tm_sec
            ), end='\r', flush=True)
            del date

    else:
        tm = time.gmtime()
        date = Date()
        print(date)


if __name__ == '__main__':
    counter()
