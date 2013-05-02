#!/usr/bin/env python

import csv
import json

from bs4 import BeautifulSoup
import requests

stations = []

for pageid, channel in [('10001', 'ROCK/POP/ & FOLK'), ('10003', 'CLASSICAL'), ('10002', 'JAZZ & BLUES'), ('10006', 'OTHER')]:
    url = 'http://www.npr.org/templates/websites/musicstreams.php?t=%s' % pageid
    r = requests.get(url)
    soup = BeautifulSoup(r.content)

    sub_stations = []

    station_list = soup.select('ul.mainlist li')

    for station in station_list:

        station_dict = {}
        station_dict['channel'] = channel
        station_dict['name'] = station.select('div.wrapid%s span.name' % pageid)[0].string
        station_dict['tagline'] = station.select('div.wrapid%s p.tagline' % pageid)[0].string
        station_dict['location'] = station.select('div.wrapid%s span.location' % pageid)[0].string
        station_dict['call_sign'] = station.select('span.lnk')[0].string
        station_dict['available_streams'] = station.select('a.arrow')[0]['href']
        sub_stations.append(station_dict)

    counter = 0
    for possible_image in soup.select('div#wrapper script')[11].string.split(';'):
        try:
            sub_stations[counter]['img_url'] = possible_image.strip().split('="')[1].split('.gif"')[0] + ".gif"
            counter += 1
        except:
            pass

    stations += sub_stations

with open('www/live-data/stations.json', 'wb') as station_json:
    station_json.write('loadStations(%s)' % json.dumps(stations))

with open('www/live-data/stations.csv', 'wb') as station_csv:
    stationwriter = csv.DictWriter(station_csv, ['channel', 'name', 'call_sign', 'tagline', 'location', 'available_streams', 'img_url'])
    for station in stations:
        stationwriter.writerow(station)
