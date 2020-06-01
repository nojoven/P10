"""

Creating and populating the database

This file is used to :

    - Create the MySQL tables "Categories", "Products" and  "Favorites"
    - Populate the "Categories" table
    - Retrieve the API data
    - Use the API Data to populate the "Products" table

"""

# Importing the Database objects provided by the ORM
# and the module to that has a requester object (named 'Collector')
from foodfacts.collector import Collector
from foodfacts.modules.database_service import DatabaseService
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """This command becomes available from manage.py"""

    help = "Fills the database."

    def handle(self, *args, **options):
        """
        This function is used to run
        the fetching and the filling
        of the tables
        """
        # Creation of the tables using makemigration and migrate
        # Instantiation of a Collector
        collector = Collector()

        # I defined there a tuple of categories
        list_of_categories = ("soup", "pizza", "salad", "cake", "cheese")

        # I populate the table of the categories
        for category in list_of_categories:
            category_entry = {"name": category}
            DatabaseService.fill_categories_table(category_entry)

        # I retrieve only the products that correspond to my categories
        # in my tuple and I populate the products table
        for category in list_of_categories:
            food_returned = collector.get_products_by_category(category)
            DatabaseService.fill_products_table(food_returned)
