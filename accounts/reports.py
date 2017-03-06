from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pygal

from django.contrib.auth import get_user_model
from django.http import HttpResponse

from django_pandas.io import read_frame


class UserReport(object):
    def __init__(self):
        self.df = read_frame(
            get_user_model().objects.filter(
                date_joined__gte=(datetime.now() - timedelta(days=15))
            )
        )
        self.df['date_joined'] = pd.to_datetime(self.df['date_joined'])

        # TODO: Optimise next queries
        self.active = self.df[self.df.is_active==True][
            ['date_joined', 'id']
        ].groupby('date_joined').count().resample('D').count()
        self.nonactive = self.df[self.df.is_active==False][
            ['date_joined', 'id']
        ].groupby('date_joined').count().resample('D').count()

    def get_svg_count_by_day(self):
        chart = pygal.StackedBar(
            width=960, height=480,
            explicit_size=True,
            show_legend=False
        )
        chart.title = "Registered users by day"
        chart.x_labels = map(lambda d: d.strftime('%d'), self.active.index)
        chart.add('Activated', self.active['id'])
        chart.add('Non-activated', self.nonactive['id'])
        return chart.render()
