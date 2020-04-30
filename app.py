from flask import Flask, render_template, redirect, request
from markupsafe import escape
from plots import plot
from numpy import nan_to_num
app = Flask(__name__)

import datastuff

data = datastuff.fetch_json()
cases = datastuff.get_cases(data)
deaths = datastuff.get_deaths(data)
recovered = datastuff.get_recovered(data)

is_country = lambda name: data[name]['level'] == 'country'
is_us_state = lambda name: data[name]['level'] == 'state' and data[name]['country'] == 'United States'

def place_str(place):
    pop = data[place]['population']
    return '%s (pop %s)' % (place, f'{pop:,}')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    place = 'United States'
    if request.method == 'POST':
        query = request.form['place']
        if query in cases.keys():
            place = query
    script, div, js_resources, css_resources = plot(list(range(len(cases[place]))), cases[place])
    return render_template(
        'index.html',
        places=filter(is_country, list(cases.keys())),
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )\

@app.route('/<place>')
def place_data(place):
    dates = list(data[place]['dates'].keys())
    place_cases = nan_to_num(cases[place])
    place_deaths = nan_to_num(deaths[place])
    timeseries = [{'cases': int(place_cases[i]), 'deaths': int(place_deaths[i]), 'date':dates[i]} for i in range(len(dates))]
    population = data[place]['population']
    return render_template('place_data.html', place=place, timeseries=timeseries, pop=population)
# @app.route('/data')
# def data_page():
#     content = ''
#     for place in data.keys():
#         if (is_country(place) or is_us_state(place)) and data[place]['population'] > 1000000:
#             content += '%s cases: %s\n\n' % (place_str(place), str(cases[place]))
#     return content

    