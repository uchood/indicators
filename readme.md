Indicator for timeseries with tails of min and max.


```python

import datetime
import time
import random

from max_min_indicator import MinMaxIndicator

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

```


Example for send cpu series to zabbix with min-max tail

```python
import time
import psutil

from pyzabbix import ZabbixMetric, ZabbixSender

from max_min_indicator import MinMaxIndicator

time_tail_in_sec = 10
indicator = MinMaxIndicator(time_tail_in_sec)
while True:    
    val = psutil.cpu_percent(interval=1)
    indicator.put_value(val)
    min_v, cur_v, max_v = indicator.get_min_last_max()
    metrics= [ZabbixMetric('fors', 'cpu_min', min_v),ZabbixMetric('fors', 'cpu[usage]', val),ZabbixMetric('fors', 'cpu_max', max_v)]
    ZabbixSender('192.168.115.143').send(metrics)
    time.sleep(1)
```