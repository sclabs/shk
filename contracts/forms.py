from django import forms

class VillageForm(forms.Form):
    name = forms.CharField(max_length=30)
