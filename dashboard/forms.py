from django import forms


class fipsNumber(forms.Form):
    fips = forms.CharField(label='fipNum', max_length=5, widget=forms.TextInput(attrs={'id': 'fipsInput'}))
