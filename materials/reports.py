from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pygal

from django.http import HttpResponse

from django_pandas.io import read_frame

from .models import Statistic


class StatisticReport(object):
    def __init__(self):
        self.df = read_frame(
            Statistic.objects.filter(
                date__gte=(datetime.now()-timedelta(days=365))
            )
        )
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
        df_mean_15 = pd.rolling_apply(self.all_by_day['count'], 15, np.mean)[-15:].to_frame()
        df_mean_30 = pd.rolling_apply(self.all_by_day['count'], 30, np.mean)[-15:].to_frame()
        df_mean_60 = pd.rolling_apply(self.all_by_day['count'], 60, np.mean)[-15:].to_frame()
        chart = pygal.Line(width=960, height=480, interpolate='cubic', explicit_size=True, x_label_rotation=35)
        chart.title = "Count of downloads by day"
        chart.x_labels = map(lambda d: d.strftime('%d %b'), df.index)
        chart.add('Downloads', df['count'])
        chart.add('15-days mean', df_mean_15['count'])
        chart.add('30-days mean', df_mean_30['count'])
        chart.add('60-days mean', df_mean_60['count'])
        return chart.render()
    def get_svg_count_by_month(self):
        df = self.all_by_day.resample('M', how='sum')[-10:]
        chart = pygal.Bar(width=960, height=480, explicit_size=True, show_legend=False)
        chart.title = "Count of downloads by month"
        chart.x_labels = map(lambda d: d.strftime('%Y-%m'), df.index)
        chart.add('Downloads', df['count'])
        return chart.render()
