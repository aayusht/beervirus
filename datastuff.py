from urllib.request import urlopen
import io
import json
import datetime
import numpy as np

def fetch_json():
    with io.open('timeseries-byLocation.json', mode='r', encoding='utf-8') as f:
        return json.loads(f.read())
    # with urlopen('https://coronadatascraper.com/timeseries-byLocation.json') as url:
    #     return json.loads(url.read())

def __get_values(place, key, data):
    to_date = lambda datestr: datetime.datetime.strptime(datestr, '%Y-%m-%d')
    first_date = to_date('2020-1-22')
    latest_date = to_date(list(data['United States']['dates'].keys())[-1])
    days = (latest_date - first_date).days + 1
    timeseries = np.empty(days)
    timeseries.fill(np.nan)
    for datestr, timeseries_point in data[place]['dates'].items():
        index = (to_date(datestr) - first_date).days
        if index >= days:
            continue
        timeseries[index] = timeseries_point.get(key, np.nan)
    return timeseries

def get_cases(data):
    return {place:__get_values(place, 'cases', data) for place in data.keys()}

def get_deaths(data):
    return {place:__get_values(place, 'deaths', data) for place in data.keys()}

def get_active(data):
    return {place:__get_values(place, 'active', data) for place in data.keys()}

def get_recovered(data):
    return {place:__get_values(place, 'recovered', data) for place in data.keys()}
