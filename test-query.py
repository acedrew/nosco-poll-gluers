import requests
import time

def get_gluer_status():
    timestamp = time.time()
    payload = {'query': "gluers:running", 'time': timestamp}
    r = requests.get("http://localhost:9090/api/v1/query", params=payload)
    return r.json()
def send_to_prom(asset_id, value, timestamp):
    counter_data = ""
    counter_data += '# TYPE stops counter\n'
    counter_data += 'stops{{instance="{2}"}} {0} {1}\n'.format(value, int(timestamp*1000), asset_id)
    r = requests.post('http://localhost:9091/metrics/job/gluers', data=counter_data)
    print(r.text)

gluers_status = get_gluer_status()
gluers = {}
for gluer_status in gluers_status['data']['result']:
    gluers[gluer_status['metric']['exported_instance']] = gluer_status['value'][1]
    gluers[gluer_status['metric']['exported_instance'] + " stops"] = 0
print(gluers)
while 1:
    timestamp = time.time()
    gluers_status_check = get_gluer_status()
    for gluer in gluers_status_check['data']['result']:
        asset_id = gluer['metric']['exported_instance']
        value = gluer['value'][1]
        if gluers[asset_id] != value and value == '0':
            gluers[asset_id + " stops"] += 1
            print(gluers)
            send_to_prom(asset_id, gluers[asset_id + " stops"], timestamp)

        gluers[asset_id] = value

    time.sleep(5)
