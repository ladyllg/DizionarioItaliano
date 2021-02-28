from django import forms

class SearchForm(forms.Form):
    parola = forms.CharField(label='Parola', required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Cerca in dizionario...', 'class': 'form-control'}) )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        