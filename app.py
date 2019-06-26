from flask import Flask, render_template, request

from bokeh.embed import server_document, components
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import pandas as pd
from datetime import datetime


app = Flask(__name__)

stock_symbol = ['MSFT', 'AAPL', 'GOOG', 'AMZN', 'INTC']

# Setup plot


def get_plot(s):
    p = figure(plot_width=600, plot_height=300,
               title='Value at Close of Day (May 2019)', x_axis_type="datetime", x_axis_label='Date', y_axis_label='Value at Close')
    p.title.text_font_size = '16pt'
    p.xaxis.axis_label_text_font_size = '12pt'
    p.yaxis.axis_label_text_font_size = '12pt'

    df = pd.read_csv(
        'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + s + '&apikey=QVAR360OY5QS7IL3&datatype=csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')

    dMay = df.loc['2019-05']
    dMay = dMay.reset_index()

    x = dMay['timestamp']
    y = dMay['close']
    source = ColumnDataSource(dict(x=x, y=y))

    p.line('x', 'y', source=source, line_color='green', line_width=3)
    return p


@app.route('/')
def homepage():

    current_stock = request.args.get("Stock Symbol")
    if current_stock == None:
        current_stock = "TSLA"

    # Create the plot
    plot = get_plot(current_stock)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)
    return render_template("index.html", script=script, div=div, stock_symbol=stock_symbol, current_stock=current_stock)


if __name__ == '__main__':
    app.run()
