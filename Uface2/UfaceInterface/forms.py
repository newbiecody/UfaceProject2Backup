from django import forms
from .models import select1

class SelectForm(forms.ModelForm):
    class Meta:
        model = select1
        fields = ['Course', 'Index', 'Session']