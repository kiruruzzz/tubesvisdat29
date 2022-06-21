from bokeh.plotting import figure, ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.models import Panel, Spinner, ColorPicker
from bokeh.layouts import column, row
import pandas as pd
from bokeh.io import curdoc, show
from bokeh.models.widgets import Tabs
from bokeh.plotting import output_file
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable
from bokeh.transform import factor_mark


from os.path import dirname, join
import pandas as pd


# from kodingan.barplot import barplot
# from kodingan.marker_map import marker_map
# from kodingan.lineplot import lineplot
# from kodingan.table import table


def table(df):
        source = ColumnDataSource(df)

	    # Columns of table
        columns = [TableColumn(field='YEAR', title='Year'),
					 TableColumn(field='MOVIE', title='Movie Title'),
					 TableColumn(field='MPAARATING', title='MPAA Rating'),
					 TableColumn(field='DISTRIBUTOR', title='Distributor'),
					 TableColumn(field='TOTALFORYEAR', title='Total For Year ($)'),
					 TableColumn(field='TOTALIN2019DOLLARS', title='Total in 2019 Dollars'),
                     TableColumn(field='TICKETSSOLD', title='Tickets Sold')]

        data_table = DataTable(source=source, columns=columns, width=1000, height=700)
        tab4 = Panel(child = data_table, title = 'TABLE')

        return tab4


def marker_map(df):
    source = ColumnDataSource(df)

    # Movie list
    movies = sorted(df.MOVIE)

    MARKERS = ['asterisk', 'circle', 'circle_cross', 'circle_dot', 'circle_x', 'circle_y', 
    'cross', 'diamond', 'diamond_cross','dash','diamond_dot','dot','hex','hex_dot','inverted_triangle',
    'plus','square','square_cross','square_dot','square_pin','square_x','star','star_dot','triangle',
    'triangle_dot','triangle_pin','x','y']

    p2 = figure(
        plot_width=1500,
        plot_height=800,
        title='MOVIES INCOME BY TICKETS SOLD',
        x_axis_label='TICKETS SOLD',
        y_axis_label='TOTAL FOR YEAR (k $)',
    )

    points = p2.scatter(
        'TICKETSSOLD',
        'TOTALFORYEAR',
        size=20,
        color='grey',
        fill_alpha=0.5,
        marker=factor_mark('MOVIE',MARKERS, movies),
        legend_group='MOVIE',
        source=source,
    )

    p2.legend.orientation = "vertical"
    p2.legend.background_fill_color = "#fafafa"
    p2.legend.location = 'bottom_right'

    # Add Tooltips
    hover = HoverTool()
    hover.tooltips = """
      <div>
        <h3>@MOVIE</h3>
        <div><strong>Year: </strong>@YEAR</div>
        <div><strong>Genre: </strong>@GENRE</div>
        <div><strong>MPAA: </strong>@MPAARATING</div>
        <div><strong>Distributor: </strong>@DISTRIBUTOR</div>
        <div><strong>Total $ For Year: $</strong>@TOTALFORYEAR</div>
        <div><strong>Tickets Sold: </strong>@TICKETSSOLD</div>
      </div>
    """
    p2.add_tools(hover)

    #spinner points size
    spinner1 = Spinner(title="Points Size", low=1, high=50, step=2, value=20, width=100)
    spinner1.js_link('value', points.glyph, 'size')

    #spinner points fill alpha
    spinner2 = Spinner(title="Points Fill Alpha", low=0.1, high=1, step=0.1, value=0.5, width=100)
    spinner2.js_link('value', points.glyph, 'fill_alpha')

    #picker points color
    picker = ColorPicker(title="Points Color", width = 100)
    picker.js_link('color', points.glyph, 'fill_color')

    widgets = column(spinner1, spinner2, picker)

    layout = row(widgets, p2)

    tab2 = Panel(child=layout, title="MARKER MAP")

    return tab2




