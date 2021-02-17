import requests
import re
import time
import json
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html5lib")
    d = dict()
    d['time'] = int(time.time())
    for x in soup.find_all('tr'):
        l = tuple(y.strip() for y in x.get_text().split('\n') if y)[0:-1]
        if len(l) != 2:
            continue
        d['_'.join(l[0].lower().split(' '))] = float(l[1])
    print(d)
    return d

def make_image(json_obj):
    demand = [json_obj[i]['actual_system_demand'] for i in range(len(json_obj))]
    capacity = [json_obj[i]['total_system_capacity_(not_including_ancillary_services)'] for i in range(len(json_obj))]
    times = [json_obj[i]['time'] for i in range(len(json_obj))]
    diffs = [x - y for x,y in zip(capacity,demand)]

    plt.plot(times, demand, label='demand')
    plt.plot(times, capacity, label='capacity')
    plt.plot(times, diffs, label='difference')

    plt.legend()
    plt.xlabel('time')
    plt.ylim(ymax=round(1.1*max(capacity)), ymin=min(0, min(diffs)))
    plt.savefig('graph.png')

def main():
    url = 'http://www.ercot.com/content/cdr/html/real_time_system_conditions.html'
    info_list = []
    while True:
        try:
            info = get_info(url)
            info_list.append(info)
            time.sleep(60*5)
        except KeyboardInterrupt:
            with open('out.json', 'w') as outfile:
                json.dump(info_list, outfile)
                make_image(info_list)
            break


if __name__ == '__main__':
        main()