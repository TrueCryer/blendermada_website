import numpy as np
import pandas as pd
import pygal

from django.http import HttpResponse

from django_pandas.io import read_frame

from .models import Statistic


class StatisticReport(object):
    def __init__(self):
        self.df = read_frame(Statistic.objects.all())
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['count'] = pd.to_numeric(self.df['count'])
        self.all_by_day = self.df[['date', 'count']].groupby('date').sum()
    def get_html_count_by_day(self):
        return self.all_by_day[-15:].to_html()
    def get_html_rolling_mean(self):
        return pd.rolling_apply(self.all_by_day['count'], 60, np.mean)[-15:].to_frame().to_html()
    def get_html_count_by_month(self):
        return self.all_by_day.resample('M', how='sum')[-6:].to_html()
    def get_svg_count_by_day(self):
        df = self.all_by_day[-15:]
        chart = pygal.Line(width=640, height=480, explicit_size=True, show_legend=False, fill=True)
        chart.title = "Count of downloads by day"
        chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), df.index)
        chart.add('Downloads', df['count'])
        return chart.render()
    def get_svg_rolling_mean(self):
        df = pd.rolling_apply(self.all_by_day['count'], 60, np.mean)[-15:].to_frame()
        chart = pygal.Line(width=640, height=480, explicit_size=True, show_legend=False, fill=False)
        chart.title = "Rolling mean count of downloads with 60-days period"
        chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), df.index)
        chart.add('Downloads', df['count'])
        return chart.render()
    def get_svg_count_by_month(self):
        df = self.all_by_day.resample('M', how='sum')[-6:]
        chart = pygal.Bar(width=640, height=480, explicit_size=True, show_legend=False, fill=False)
        chart.title = "Count of downloads by month"
        chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), df.index)
        chart.add('Downloads', df['count'])
        return chart.render()


def stat_report(request):
    sr = StatisticReport()
    template = """
    <h3>Count by day</h3>
    {by_day}
    <h3>Average</h3>
    {average}
    <h3>Count by month</h3>
    {by_month}
    """.format(
        by_day=sr.get_html_count_by_day(),
        average=sr.get_html_rolling_mean(),
        by_month=sr.get_html_count_by_month(),
    )
    return HttpResponse(template, content_type='text/plain')
