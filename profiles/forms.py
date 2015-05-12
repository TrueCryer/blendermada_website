from __future__ import unicode_literals

from django import forms

from core.settings import COUNTRIES

from .models import UserProfile


class EditProfileForm(forms.ModelForm):
    country = forms.ChoiceField(
        label='Country',
        choices=COUNTRIES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),
    )
    send_newsletters = forms.BooleanField(
        label='Send newsletters',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    send_notifications = forms.BooleanField(
        label='Send notifications',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    show_fullname = forms.BooleanField(
        label='Show full name on site',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    show_email = forms.BooleanField(
        label='Show e-mail on site',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )

    class Meta:
        model = UserProfile
