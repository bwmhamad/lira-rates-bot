#!/usr/bin/env python3

from lxml import html
import requests
import dateparser
import datetime
from tzlocal import get_localzone
import json

local_tz = get_localzone()

def parse_line(line):
    date_string = line[0] + " " + line[1]
    date = dateparser.parse(date_string, settings = {'TIMEZONE': 'EEST', "TO_TIMEZONE": local_tz.tzname(datetime.datetime.now())})
    ts = int((date - datetime.datetime.fromtimestamp(0)).total_seconds())
    br = int(line[11].replace(",", ""))
    sr = int(line[10].replace(",", ""))
    return ts, br, sr, date_string
        

page=requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQKxp7P4c5bbgJf403C4r51yQDeDljC6-ETLLBPYEXX9q64iGSRo0PpPEtY4W68qOYEmFTiEfVKDkz3/pubhtml')
tree = html.fromstring(page.content)

latest = [x.text for x in tree.xpath('//tbody/tr[4]/td')]
previous = [x.text for x in tree.xpath('//tbody/tr[5]/td')]

ts, br, sr, date_string = parse_line(latest)
result = {'buy': br, 'sell': sr, 'time': date_string}
try:
    pts, pbr, psr, _ = parse_line(previous)
    result['db'] = br - pbr
    result['ds'] = sr - psr
    result['dts'] = ts - pts
except:
    pass

print(json.dumps(result))
