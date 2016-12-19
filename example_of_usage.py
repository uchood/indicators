import datetime
import time
import random

from max_min_indicator import MinMaxIndicator

"""
example of usage MinMaxIndicator for logging cpu time series
"""

time_tail_in_sec = 5

indicator = MinMaxIndicator(time_tail_in_sec)

interval_in_sec = 20
end_time = datetime.datetime.utcnow() + datetime.timedelta(0,interval_in_sec)
while datetime.datetime.utcnow() < end_time:
    val = random.random() * 100.0
    print("time :  {} ++++++++".format(datetime.datetime.utcnow()))

    indicator.put_value(val)
    min_tail = [y.v for y in indicator.min_tail]
    max_tail = [y.v for y in indicator.max_tail]
    min_v, cur_v, max_v = indicator.get_min_last_max()
    
    print("max tail: {}".format(max_tail))
    print("{}: {}: {}".format(min_v, cur_v, max_v))
    print("min tail: {}".format(min_tail))
    
    time.sleep(0.01)
