"""This file contains the url patterns used by foodfacts"""

from . import views
from django.urls import path
from django.conf.urls import re_path

urlpatterns = [
    path("", views.home, name="home"),
    path("aliment/<int:product_chosen>/",
         views.product_wanted, name="product_chosen"),
    re_path(r"^resultats/?$",
            views.search_term, name="search_term"),
    re_path(r"^notice/?$", views.notice, name="notice"),
]
