"""
Data management code

This file is used to interact with the database
in order to display and manipulate the data.
It uses the orm objects Product, Categories and Favorites
"""
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from foodfacts.models import Categories, Favorites, Products


class DatabaseService:
    """
    DatabaseServices

    Class created to provide statics methods
    that allows my terminal app do deal
    with the mysql data.
    Being static makes
    the call of DatabaseService's functions easier.
    """

    # I created this list here to be accessible inside the methods
    articles_ids = []

    # Insert multiple data at a time in multiple rows in (table Product)
    @staticmethod
    def fill_products_table(plist):
        """This executes all the insertion requests needed."""
        list_product = []
        for product in plist:
            list_product.append(
                Products(
                    productname=product["productname"],
                    stores=product["stores"],
                    brands=product["brands"],
                    nutrigrade=product["nutrigrade"],
                    quantity=product["quantity"],
                    category=product["category"],
                    front_img=product["front_img"],
                    nutrition_img=product["nutrition_img"],
                    ingredients_img=product["ingredients_img"],
                    fat_100g=round(product["fat_100g"], 2),
                    sugars_100g=round(product["sugars_100g"], 2),
                    saturated_fat_100g=round(product["saturated_fat_100g"], 2),
                    energy_kcal_100g=round(product["energy_kcal_100g"], 2),
                    nutrition_Score_100g=product["nutrition_Score_100g"],
                    fiber_100g=round(product["fiber_100g"], 2),
                    salt_100g=round(product["salt_100g"], 2),
                    proteins_100g=round(product["proteins_100g"], 2),
                    carbs_100g=round(product["carbs_100g"], 2),
                    sodium_100g=round(product["sodium_100g"], 2),
                    url=product["url"],
                )
            )

        Products.objects.bulk_create(list_product)

    # Insert multiple data at a time in multiple rows in (table Categories)
    @staticmethod
    def fill_categories_table(category):
        """This executes all the insertion requests needed."""
        if not Categories.objects.filter(name=category["name"]).exists():
            query = Categories(**category)
            query.save()

    @staticmethod
    def select_better_products(category_selected, nutriscore):
        """
        Substitution food is extracted here.
        Allows to the display of the better products.
        """
        better_products = Products.objects.filter(
            category=category_selected, nutrition_Score_100g__lt=nutriscore
        )
        return better_products

    @staticmethod
    def select_product(search_term):
        """
        Executes the SELECT request for a
        specific article based on its name.
        """
        term_data = Products.objects.filter(productname=search_term).order_by(
            "-nutrition_Score_100g"
        )[0]
        return term_data

    @staticmethod
    def show_details(product_chosen):
        """Returns the row of an article based on its id"""
        details = Products.objects.get(idproduct=product_chosen)
        return details

    @staticmethod
    def sort_favourites(user_id, term_category):
        """Returns the user's favourites in the exeplored category"""
        relevant_favourites = Favorites.objects.filter(
            userid=user_id, category=term_category
        )
        return relevant_favourites

    @staticmethod
    def create_user(username, password, mail, user_first_name, user_last_name):
        """This easily creates a user thanks to the Django admin system."""
        user = User.objects.create_user(
            username=username,
            password=password,
            email=mail,
            first_name=user_first_name,
            last_name=user_last_name,
        )
        user.save()
        return user

    @staticmethod
    def identify(request, provided_mail, provided_password):
        """
        This performs a SELECT request
        to authenticate a specific user
        """
        user = authenticate(request, username=provided_mail,
                            password=provided_password)
        return user

    @staticmethod
    def select_liked_in_products(liked_id):
        """
        This returns the entire row of the product that we
        want to add to favourites
        """
        product = Products.objects.get(idproduct=liked_id)
        return product

    @staticmethod
    def select_user_favs(userid):
        """Returns the favourites rows of a specific user"""
        user_favs = Favorites.objects.filter(userid=userid)
        return user_favs

    @staticmethod
    def remove_user_fav(userid_unlike, unliked_id):
        """Removes a article from the user's favourites list"""
        unliked_product = Favorites.objects.get(
            userid=userid_unlike, productid=unliked_id
        )
        unliked_product.delete()
        return unliked_product
