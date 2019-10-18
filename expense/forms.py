from django import forms

class AddTransactionForm(forms.Form):
    created_at = forms.DateTimeField(
        # widget=forms.TextInput(attrs={'placeholder': 'Pick-up Date & Time', 'autocomplete': "off"}),
        input_formats=["%d/%m/%Y %H:%M", "%d/%m/%Y %I:%M %p", "%Y-%m-%d %H:%M"],
        error_messages={'required': 'transaction date is missing.'})
    amount = forms.FloatField()