"""This file contains the url patterns used by foodfacts"""

from . import views
from django.urls import path
from django.conf.urls import re_path


urlpatterns = [
    path("", views.home, name="home"),
    re_path(r"^resultats/?$",
            views.resultats, name="resultats"),
    path("aliment/<int:product_chosen>/",
         views.product_wanted, name="product_chosen"),
    path("resultats/<str:search_term>/",
         views.research_term, name="search_term"),
    re_path(r"^research/?$",
            views.research, name="research"),
    re_path(r"^notice/?$", views.notice, name="notice"),
]