def lineplot(df):
    source = ColumnDataSource(df)

    p3 = figure(
        plot_width=1500,
        plot_height=800,
        title='MOVIES INCOME BY TICKETS SOLD',
        x_axis_label='YEAR',
        y_axis_label='TICKETS SOLD',
    )

    # Add Tooltips
    hover = HoverTool()
    hover.tooltips = """
      <div>
        <h3>@MOVIE</h3>
        <div><strong>Year: </strong>@YEAR</div>
        <div><strong>Genre: </strong>@GENRE</div>
        <div><strong>MPAA: </strong>@MPAARATING</div>
        <div><strong>Distributor: </strong>@DISTRIBUTOR</div>
        <div><strong>Total $ For Year: $</strong>@TOTALFORYEAR</div>
        <div><strong>Tickets Sold: </strong>@TICKETSSOLD</div>
      </div>
    """
    p3.add_tools(hover)

    line =  p3.line(x='YEAR', y='TICKETSSOLD', line_width=3, source=source)

    #spinner line width
    spinner = Spinner(title="Line Width", low=1, high=20, step=1, value=3, width=100)
    spinner.js_link('value', line.glyph, 'line_width')

    #picker line color
    picker = ColorPicker(title="Line Color", width = 100)
    picker.js_link('color', line.glyph, 'line_color')

    widgets = column(spinner, picker)

    layout = row(widgets, p3)


    tab3 = Panel(child=layout, title="LINE PLOT")


    return tab3



def barplot(df):
    # Create ColumnDataSource from data frame
    source = ColumnDataSource(df)

    # Movie list
    movie_list = source.data['MOVIE'].tolist()
    movie_list.reverse()

    # Add plot
    p1 = figure(
        y_range=movie_list,
        plot_width=1800,
        plot_height=1000,
        title='MOVIES TOP TICKETS SOLD PER YEAR',
        x_axis_label='TICKETS SOLD',
        y_axis_label='TITLE',
        tools="zoom_in,zoom_out,save,reset",
        toolbar_location='above'
    )

    # Render glyph
    bar =  p1.hbar(
        y='MOVIE',
        right='TICKETSSOLD',
        left=0,
        height=0.6,
        fill_color='orange',
        color = 'black',
        fill_alpha=0.5,
        source=source,
    )


    # Add Tooltips
    hover = HoverTool()
    hover.tooltips = """
      <div>
        <h3>@MOVIE</h3>
        <div><strong>Year: </strong>@YEAR</div>
        <div><strong>Genre: </strong>@GENRE</div>
        <div><strong>MPAA: </strong>@MPAARATING</div>
        <div><strong>Distributor: </strong>@DISTRIBUTOR</div>
        <div><strong>Total $ For Year: $</strong>@TOTALFORYEAR</div>
        <div><strong>Tickets Sold: </strong>@TICKETSSOLD</div>
      </div>
    """
    p1.add_tools(hover)

    #spinner bar height
    spinner1 = Spinner(title="Bar Height", low=0.1, high=1, step=0.1, value=0.6, width=100)
    spinner1.js_link('value', bar.glyph, 'height')

    #spinner bar fill alpha
    spinner2 = Spinner(title="Bar Fill Alpha", low=0.1, high=1, step=0.1, value=0.5, width=100)
    spinner2.js_link('value', bar.glyph, 'fill_alpha')

    #picker bar color
    picker = ColorPicker(title="Bar Color", width = 100)
    picker.js_link('color', bar.glyph, 'fill_color')

    widgets = column(spinner1, spinner2, picker)

    layout = row(widgets, p1)

    tab1 = Panel(child=layout, title="BAR PLOT")

    return tab1

output_file('TUBES.html')

df = pd.read_csv('HighestGrossers.csv')
curdoc().theme = 'dark_minimal'

tab1 = barplot(df)
tab2 = marker_map(df)
tab3 = lineplot(df)
tab4 = table(df)

tabs = Tabs(tabs=[tab1,tab2,tab3,tab4])

show(tabs)