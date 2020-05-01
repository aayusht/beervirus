from flask import Flask, render_template, redirect, request
from markupsafe import escape
from plots import plot
from numpy import nan_to_num
app = Flask(__name__)

import datastuff

data = datastuff.fetch_json()
population = datastuff.get_population(data)
dates = datastuff.get_dates(data)
cases = datastuff.get_cases(data)
deaths = datastuff.get_deaths(data)
recovered = datastuff.get_recovered(data)

current_places = ['United States']

is_country = lambda name: data[name]['level'] == 'country'
is_us_state = lambda name: data[name]['level'] == 'state' and data[name]['country'] == 'United States'

def place_str(place):
    pop = population[place]
    return '%s (pop %s)' % (place, f'{pop:,}')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    data_list = [cases[place] for place in current_places]
    if request.method == 'POST':
        query = request.form.get('place')
        if query in cases.keys() and query not in current_places:
            current_places.append(query)
        function = request.form.get('function')
        try:
            data_list = [eval(function) for place in current_places]
        except:
            data_list = [cases[place] for place in current_places]
    script, div, js_resources, css_resources = plot(dates, data_list, current_places)
    return render_template(
        'index.html',
        current_places=current_places,
        places=filter(is_country, list(cases.keys())),
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )
# @app.route('/data')
# def data_page():
#     content = ''
#     for place in data.keys():
#         if (is_country(place) or is_us_state(place)) and data[place]['population'] > 1000000:
#             content += '%s cases: %s\n\n' % (place_str(place), str(cases[place]))
#     return content

    