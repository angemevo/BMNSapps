from django.forms import ModelForm
from reservation_billet.models import Client
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError


class UserForms(ModelForm):
    class Meta:
        model = Client
        fields = ['Contact', 'Adresse']
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields["Contact"].widget.attrsx.update(
                {
                    "class": "form-control",
                    "placeholder": "Contact"
                }
            )
            
            self.fields["Adresse"].widget.attrsx.update(
                {
                    "class": "form-control",
                    "placeholder": "Adresse"
                }
            )
                


