from django import forms
from django.forms import ValidationError

from .models import Upload, ENGINE_VERSIONS, SCENE_TYPES


class UploadForm(forms.Form):
    name = forms.CharField(
        label='Name (max 20 characters)',
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input name of material to show on site',
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'placeholder': 'Make a short description of your file',
                'rows': 5,
            }
        )
    )
    engine = forms.ChoiceField(
        choices=ENGINE_VERSIONS,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    scene = forms.ChoiceField(
        choices=SCENE_TYPES,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            },
        ),
    )
    file = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'btn btn-info',
                'placeholder': '*.blend file with material. ONLY *.blend FILE! Make it as small as you can',
            }
        )
    )
    name_in_file = forms.CharField(
        label='Name in file (max 50 characters)',
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Input name of material into uploaded file',
            }
        )
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UploadForm, self).__init__(*args, **kwargs)

    def clean_file(self):
        file_field = self.cleaned_data.get('file', False)
        if file_field:
            if file_field._size > 10*1024*1024:
                raise ValidationError(' too large ( > 10MB )')
            elif file_field.name.split('.')[-1] != 'blend':
                raise ValidationError(' isn\'t *.blend file')
            return file_field
        else:
            raise ValidationError('Couldn\'t read uploaded file')

    def save_data(self):
        instance = Upload(
            name=self['name'].value(),
            description=self['description'].value(),
            engine=self['engine'].value(),
            scene=self['scene'].value(),
            uploaded_file=self['file'].value(),
            name_in_file=self['name_in_file'].value(),
            author=self.user,
        )
        instance.save()
