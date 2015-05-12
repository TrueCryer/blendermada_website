from __future__ import unicode_literals

from collections import OrderedDict

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm

from captcha.fields import CaptchaField
from core.settings import COUNTRIES


class RegistrationForm(forms.Form):
    required_css_class = 'required'
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=30,
        label='Username',
        error_messages={'invalid': 'This value may contain only letters, numbers and @/./+/-/_ characters.'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username (Login)',
            }
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        label='First name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First name',
            }
        ),
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last name',
            }
        ),
        required=False,
    )
    email1 = forms.EmailField(
        label='E-mail',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'E-mail',
            }
        ),
    )
    email2 = forms.EmailField(
        label='Confirm e-mail',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm e-mail',
            }
        ),
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
            },
        ),
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Confirm password',
            }
        ),
    )
    country = forms.ChoiceField(
        label='Where are you from?',
        choices=COUNTRIES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your country',
            },
        ),
    )
    send_newsletters = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='I want to recieve newsletters from Blendermada',
        initial=True,
        required=False,
    )
    send_notifications = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='I want to recieve notification letters from Blendermada',
        initial=True,
        required=False,
    )
    show_fullname = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='Show my full name on the site',
        initial=True,
        required=False,
    )
    show_email = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='Show my e-mail on the site',
        initial=True,
        required=False,
    )
    captcha = CaptchaField()

    def clean_username(self):
        existing = get_user_model().objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError('A user with that username already exists.')
        else:
            return self.cleaned_data['username']

    def clean_password2(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Doesnt\'t match')
        return self.cleaned_data['password2']

    def clean_email1(self):
        if get_user_model().objects.filter(email__iexact=self.cleaned_data['email1']):
            raise forms.ValidationError(
                'Already in use.')
        return self.cleaned_data['email1']

    def clean_email2(self):
        if self.data['email1'] !=  self.data['email2']:
            raise forms.ValidationError('Doesn\'t match')
        return self.cleaned_data['email2']

    def clean(self):
        return self.cleaned_data


class AuthenticationFormBootstrap(AuthenticationForm):
    username = forms.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=30,
        label='Username',
        error_messages={'invalid': 'This value may contain only letters, numbers and @/./+/-/_ characters.'},
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input username',
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input password',
            },
        ),
    )


class PasswordResetFormBootstrap(PasswordResetForm):
    email = forms.EmailField(
        label='E-mail',
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input e-mail',
            },
        ),
    )

    def clean_email(self):
        User = get_user_model()
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            raise forms.ValidationError('Doesn\'t registered')
        return self.cleaned_data['email']


class SetPasswordFormBootstrap(SetPasswordForm):
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password',
            },
        ),
    )
    new_password2 = forms.CharField(
        label='New password confirmation',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'New password confirmation',
            },
        ),
    )


class PasswordChangeFormBootstrap(SetPasswordFormBootstrap, PasswordChangeForm):
    old_password = forms.CharField(
        label='Old password',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Old password',
            },
        ),
    )
PasswordChangeFormBootstrap.base_fields = OrderedDict(
    (k, PasswordChangeFormBootstrap.base_fields[k])
    for k in ['old_password', 'new_password1', 'new_password2']
)


class SettingsForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label='First name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input your first name',
            }
        ),
        required=False,
    )
    last_name = forms.CharField(
        max_length=30,
        label='Last name',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input your last name',
            }
        ),
        required=False,
    )
    country = forms.ChoiceField(
        choices=COUNTRIES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'placeholder': 'Select your country',
            },
        ),
    )
    about = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Write about yourself',
            },
        ),
        required=False,
    )
    website = forms.CharField(
        max_length=255,
        label='Personal website',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'http://',
            }
        ),
        required=False,
    )
    deviantart = forms.CharField(
        max_length=255,
        label='Deviantart page',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'http://deviantart.com/',
            }
        ),
        required=False,
    )
    facebook = forms.CharField(
        max_length=255,
        label='Facebook page',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'http://facebook.com/',
            }
        ),
        required=False,
    )
    twitter = forms.CharField(
        max_length=255,
        label='Twitter page',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'http://twitter.com/',
            }
        ),
        required=False,
    )
    gplus = forms.CharField(
        max_length=255,
        label='Google+ page',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'http://plus.google.com/',
            }
        ),
        required=False,
    )
    send_newsletters = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='I want to recieve newsletters from Blendermada',
        required=False,
    )
    send_notifications = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='I want to recieve notification letters from Blendermada',
        required=False,
    )
    show_fullname = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='Show my full name on the site',
        required=False,
    )
    show_email = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='Show my e-mail on the site',
        required=False,
    )
