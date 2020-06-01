"""
This file contains the forms of the
foodfacts app.
"""
from django import forms


class NavSearchForm(forms.Form):
    """Reasearch form's input is got as follows"""
    nav_search = forms.CharField(max_length=100)
