DECIMAL TIME
============

Usage
-----

``pip install detime``

.. code:: bash

    >>> from detime import detime

    >>> detime()
    0051-02-21 00:62:18.46994

    >>> d = detime(1970, 1, 1)
    0000-01-01 00:00:0.00000

    >>> d.date
    datetime.datetime(1970, 1, 1, 0, 0)

    >>> detime(2000, 1, 1).get_month_lengths()
    [36, 37, 36, 37, 36, 37, 36, 37, 36, 38]

    $ dtime
    0051-02-21 00:33:19.38145

    $ dtime -show
    [2021-02-26 =] 0051-02-21 00:33:19.38145 [= 00:47:47]

    (ctrl+c to stop)


`Demo (1.8M)
(MP4) <https://github.com/mindey/detime/blob/master/media/about.mp4?raw=true>`__.

About
-----

In childhood, I tried to simplify computation of time for myself, so I
invented a decimal system for counting time.

1 year = 10 months 1 week = 10 days 1 day = 10 hours 1 hour = 100
minutes 1 minute = 100 seconds

=> 1 second = 0.864 standard SI seconds. => 1 month = 3~4 weeks.

Years start at 1970 Jan 1, midnight.
