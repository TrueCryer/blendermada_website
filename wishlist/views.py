from django.views.generic import ListView

from .models import Wish

# Create your views here.

class WishListView(ListView):
    model = Wish
    template_name = 'wishlist/list.html'
    paginate_by = 10