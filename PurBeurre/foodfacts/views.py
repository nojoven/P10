"""File of the views of this Django app are in this file."""
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NavSearchForm
from .models import Products, Favorites


def home(request):
    """Gets the home page"""
    user = request.user
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


def search_term(request):
    """
        Gets the forms inputs in a research of results
    """
    form = NavSearchForm(request.GET)
    context = {}

    if form.is_valid():
        search_word = form.cleaned_data["nav_search"]
        user_id = request.user.id
        term_data = select_product(search_word)
        if term_data is not None:
            term_category = term_data.category
            term_score = term_data.nutrition_Score_100g

            context["product"] = term_data

            better_products = select_better_products(
                term_category, term_score
            )
            relevant_favourites = sort_favourites(
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
    return render(request, "resultats.html", context)


def product_wanted(request, product_chosen):
    """Renders a context for the details page."""
    context = dict()
    try:
        product = show_details(product_chosen)
        context.update({"product": product})
    except ObjectDoesNotExist:
        print("IMPOSSIBLE DE RECUPERER CE PRODUIT")
    return render(request, "aliment.html", context)


def select_product(search_term):
    """
    Executes the SELECT request for a
    specific article based on its name.
    """
    term_data = Products.objects.filter(
        productname__icontains=search_term
    ).order_by(
        "-nutrition_Score_100g"
    ).first()
    return term_data


def select_better_products(
        category_selected,
        nutriscore
):
    """
    Substitution food is extracted here.
    Allows to the display of the better products.
    """
    better_products = Products.objects.filter(
        category=category_selected,
        nutrition_Score_100g__lt=nutriscore
    )
    return better_products


def sort_favourites(user_id,
                    term_category
                    ):
    """
    Returns the user's favourites in the exeplored category
    """
    relevant_favourites = Favorites.objects.filter(
        userid=user_id,
        category=term_category
    )
    return relevant_favourites


def show_details(product_chosen):
    """Returns the row of an article based on its id"""
    details = Products.objects.get(
        idproduct=product_chosen)
    return details
