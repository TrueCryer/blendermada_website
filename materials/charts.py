import pygal

from django.http import HttpResponse

from django_pandas.io import read_frame

from .models import Material, Statistic


def response_svg_chart(chart):
    return HttpResponse(chart.render(), content_type='image/svg+xml')


def material_downloads(request, pk):
    qs = Statistic.objects.filter(material=pk)
    df = read_frame(qs)
    df = df.sort('date')
    chart = pygal.StackedLine(show_dots=False)
    chart.x_labels = df['date']
    chart.add('Material', df['count'])
    return response_svg_chart(chart)
