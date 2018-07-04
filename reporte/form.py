from django import forms
from decimal import Decimal


class ReporteForm(forms.Form):
    mes = forms.DecimalField(max_digits = 2, decimal_places=0, min_value=1, max_value=12)
    año = forms.DecimalField(max_digits = 4, decimal_places=0, min_value=2018, max_value=2030)
