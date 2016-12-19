import datetime
from collections import deque
import pytz

__version__ = 0.3
"""
Indicator for timeseries with tails of min and max.
author = uchood

"""

class TimeDate(object):

    def __init__(self, value, time):
        self.v = value
        self.t = time


class MinMaxIndicator(object):
    time_tail_in_sec = 10

    def __init__(self, len_of_time_series_in_sec=None):
        super(MinMaxIndicator, self).__init__()
        self.max_tail = deque()
        self.min_tail = deque()
        self.current_val = TimeDate(0, 0)
        if len_of_time_series_in_sec is not None:
            self.time_tail_in_sec = len_of_time_series_in_sec
        self.is_empty = True

    def clear_deque_by_time(self, current_time, time_tail):
        while len(time_tail) > 0:
            delta_time_in_sec = (current_time - time_tail[0].t).total_seconds()
            if delta_time_in_sec > self.time_tail_in_sec:
                time_tail.popleft()
            else:
                break

    def clear_deque_by_max(self, time_tail, new_value):
        while len(time_tail) > 0:
            if time_tail[-1].v <= new_value.v:
                time_tail.pop()
            else:
                break
        time_tail.append(new_value)

    def clear_deque_by_min(self, time_tail, new_value):
        while len(time_tail) > 0:
            if time_tail[-1].v >= new_value.v:
                time_tail.pop()
            else:
                break
        time_tail.append(new_value)

    def update_current_time(self, time=None):
        current_time = time
        if current_time is None:
            current_time = datetime.datetime.utcnow()
        self.clear_deque_by_time(current_time, self.max_tail)
        self.clear_deque_by_time(current_time, self.min_tail)

    def put_value(self, value, time=None):
        current_time = datetime.datetime.utcnow()
        if time is not None:
            current_time = time
        self.current_val = TimeDate(value, current_time)
        self.update_current_time(current_time)
        self.clear_deque_by_max(self.max_tail, self.current_val)
        self.clear_deque_by_min(self.min_tail, self.current_val)

    def get_min_last_max(self):
        return self.min_tail[0].v, self.current_val.v, self.max_tail[0].v
