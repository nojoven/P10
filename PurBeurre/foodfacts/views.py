"""File of the views of this Django app are in this file."""
from foodfacts.modules.database_service import DatabaseService
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import NavSearchForm


def home(request):
    """Gets the home page"""
    user = request.user
    print(user)
    return render(request, "accueil.html", {"user": user})


def aliment(product_chosen):
    """Gets the details page"""
    return HttpResponseRedirect(product_chosen)


def resultats(request):
    """Gets the results page"""
    return render(request, "resultats.html")


def notice(request):
    """Gets the notices page"""
    return render(request, "mentions_legales.html")


def research(request):
    """Gets the forms inputs in a research of results"""
    form = NavSearchForm(request.POST)
    search_term = "empty"
    if form.is_valid():
        search_term = form.cleaned_data["nav_search"]
    url = reverse("search_term", args=[search_term])
    return HttpResponseRedirect(url)


def research_term(request, search_term):
    """Renders a context for the results page"""
    user_id = request.user.id
    context = {}
    try:
        term_data = DatabaseService.select_product(search_term)
        term_category = term_data.category
        term_score = term_data.nutrition_Score_100g

        context["product"] = term_data
        try:
            better_products = DatabaseService.select_better_products(
                term_category, term_score
            )
            relevant_favourites = DatabaseService.sort_favourites(
                user_id, term_category
            )
            favs_id_list = []
            for item in relevant_favourites:
                favs_id_list.append(item.productid)
            if better_products is not None and len(better_products) > 0:
                context["better"] = better_products
                context["favs"] = favs_id_list
            else:
                context["better"] = None
        except IndexError:
            print(
                "SUBTSTITUTION RESEARCH FAILED")
    except IndexError:
        print("NOT FOUND")

    return render(request, "resultats.html", context)


def product_wanted(request, product_chosen):
    """Renders a context for the details page."""
    context = dict()
    try:
        product = DatabaseService.show_details(product_chosen)
        context.update({"product": product})
    except ObjectDoesNotExist:
        print("IMPOSSIBLE DE RECUPERER CE PRODUIT")
    return render(request, "aliment.html", context)
