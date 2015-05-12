from django.views.generic import DetailView
from django.contrib.auth import get_user_model


class ProfileView(DetailView):
    model = get_user_model()
    slug_field = 'username'


class DetailView(ProfileView):
    template_name = 'profiles/detail.html'


class MaterialsView(ProfileView):
    template_name = 'profiles/materials.html'


class ActivitiesView(ProfileView):
    template_name = 'profiles/activities.html'
