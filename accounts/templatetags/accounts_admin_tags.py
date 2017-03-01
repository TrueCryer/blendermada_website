from django import template

from ..reports import UserReport as UR


register = template.Library()


@register.inclusion_tag('materials/admin_statistic.html')
def statistic_report():
    ur = UR()
    return {
        'count_by_day': ur.get_svg_count_by_day(),
        #'count_by_month': sr.get_svg_count_by_month(),
    }
