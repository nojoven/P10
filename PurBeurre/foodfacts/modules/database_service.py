"""
Data management code

This file is used to interact with the database
in order to display and manipulate the data.
It uses the orm objects Product, Categories and Favorites
"""
from foodfacts.models import Categories, Products


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
