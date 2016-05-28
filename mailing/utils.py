from django.db.models import Sum
from django.template import loader, Context

from materials.models import Material, Statistic

from .models import Mail



def generate_digest(date_from, date_to, number):
    new_materials = Material.objects.published(date__gte=date_from, date__lte=date_to).order_by('-date')
    top_downloads = Statistic.objects.filter(date__gte=date_from, date__lte=date_to).values('material').annotate(sum_count=Sum('count')).order_by('-sum_count')[:5]
    top_materials = [(Material.objects.get(pk=top['material']), top['sum_count']) for top in top_downloads]
    t = loader.get_template('mailing/digest.html')
    c = {
        'number': number,
        'date': date_to,
        'new_materials': new_materials,
        'top_materials': top_materials,
    }
    mail = Mail()
    mail.mailing_type = 'sub'
    mail.subject = 'Blendermada digest for {date}'.format(date=date_to)
    mail.message = t.render(c)
    mail.save()