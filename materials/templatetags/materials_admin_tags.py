from __future__ import unicode_literals

from django import template

from ..reports import StatisticReport as SR


register = template.Library()


@register.inclusion_tag('materials/admin_statistic.html')
def statistic_report():
    sr = SR()
    return {
        'count_by_day': sr.get_svg_count_by_day(),
        'count_by_month': sr.get_svg_count_by_month(),
    }
