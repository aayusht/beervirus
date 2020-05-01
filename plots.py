import numpy as np
from collections import defaultdict
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.palettes import Dark2_5 as palette
import itertools 
from datetime import timedelta

def get_source(dates, labels, data_list):
    data = defaultdict(list)
    for label, y in zip(labels, data_list):
        data['date'].append(dates)
        data['place'].append(label)
        data['timeseries'].append(y)
    data['color'] = palette
    return ColumnDataSource(data)

def plot(dates, data_list, labels):
    source = get_source(dates, labels, data_list)

    max_data = max(max(data) for data in data_list)
    fig = figure(
        x_axis_type='datetime',
        sizing_mode='stretch_both',
        x_range=Range1d(dates[0], dates[-1] + timedelta(days=2), bounds=(dates[0] - timedelta(days=1), None)),
        y_range=Range1d(-max_data * 0.01, max_data * 1.1, bounds=(-max_data * 0.01, None))
    )
    fig.left[0].formatter.use_scientific = False
    
    fig.multi_line(
        xs='date',
        ys='timeseries',
        legend='place',
        line_width=3,
        line_color='color',
        line_alpha=0.6,
        hover_line_color='color',
        hover_line_alpha=1.0,
        source=source
    )
    
    fig.legend.location = "top_left"

    fig.add_tools(HoverTool(
        show_arrow=False,
        line_policy='next',
        tooltips=[
            ('Date', '@date{%Y-%m-%d}'),
            ('Place', '@place'),
            ('Value', '$timeseries')
        ],
        formatters={'date': 'datetime'},
        mode='vline'
    ))

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    return script, div, js_resources, css_resources

