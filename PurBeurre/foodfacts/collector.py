"""
API call

This code allows to fetch the data
from the OpenFoodFact API.
It uses the built-in modules JSON and requests
"""
import requests as reqs
from json import JSONDecodeError


class Collector:
    """

    The collect of the data is done
    by a Collector object.

    This class is used to rerieve the products data
    by calling the OpenFoodFacts API.
    """

    def __init__(self):
        """

        Request components

        When instantiated a Collector object receives
        two attributes that are necessary
        to send an HTTP request:
        - the query params
        - the url
        """
        # We limit the fetch to 1000 products
        self.params = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": "category",
            "sort_by": "unique_scans_n",
            "page_size": 1000,
            "json": 1,
        }
        self.url = "https://fr.openfoodfacts.org/cgi/search.pl"

    def get_products_by_category(self, category):
        """
        Five API requests for my five categories.

        I send a GET request for 1000 product
        of a category, then 1000 from another one, etc.
        """
        # I create lists to use them later
        results = []
        products = []
        try:
            self.params["tag_0"] = category
            req = reqs.get(self.url, self.params)
            data = req.json()
            products = data["products"]

        except JSONDecodeError:
            pass

        for product in products:
            product_data = dict()
            try:
                product_data = {
                    "category": category,
                    "stores": str(product["stores_tags"])[1:-1],
                    "brands": product["brands"],
                    "productname": product["product_name"],
                    "nutrigrade": product["nutrition_grade_fr"],
                    "quantity": product["quantity"],
                    "front_img": product["selected_images"][
                        "front"]["display"]["fr"],
                    "nutrition_img": product["selected_images"][
                        "nutrition"]["display"]["fr"],
                    "ingredients_img": product["selected_images"][
                        "ingredients"]["display"]["fr"],
                    "fat_100g": float(product["nutriments"][
                                          "fat_100g"]),
                    "sugars_100g": float(product["nutriments"][
                                             "sugars_100g"]),
                    "saturated_fat_100g": float(
                        product["nutriments"]["saturated-fat_100g"]
                    ),
                    "energy_kcal_100g": float(
                        product["nutriments"]["energy-kcal_100g"]
                    ),
                    "nutrition_Score_100g": int(
                        product["nutriments"]["nutrition-score-fr_100g"]
                    ),
                    "fiber_100g": float(
                        product["nutriments"]["fiber_100g"]),
                    "salt_100g": float(
                        product["nutriments"]["salt_100g"]),
                    "proteins_100g": float(
                        product["nutriments"]["proteins_100g"]),
                    "carbs_100g": float(
                        product["nutriments"]["carbohydrates_100g"]),
                    "sodium_100g": float(
                        product["nutriments"]["sodium_100g"]),
                    "url": product["url"],
                }

            except KeyError:
                continue
            except Exception as err:
                print(err)
            results.append(product_data)
        return results
