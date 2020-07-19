"""This form contains the forms of the roles app."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateForm(UserCreationForm):
    """'This is the sign up form '"""
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            'first_name', 'last_name', 'email',)


class SigninForm(forms.Form):
    """This is the sign in form """
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput,
                               max_length=100, required=True)

    def clean(self):
        # data from the form is fetched using super function
        super(SigninForm, self).clean()

        # extract the username and text field from the data
        self.email = self.cleaned_data.get('email')
        self.password = self.cleaned_data.get('password')

        if len(self.password) < 2:
            self._errors['password'] = self.error_class([
                'Password  Should Contain a minimum of 2 characters'])

        return self.cleaned_data


class UpdateProfileForm(forms.ModelForm):
    """This is the update form """
    email = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
