import numpy as np
from bokeh.embed import components
from bokeh.models.ranges import Range1d
from bokeh.plotting import figure
from bokeh.resources import INLINE

def plot(x, y):
    fig = figure(
        plot_width=600,
        plot_height=600,
        y_range=Range1d(0, max(y) * 1.1, bounds=(-1, None)),
        x_range=Range1d(0, len(x) * 1.1, bounds=(-1, None))
    )
    fig.line(x=x, y=y, color='blue')
    fig.circle(x=x, y=y, color='blue')
    fig.left[0].formatter.use_scientific = False

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(fig)
    return script, div, js_resources, css_resources

