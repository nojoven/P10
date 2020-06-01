"""This form contains the forms of the roles app."""
from django import forms
from django.core.exceptions import ValidationError


class CreateForm(forms.Form):
    """This is the sign up form """
    prenom = forms.CharField(max_length=100)
    nom = forms.CharField(max_length=100)
    mot_de_passe = forms.CharField(max_length=100)
    repeter_mot_de_passe = forms.CharField(max_length=100)
    mail = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=100)

    def is_valid(self):

        if self.data.get("mot_de_passe") \
                != self.data.get("repeter_mot_de_passe"):
            self.add_error(
                field="mot_de_passe",
                error=ValidationError(
                    "Les mots de passe doivent être identiques",
                    code="unmatch",
                ),
            )
            return False

        return super().is_valid()


class SigninForm(forms.Form):
    """This is the sign in form """
    signin_email = forms.CharField(max_length=100)
    signin_password = forms.CharField(max_length=100)


class UpdateProfileForm(forms.Form):
    """This is the update form """
    update_email = forms.CharField(max_length=100)
    update_first_name = forms.CharField(max_length=100)
    update_last_name = forms.CharField(max_length=100)
    confirm_email = forms.CharField(max_length=100)
    confirm_password = forms.CharField(max_length=100)


class LikeForm(forms.Form):
    """This is the form to add a favourite."""
    liked_id = forms.IntegerField()
    replaced_id = forms.CharField(max_length=100)
    replaced_name = forms.CharField(max_length=100)
    replaced_nutrigrade = forms.CharField(max_length=100)
    userid = forms.CharField(max_length=100)


class UnlikeForm(forms.Form):
    """This is the form to delete a favourite."""
    unliked_id = forms.IntegerField()
    userid_unlike = forms.CharField(max_length=100)
