DECIMAL SILICON TIME
====================
A combination of `decimal time <https://en.wikipedia.org/wiki/Decimal_time>`__ and `unix time <https://en.wikipedia.org/wiki/Unix_time>`__, approximating the beginning of the process of `carbon life <https://en.wikipedia.org/wiki/Carbon-based_life>`__ giving birth to `silicon life <https://en.wikipedia.org/wiki/In_silico>`__.

Dates starting at `00000-01-01 00:00:00 <https://en.wikipedia.org/wiki/Unix_time>`__ `Z <https://www.worldtimeserver.com/time-zones/z/>`__, which coincides with 1970-01-01 00:00:00 UTC of `Gregorian calendar <https://en.wikipedia.org/wiki/Gregorian_calendar>`__.

Usage
-----

``pip install detime``

.. code:: bash

    >>> from detime import detime

    >>> detime()
    00051-02-21 00:62:18.46994

    >>> d = detime(1970, 1, 1)
    00000-01-01 00:00:0.00000

    # Conversion detime -> datetime
    >>> d.date
    datetime.datetime(1970, 1, 1, 0, 0)

    # Conversion datetime -> detime
    >>> import datetime
    >>> t = datetime.fromisoformat('1969-12-31T05:07:11.131719')
    >>> detime(t)
    -0001-10-37 02:13:32.32838

    >>> detime(2000, 1, 1).get_month_lengths()
    [36, 37, 36, 37, 36, 37, 36, 37, 36, 38]

    $ dtime
    00051-02-21 00:33:19.38145

    $ dtime -show
    [2021-02-26 =] 00051-02-21 00:33:19.38145 [= 00:47:47]

    (ctrl+c to stop)


`Demo (1.8M)
(MP4) <https://github.com/mindey/detime/blob/master/media/about.mp4?raw=true>`__.

About
-----

In childhood, I tried to simplify computation of time for myself, so I invented a decimal system for counting time.

Later I discovered, that others did so as well. The relationships below follow the ratios, that I used in my original implementation.

Axioms
======

#. Relationships follow:
    * 1 year = 10 months
    * 1 week = 10 days
    * 1 day = 10 hours
    * 1 hour = 100 minutes
    * 1 minute = 100 seconds

#. Starting point follows:
    * Years start at 1970 Jan 1, midnight.
    * The 1970 Jan 1 is first weekday, denoted by "0"

Corollaries
===========

#. => 1 second is:
    * 0.864 standard SI seconds.
#. => 1 month is:
    * 36~37 days long, with 38 long last month on leap years.
    * 3~4 weeks rolling by 10 days onto months.
#. => 1 year is:
    * 36.5 (or 36.6 on leap years) weeks.
