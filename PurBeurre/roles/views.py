import logging
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import foodfacts.models as models
from foodfacts.modules.database_service import DatabaseService
from .forms import (
    CreateForm,
    SigninForm,
    UpdateProfileForm,
    LikeForm,
    UnlikeForm)

LOGGER = logging.getLogger(__name__)


def create_user(request):
    """Creates a user based on form inputs"""
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            user_first_name = form.cleaned_data["prenom"]
            user_last_name = form.cleaned_data["nom"]
            user_phone = form.cleaned_data["telephone"]
            user_phone_ending = user_phone[-6:-1]
            username = f"{user_first_name}{user_phone_ending}{user_last_name}"
            password = form.cleaned_data["mot_de_passe"]
            mail = form.cleaned_data["mail"]
            user = DatabaseService.create_user(
                username, password, mail, user_first_name, user_last_name
            )
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/roles/account")
            else:
                return render(request, "register.html", {"form": form})
        else:
            return render(request, "register.html", {"form": form})
    return render(request, "register.html", {"form": CreateForm()})


def signin_user(request):
    """Logs a user in based on form inputs"""
    if request.method == "POST":
        form = SigninForm(request.POST)
        user = None
        if form.is_valid():
            provided_mail = form.cleaned_data["signin_email"]
            provided_password = form.cleaned_data["signin_password"]
            user = DatabaseService.identify(
                request,
                provided_mail,
                provided_password)

        if user is not None:
            login(request, user)
            return render(request, "mon_compte.html")
        else:
            form.add_error(
                field="signin_email",
                error=ValidationError("Email incorrect", code="signin_mail"),
            )
            form.add_error(
                field="signin_password",
                error=ValidationError("Mot de passe incorrect",
                                      code="signin_password"),
            )
            return render(request, "signin.html", {"form": form})

    return render(request, "signin.html", {"form": SigninForm()})


def update_profile(request):
    """Updates user data based on user inputs."""
    if request.method == "POST":
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            update_first_name = form.cleaned_data["update_first_name"]
            update_last_name = form.cleaned_data["update_last_name"]
            update_email = form.cleaned_data["update_email"]
            confirm_email = form.cleaned_data["confirm_email"]
            confirm_password = form.cleaned_data["confirm_password"]
        else:
            return render(request, "mon_compte.html", {"form": form})

        if update_first_name \
                or update_last_name \
                or update_email:
            user = DatabaseService.identify(
                request, confirm_email,
                confirm_password)
            if user is not None:
                if update_email != "":
                    user.email = update_email
                if update_first_name != "":
                    user.first_name = update_first_name
                if update_last_name != "":
                    user.last_name = update_last_name
                user.save()
                return render(request, "mon_compte.html", {"user": user})
            else:
                form.add_error(
                    field="confirm_email",
                    error=ValidationError(
                        "Email de confirmation incorrect",
                        code="confirm_email"
                    ),
                )
                form.add_error(
                    field="confirm_password",
                    error=ValidationError(
                        "Mot de passe à bien confirmer.",
                        code="confirm_email"
                    ),
                )
                return render(request, "mon_compte.html", {"form": form})
        else:
            return render(request, "mon_compte.html", {"form": form})

    return render(request, "mon_compte.html", {"form": UpdateProfileForm()})


def logout_user(request):
    """Logs out a user based on form inputs"""
    logout(request)
    return render(request, "signin.html")


def like(request):
    """Adds a favourite to the database for a user"""
    if request.method == "POST":
        form = LikeForm(request.POST)
        LOGGER.info("LIKE FORM")
        if form.is_valid():
            LOGGER.info("VALID FORM")
            liked_id = form.cleaned_data["liked_id"]
            replaced_id = form.cleaned_data["replaced_id"]
            replaced_name = form.cleaned_data["replaced_name"]
            replaced_nutrigrade = form.cleaned_data["replaced_nutrigrade"]
            userid = form.cleaned_data["userid"]

            if liked_id:
                product = DatabaseService.select_liked_in_products(liked_id)

                like_data = dict()
                like_data["productid"] = liked_id
                like_data["name"] = product.productname
                like_data["nutrigrade"] = product.nutrigrade
                like_data["stores"] = product.stores
                like_data["brands"] = product.brands
                like_data["category"] = product.category
                like_data["quantity"] = product.quantity
                like_data["replacedid"] = replaced_id
                like_data["replacedarticle"] = replaced_name
                like_data["replacednutrigrade"] = replaced_nutrigrade
                like_data["userid"] = userid
                like_data["front_img"] = product.front_img

                if not models.Favorites.objects.filter(
                    productid=product.idproduct
                ).exists():
                    query = models.Favorites(**like_data)
                    query.save()
            url = reverse("search_term", args=[replaced_name])
            return HttpResponseRedirect(url)
        else:
            return render(request, "resultats.html", {"form": form})
    else:
        return render(request, "resultats.html")


def favourites(request):
    """Allows to display the favourites of a user in the template"""
    userid = request.user.id
    user_favs = DatabaseService.select_user_favs(userid)
    return render(request, "mes_aliments.html", {"favlist": user_favs})


def unlike(request):
    """Adds a favourite to the database for a user"""
    if request.method == "POST":
        form = UnlikeForm(request.POST)
        if form.is_valid():
            unliked_id = form.cleaned_data["unliked_id"]
            userid_unlike = form.cleaned_data["userid_unlike"]
            DatabaseService.remove_user_fav(userid_unlike, unliked_id)

        url = reverse("favourites")
        return HttpResponseRedirect(url)


def register(request):
    """Returns the register page"""
    return render(request, "register.html")


def account(request):
    """Returns the account page"""
    return render(request, "mon_compte.html")
