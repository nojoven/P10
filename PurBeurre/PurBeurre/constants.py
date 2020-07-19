"""
The purpose of this file is to provide
constants to the project's functions
"""

IMG_URL = "https://static.openfoodfacts.org/images/"\
          "products/301/136/002/3995/front_fr.39.400.jpg"

CATEGORIES_URL = "https://world.openfoodfacts.org/"\
                 "categories.json"

PRODUCT_EXAMPLE = {
    "idproduct": 44,
    "category": "soup",
    "stores": "Auchan",
    "brands": "Reflets",
    "productname": "Gazpacho",
    "nutrigrade": "a",
    "quantity": "1L",
    "front_img": "img.jpg",
    "nutrition_img": "img.png",
    "ingredients_img": "img.svg",
    "fat_100g": 0.20,
    "sugars_100g": 3.20,
    "saturated_fat_100g": 0.20,
    "energy_kcal_100g": 250.16,
    "nutrition_Score_100g": -4,
    "fiber_100g": 24.14,
    "salt_100g": 1.03,
    "proteins_100g": 5.63,
    "carbs_100g": 3.20,
    "sodium_100g": 1.03,
    "url": "www.url.com"
}

FAVOURITE_EXAMPLE = {
    "productid": 44,
    "name": "Gazpacho",
    "nutrigrade": "a",
    "category": "soup",
    "replacedid": 191,
    "userid": 1,
    "front_img": "www.url.com"
}

USER_EXAMPLE = {
    "id": 1,
    "username": "Arnold6262",
    "first_name": "Giuseppe",
    "last_name": "Verdi",
    "email": "gverdi@gmail.com",
    "password1": "pasTest2020",
    "password2": "pasTest2020"
}
