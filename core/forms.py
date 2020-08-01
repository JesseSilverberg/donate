from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Donator

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(max_length=100, help_text='Last Name')
    # last_name = forms.CharField(max_length=100, help_text='Last Name')
    # email = forms.EmailField(max_length=150, help_text='Email')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'email', 'username', 'password1', 'password2',)


class DonateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DonateForm, self).__init__(*args, **kwargs)

        # If you pass FormHelper constructor a form instance
        # It builds a default layout with all its fields
        self.helper = FormHelper(self)

        # You can dynamically adjust your layout
        self.helper.layout.append(Submit('submit', 'Submit', css_class='btn-primary'))

    class Meta:
        model = Donator
        fields = ['bio', 'location', 'birth_date']
