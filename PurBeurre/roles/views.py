import logging
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from foodfacts.models import (
    Favorites,
    Products
)

from .forms import (
    CreateForm,
    SigninForm,
    UpdateProfileForm
)

LOGGER = logging.getLogger(__name__)


def create_user(request):
    """Creates a user based on form inputs"""
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                request,
                username=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password1")
            )
            if user is not None:
                login(request, user)
                return redirect("account")
            else:
                return render(request, "register.html", {"form": form})
        else:
            return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": CreateForm()})


def signin_user(request):
    """Logs a user in based on form inputs"""
    if request.method == "POST":
        form = SigninForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(
                request,
                username=mail,
                password=password
                )
            if user is not None:
                login(request, user)
                return redirect("account")
            else:
                form.add_error(
                        field="email",
                        error=ValidationError(
                            "Email ou mot de passe incorrect"),
                    )
                return render(request, "signin.html", {"form": form})
        else:
            return render(request, "signin.html", {"form": form})

    return render(request, "signin.html", {"form": SigninForm()})


def update_profile(request):
    """Updates user data based on user inputs."""
    # instance is used to indicate the current user
    if request.method == "POST":
        form = UpdateProfileForm(
            request.POST,
            instance=request.user)

        if form.is_valid():
            form.save()
            return render(
                request,
                "mon_compte.html",
                {"form": UpdateProfileForm(instance=request.user)})
        else:
            return render(request, "mon_compte.html", {"form": form})
    else:
        return render(
            request,
            "mon_compte.html",
            {"form": UpdateProfileForm(instance=request.user)})


def logout_user(request):
    """Logs out a user based on form inputs"""
    logout(request)
    return redirect("signin")


def like(request, product_id, replaced_id):
    """Adds a favourite to the database for a user"""
    if request.method == "POST":
        user = request.user
        if product_id:
            product = select_liked_in_products(product_id)
            like_data = dict()
            like_data["productid"] = product_id
            like_data["name"] = product.productname
            like_data["nutrigrade"] = product.nutrigrade
            like_data["category"] = product.category
            like_data["replacedid"] = replaced_id
            if user.id is not None:
                like_data["userid"] = user.id
            else:
                like_data["userid"] = 0
            like_data["front_img"] = product.front_img
            if not Favorites.objects.filter(
                productid=product.idproduct,
                userid=user.id
            ).exists():
                query = Favorites(**like_data)
                query.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
        else:
            return render(request, "resultats.html")
    else:
        return render(request, "resultats.html")


def favourites(request):
    """Allows to display the favourites of a user in the template"""
    userid = request.user.id
    user_favs = select_user_favs(userid)
    return render(
        request, "mes_aliments.html", {"favlist": user_favs}
    )


def unlike(request, unliked_id):
    """Adds a favourite to the database for a user"""
    if request.method == "POST":
        remove_user_fav(
            request.user.id, unliked_id
        )
        url = reverse("favourites")
        return HttpResponseRedirect(url)


def account(request):
    """Returns the account page"""
    return render(request, "mon_compte.html")


def select_liked_in_products(liked_id):
    """
    This returns the entire row of the product that we
    want to add to favourites
    """
    product = Products.objects.get(
        idproduct=liked_id
    )
    return product


def select_user_favs(userid):
    """
    Returns the favourites rows of a specific user
    """
    user_favs = Favorites.objects.filter(
        userid=userid)
    return user_favs


def remove_user_fav(userid_unlike, unliked_id):
    """Removes a article from the user's favourites list"""
    unliked_product = Favorites.objects.get(
        userid=userid_unlike, productid=unliked_id
    )
    unliked_product.delete()
    return unliked_product
