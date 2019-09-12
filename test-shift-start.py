import requests
import time
from datetime import datetime
from datetime import timedelta
from pytz import timezone
import calendar
def get_gluer_resets(delta_seconds, timestamp):
    payload = {'query': "resets(gluers:running[{0}s])".format(delta_seconds), 'time': timestamp}
    r = requests.get("http://localhost:9090/api/v1/query", params=payload)
    print(r.url)
    return r.json()
def make_prom_message(results):
    gluer_stops = []
    for result in results:
        gluer_stops.append({'stops': result['value'], 'instance': result['metric']['exported_instance']})

    print(gluer_stops)
def send_to_prom(asset_id, shiftvalue, dayvalue, timestamp):
    counter_data = ""
    counter_data += '# TYPE gluers:stops counter\n'
    counter_data += 'gluers:stops{{period="day",instance={2}}} {0} {1}\n'.format(dayvalue, int(timestamp*1000, asset_id))
    counter_data += 'gluers:stops{{period="shift",instance={2}}} {0} {1}\n'.format(shiftvalue, int(timestamp*1000, asset_id))
    r = requests.post('http://localhost:9091/metrics/job/infrastructure', data=counter_data)
    print(r.text)
while 1:
    CxT_now = datetime.now(timezone('US/Central'))
    CxT_now = CxT_now.replace(hour=6)
    hour = CxT_now.hour
    day = CxT_now.day
    record = True
    naive_day_start_time = CxT_now.replace(hour=5, minute=0, second=0, microsecond=0)
    oneday = timedelta(days=1)
    if hour in range(5, 15):
        day_start_time = naive_day_start_time
        print(day_start_time)
        print(CxT_now)
        shift_start_time = day_start_time
        time_since_shift_start = int((CxT_now - shift_start_time).total_seconds())
        time_since_day_start = time_since_shift_start
        message = ""
        now_timestamp = calendar.timegm(CxT_now.astimezone(timezone('UTC')).timetuple())
        make_prom_message(get_gluer_resets(time_since_shift_start, now_timestamp)['data']['result'])
    elif hour in range(15,24) + [0]:
        if hour == 0:
            day_start_time = naive_day_start_time - oneday
        shift_start_time = day_start_time.replace(hour=15)
    else:
        record = False
    if record:
        message = ""
        now_timestamp = calendar.timegm(CxT_now.astimezone(timezone('UTC')).timetuple())




    time.sleep(5)

