from django import forms

from django.core.exceptions import ValidationError

from .models import *

#
# class NewVisitorForm(forms.Form):
#     email = forms.EmailField(label='Your email')


class NewMeetupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['location'].empty_label = 'Место не выбрано'

    class Meta:
        model = MeetUp
        # fields = '__all__'
        fields = ['title', 'slug', 'description', 'date', 'image', 'location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # Пользовательские валидаторы(Проверка корректности введенных данных)
    def clean_title(self):  # start with clean_ than any field
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина названия превышает 100 символов')
        return title


