"""This file contains the urls patterns used in the roles app."""
from django.urls import path

from . import views
from django.conf.urls import re_path

urlpatterns = [
    re_path(r"^create/?$", views.create_user, name="create"),
    re_path(r"^signin/?$", views.signin_user, name="signin"),
    re_path(r"^profileupdate/?$", views.update_profile, name="profileupdate"),
    re_path(r"^logout/?$", views.logout_user, name="logout"),
    path("like/<int:product_id>/<int:replaced_id>/", views.like, name="like"),
    path("unlike/<int:unliked_id>/", views.unlike, name="unlike"),
    re_path(r"^favourites/?$", views.favourites, name="favourites"),
    re_path(r"^register/?$", views.create_user, name="register"),
    re_path(r"^account/?$", views.update_profile, name="account"),
]
